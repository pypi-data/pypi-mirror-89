import re

import boto3
import logging
import requests
from datetime import datetime, timezone, timedelta

from botocore import UNSIGNED
from botocore.client import Config

from time import sleep
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from indra import get_config, has_config
from indra.util.nested_dict import NestedDict

logger = logging.getLogger(__name__)


def get_ids(job_list):
    if job_list is None:
        return None
    return [job['jobId'] for job in job_list]


def kill_all(job_queue, reason='None given', states=None, kill_list=None):
    """Terminates/cancels all jobs on the specified queue.

    Parameters
    ----------
    job_queue : str
        The name of the Batch job queue on which you wish to terminate/cancel
        jobs.
    reason : str
        Provide a reason for the kill that will be recorded with the job's
        record on AWS.
    states : None or list[str]
        A list of job states to remove. Possible states are 'STARTING',
        'RUNNABLE', and 'RUNNING'. If None, all jobs in all states will be
        ended (modulo the `kill_list` below).
    kill_list : None or list[dict]
        A list of job dictionaries (as returned by the submit function) that
        you specifically wish to kill. All other jobs on the queue will be
        ignored. If None, all jobs on the queue will be ended (modulo the
        above).

    Returns
    -------
    killed_ids : list[str]
        A list of the job ids for jobs that were killed.
    """
    # Default is all states.
    if states is None:
        states = ['STARTING', 'RUNNABLE', 'RUNNING']

    # Get batch client
    batch = boto3.client('batch')

    # Get all other jobs, and terminate them.
    killed_ids = []
    for status in states:
        running = batch.list_jobs(jobQueue=job_queue, jobStatus=status)
        active_job_list = running.get('jobSummaryList')
        if active_job_list is None:
            continue

        for job in active_job_list:
            # Check if this is one of the specified jobs, if any specified.
            ids_to_kill = get_ids(kill_list)
            if ids_to_kill is not None and job['jobId'] not in ids_to_kill:
                continue

            # End the job.
            if status == 'RUNNING':
                logger.info('Terminating {jobName} ({jobId})'.format(**job))
                res = batch.terminate_job(jobId=job['jobId'], reason=reason)
            else:
                logger.info('Canceling {jobName} ({jobId})'.format(**job))
                res = batch.cancel_job(jobId=job['jobId'], reason=reason)

            # Record the result of the kill
            killed_ids.append(res)

    return killed_ids


def tag_instance(instance_id, **tags):
    """Tag a single ec2 instance."""
    logger.debug("Got request to add tags %s to instance %s."
                 % (str(tags), instance_id))
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)

    # Remove None's from `tags`
    filtered_tags = {k: v for k, v in tags.items() if v and k}

    # Check for existing tags
    if instance.tags is not None:
        existing_tags = {tag.get('Key'): tag.get('Value')
                         for tag in instance.tags}
        logger.debug("Ignoring existing tags; %s" % str(existing_tags))
        for tag_key in existing_tags.keys():
            filtered_tags.pop(tag_key, None)

    # If we have new tags to add, add them.
    tag_list = [{'Key': k, 'Value': v} for k, v in filtered_tags.items()]
    if len(tag_list):
        logger.info('Adding project tags "%s" to instance %s'
                    % (filtered_tags, instance_id))
        instance.create_tags(Tags=tag_list)
        vols = instance.volumes.all()
        for page in vols.pages():
            for vol in page:
                vol.create_tags(Tags=tag_list)
    else:
        logger.info('No new tags from: %s' % str(tags))
    return


def tag_myself(project='cwc', **other_tags):
    """Function run when indra is used in an EC2 instance to apply tags."""
    base_url = "http://169.254.169.254"
    try:
        resp = requests.get(base_url + "/latest/meta-data/instance-id")
    except requests.exceptions.ConnectionError:
        logger.warning("Could not connect to service. Note this should only "
                       "be run from within a batch job.")
        return
    instance_id = resp.text
    tag_instance(instance_id, project=project, **other_tags)
    return


def get_batch_command(command_list, project=None, purpose=None):
    """Get the command appropriate for running something on batch."""
    command_str = ' '.join(command_list)
    ret = ['python3', '-m', 'indra.util.aws', 'run_in_batch', command_str]
    if not project and has_config('DEFAULT_AWS_PROJECT'):
        project = get_config('DEFAULT_AWS_PROJECT')
    if project:
        ret += ['--project', project]
    if purpose:
        ret += ['--purpose', purpose]
    return ret


def run_in_batch(command_list, project, purpose):
    from subprocess import call
    tag_myself(project, purpose=purpose)
    logger.info("Running command list: %s" % str(command_list))
    logger.info('\n'+20*'='+' Begin Primary Command Output '+20*'='+'\n')
    ret_code = call(command_list)
    logger.info('\n'+21*'='+' End Primary Command Output '+21*'='+'\n')
    return ret_code


def get_jobs(job_queue='run_reach_queue', job_status='RUNNING'):
    """Returns a list of dicts with jobName and jobId for each job with the
    given status."""
    batch = boto3.client('batch')
    jobs = batch.list_jobs(jobQueue=job_queue, jobStatus=job_status)
    return jobs.get('jobSummaryList')


s3_path_patt = re.compile('^s3:([-a-zA-Z0-9_]+)/(.*?)$')


class JobLog(object):
    """Gets the Cloudwatch log associated with the given job.

    Parameters
    ----------
    job_info : dict
        dict containing entries for 'jobName' and 'jobId', e.g., as returned
        by get_jobs()
    log_group_name : string
        Name of the log group; defaults to '/aws/batch/job'

    Returns
    -------
    list of strings
        The event messages in the log, with the earliest events listed first.
    """
    _suffix_base = '/part_'

    def __init__(self, job_info, log_group_name='/aws/batch/job',
                 verbose=False, append_dumps=True):
        self.job_name = job_info['jobName']
        self.job_id = job_info['jobId']
        self.logs_client = boto3.client('logs')
        self.verbose = verbose
        self.log_group_name = log_group_name
        batch = boto3.client('batch')
        resp = batch.describe_jobs(jobs=[self.job_id])
        job_desc = resp['jobs'][0]
        job_def_name = job_desc['jobDefinition'].split('/')[-1].split(':')[0]
        task_arn_id = job_desc['container']['taskArn'].split('/')[-1]
        self.log_stream_name = '%s/default/%s' % (job_def_name, task_arn_id)
        self.latest_timestamp = None
        self.lines = []
        self.nextToken = None
        self.__len = 0
        self.append = append_dumps
        return

    def __len__(self):
        return self.__len

    def clear_lines(self):
        self.lines = []

    def dump(self, out_file, append=None):
        """Dump the logs in their entirety to the specified file."""
        if append is None:
            append = self.append
        elif append != self.append:
            logger.info("Overriding default append behavior. This could muddy "
                        "future loads.")
        m = s3_path_patt.match(out_file)
        if m is not None:
            # If the user wants the files on s3...
            bucket, prefix = m.groups()
            s3 = boto3.client('s3')

            # Find the largest part number among the current suffixes
            if append:
                max_num = 0
                for key in iter_s3_keys(s3, bucket, prefix, do_retry=False):
                    if key[len(prefix):].startswith(self._suffix_base):
                        num = int(key[len(prefix + self._suffix_base):])
                        if max_num > num:
                            max_num = num

                # Create the new suffix, and dump the lines to s3.
                new_suffix = self._suffix_base + str(max_num + 1)
                key = prefix + new_suffix
            else:
                key = prefix
            s3.put_object(Bucket=bucket, Key=key, Body=self.dumps())
        else:
            # Otherwise, if they want them locally...
            with open(out_file, 'wt' if append else 'w') as f:
                for line in self.lines:
                    f.write(line)
        return

    def load(self, out_file):
        """Load the log lines from the cached files."""
        m = s3_path_patt.match(out_file)
        if m is not None:
            bucket, prefix = m.groups()
            s3 = boto3.client('s3')

            if self.append:
                prior_line_bytes = []
                for key in sorted(iter_s3_keys(s3, bucket, prefix)):
                    if key[len(prefix):].startswith(self._suffix_base):
                        res = s3.get_object(Bucket=bucket, Key=key)
                        prior_line_bytes += res['Body'].read().splitlines()
            else:
                res = s3.get_object(Bucket=bucket, Key=prefix)
                prior_line_bytes = res['Body'].read().splitlines()

            prior_lines = [s.decode('utf-8') + '\n'
                           for s in prior_line_bytes]
        else:
            with open(out_file, 'r') as f:
                prior_lines = f.readlines()
        self.lines = prior_lines + self.lines
        return

    def dumps(self):
        return ''.join(self.lines)

    def get_lines(self):
        kwargs = {'logGroupName': self.log_group_name,
                  'logStreamName': self.log_stream_name,
                  'startFromHead': True}
        while True:
            if self.nextToken is not None:
                kwargs['nextToken'] = self.nextToken
            response = self.logs_client.get_log_events(**kwargs)
            # If we've gotten all the events already, the nextForwardToken for
            # this call will be the same as the last one
            if response.get('nextForwardToken') == self.nextToken:
                break
            else:
                events = response.get('events')
                if events:
                    for evt in events:
                        line = '%s: %s\n' % (evt['timestamp'], evt['message'])
                        self.lines.append(line)
                        self.latest_timestamp = \
                            (datetime.fromtimestamp(evt['timestamp']/1000)
                                     .astimezone(timezone.utc)
                                     .replace(tzinfo=None))
                        self.__len += 1
                        if self.verbose:
                            logger.info('%d %s' % (len(self.lines), line))
                self.nextToken = response.get('nextForwardToken')
        return


def dump_logs(job_queue='run_reach_queue', job_status='RUNNING'):
    """Write logs for all jobs with given the status to files."""
    jobs = get_jobs(job_queue, job_status)
    for job in jobs:
        log = JobLog(job)
        log.get_lines()
        log.dump('{jobName}_{jobId}.log'.format(**job))


def get_date_from_str(date_str):
    """Get a utc datetime object from a string of format %Y-%m-%d-%H-%M-%S

    Parameters
    ----------
    date_str : str
        A string of the format %Y(-%m-%d-%H-%M-%S). The string is assumed
        to represent a UTC time.

    Returns
    -------
    datetime.datetime
    """
    date_format = '%Y-%m-%d-%H-%M-%S'
    # Pad date_str specifying less than full format
    if 1 <= len(date_str.split('-')) < 6:
        # Add Jan if not present
        if len(date_str.split('-')) == 1:
            date_str += '-01'
        # Add day after month if not present
        if len(date_str.split('-')) == 2:
            date_str += '-01'
        # Pad with 0 hours, 0 minutes and 0 seconds
        while len(date_str.split('-')) < 6:
            date_str += '-0'
    return datetime.strptime(
        date_str, date_format).replace(
        tzinfo=timezone.utc)


def iter_s3_keys(s3, bucket, prefix, date_cutoff=None, after=True,
                 with_dt=False, do_retry=True):
    """Iterate over the keys in an s3 bucket given a prefix

    Parameters
    ----------
    s3 : boto3.client.S3
        A boto3.client.S3 instance
    bucket : str
        The name of the bucket to list objects in
    prefix : str
        The prefix filtering of the objects for list
    date_cutoff : str|datetime.datetime
        A datestring of format %Y(-%m-%d-%H-%M-%S) or a datetime.datetime
        object. The date is assumed to be in UTC. By default no filtering
        is done. Default: None.
    after : bool
        If True, only return objects after the given date cutoff.
        Otherwise, return objects before. Default: True
    with_dt : bool
        If True, yield a tuple (key, datetime.datetime(LastModified)) of
        the s3 Key and the object's LastModified date as a
        datetime.datetime object, only yield s3 key otherwise.
        Default: False.
    do_retry : bool
        If True, and no contents appear, try again in case there was simply a
        brief lag. If False, do not retry, and just accept the "directory" is
        empty.

    Returns
    -------
    iterator[key]|iterator[(key, datetime.datetime)]
        An iterator over s3 keys or (key, LastModified) tuples.
    """
    if date_cutoff:
        date_cutoff = date_cutoff if\
            isinstance(date_cutoff, datetime) else\
            get_date_from_str(date_cutoff)
        # Check timezone info
        if date_cutoff.utcoffset() is None:
            date_cutoff = date_cutoff.replace(tzinfo=timezone.utc)
        if date_cutoff.utcoffset() != timedelta():
            date_cutoff = date_cutoff.astimezone(timezone.utc)
    is_truncated = True
    marker = None
    while is_truncated:
        # Get the (next) batch of contents.
        if marker:
            resp = s3.list_objects(Bucket=bucket, Prefix=prefix, Marker=marker)
        else:
            resp = s3.list_objects(Bucket=bucket, Prefix=prefix)

        # Handle case where no contents are found.
        if not resp.get('Contents'):
            if do_retry:
                logger.info("Prefix \"%s\" does not seem to have children. "
                            "Retrying once." % prefix)
                do_retry = False
                sleep(0.1)
                continue
            else:
                logger.info("No contents found for \"%s\"." % prefix)
                break

        # Filter by time.
        for entry in resp['Contents']:
            if entry['Key'] != marker:
                if date_cutoff and after and\
                        entry['LastModified'] > date_cutoff\
                        or\
                        date_cutoff and not after and\
                        entry['LastModified'] < date_cutoff\
                        or \
                        date_cutoff is None:
                    yield (entry['Key'], entry['LastModified']) if with_dt \
                        else entry['Key']

        is_truncated = resp['IsTruncated']
        marker = entry['Key']


def rename_s3_prefix(s3, bucket, old_prefix, new_prefix):
    """Change an s3 prefix within the same bucket."""
    to_delete = []
    for key in iter_s3_keys(s3, bucket, old_prefix):
        # Copy the object to the new key (with prefix replaced)
        new_key = key.replace(old_prefix, new_prefix)
        s3.copy_object(Bucket=bucket, Key=new_key,
                       CopySource={'Bucket': bucket, 'Key': key},
                       MetadataDirective='COPY',
                       TaggingDirective='COPY')

        # Keep track of the objects that will need to be deleted (the old keys)
        to_delete.append({'Key': key})

        # Delete objects in maximum batches of 1000.
        if len(to_delete) >= 1000:
            s3.delete_objects(Bucket=bucket,
                              Delete={'Objects': to_delete[:1000]})
            del to_delete[:1000]

    # Get any stragglers.
    s3.delete_objects(Bucket=bucket,
                      Delete={'Objects': to_delete})
    return


def get_s3_file_tree(s3, bucket, prefix, date_cutoff=None, after=True,
                     with_dt=False):
    """Overcome s3 response limit and return NestedDict tree of paths.

    The NestedDict object also allows the user to search by the ends of a path.

    The tree mimics a file directory structure, with the leave nodes being the
    full unbroken key. For example, 'path/to/file.txt' would be retrieved by

        ret['path']['to']['file.txt']['key']

    The NestedDict object returned also has the capability to get paths that
    lead to a certain value. So if you wanted all paths that lead to something
    called 'file.txt', you could use

        ret.get_paths('file.txt')

    For more details, see the NestedDict docs.

    Parameters
    ----------
    s3 : boto3.client.S3
        A boto3.client.S3 instance
    bucket : str
        The name of the bucket to list objects in
    prefix : str
        The prefix filtering of the objects for list
    date_cutoff : str|datetime.datetime
        A datestring of format %Y(-%m-%d-%H-%M-%S) or a datetime.datetime
        object. The date is assumed to be in UTC. By default no filtering
        is done. Default: None.
    after : bool
        If True, only return objects after the given date cutoff.
        Otherwise, return objects before. Default: True
    with_dt : bool
        If True, yield a tuple (key, datetime.datetime(LastModified)) of
        the s3 Key and the object's LastModified date as a
        datetime.datetime object, only yield s3 key otherwise.
        Default: False.

    Returns
    -------
    NestedDict
        A file tree represented as an NestedDict
    """
    file_tree = NestedDict()
    pref_path = prefix.split('/')[:-1]   # avoid the trailing empty str.
    for k in iter_s3_keys(s3, bucket, prefix, date_cutoff, after, with_dt):
        if with_dt:
            key, dt = k
        else:
            key, dt = k, None
        full_path = key.split('/')
        relevant_path = full_path[len(pref_path):]
        curr = file_tree
        for step in relevant_path:
            curr = curr[step]
        curr['key'] = k
    return file_tree


def get_s3_client(unsigned=True):
    """Return a boto3 S3 client with optional unsigned config.

    Parameters
    ----------
    unsigned : Optional[bool]
        If True, the client will be using unsigned mode in which public
        resources can be accessed without credentials. Default: True

    Returns
    -------
    botocore.client.S3
        A client object to AWS S3.
    """
    if unsigned:
        return boto3.client('s3', config=Config(signature_version=UNSIGNED))
    else:
        return boto3.client('s3')


if __name__ == '__main__':
    parser = ArgumentParser(
        'aws.py',
        description=('Use some of INDRA\'s aws tools. For more specific help, '
                     'select one of the Methods with the `-h` option.')
        )
    subparsers = parser.add_subparsers(title='Task')
    subparsers.required = True
    subparsers.dest = 'task'

    # Create parent parser classes for second layer of options
    parent_run_parser = ArgumentParser(add_help=False)
    parent_run_parser.add_argument(
        'command',
        help=('Enter the command as a single string to be run as if in a '
              'batch environment.')
        )
    parent_run_parser.add_argument(
        '--project', '-P',
        default='cwc',
        help='Give a name for the project.'
        )
    parent_run_parser.add_argument(
        '--purpose', '-p',
        help='Give the task some meaning.'
        )
    parent_kill_parser = ArgumentParser(add_help=False)
    parent_kill_parser.add_argument(
        'queue_name',
        help='Select the batch queue in which all jobs should be terminated.'
        )
    parent_kill_parser.add_argument(
        '--reason', '-R',
        help='Give a reason for killing all the jobs.'
        )
    # Make non_db_parser and get subparsers
    run_parser = subparsers.add_parser(
        'run_in_batch',
        parents=[parent_run_parser],
        description=('This should be called to run any command wtihin an aws '
                     'batch job instance.'),
        formatter_class=ArgumentDefaultsHelpFormatter
        )

    # Make db parser and get subparsers.
    kill_parser = subparsers.add_parser(
        'kill_all',
        parents=[parent_kill_parser],
        description='Kill all the jobs running in a given queue.',
        formatter_class=ArgumentDefaultsHelpFormatter
        )
    args = parser.parse_args()

    if args.task == 'run_in_batch':
        ret_code = run_in_batch(args.command.split(), args.project,
                                args.purpose)
        if ret_code is 0:
            logger.info('Job endend well.')
        else:
            logger.error('Job failed!')
            import sys
            sys.exit(ret_code)
    elif args.task == 'kill_all':
        kill_all(args.queue_name, args.reason)
