__all__ = ['process_annotations', 'get_annotations']

import requests
from indra.config import get_config
from .processor import HypothesisProcessor


base_url = 'https://api.hypothes.is/api/'
api_key = get_config('HYPOTHESIS_API_KEY')
headers = {'Authorization': 'Bearer %s' % api_key,
           'Accept': 'application/vnd.hypothesis.v1+json',
           'content-type': 'application/json'}
indra_group = get_config('HYPOTHESIS_GROUP')


def send_request(endpoint, **params):
    """Send a request to the hypothes.is web service and return JSON response.

    Note that it is assumed that `HYPOTHESIS_API_KEY` is set either as a
    configuration entry or as an environmental variable.

    Parameters
    ----------
    endpoint : str
        The endpoint to call, e.g., `search`.
    params : kwargs
        A set of keyword arguments that are passed to the `requests.get` call
        as `params.
    """
    if api_key is None:
        return ValueError('No API key set in HYPOTHESIS_API_KEY')
    res = requests.get(base_url + endpoint, headers=headers,
                       params=params)
    res.raise_for_status()
    return res.json()


def get_annotations(group=None):
    """Return annotations in hypothes.is in a given group.

    Parameters
    ----------
    group : Optional[str]
        The hypothesi.is key of the group (not its name). If not given, the
        HYPOTHESIS_GROUP configuration in the config file or an environmental
        variable is used.
    """
    if group is None:
        if indra_group:
            group = indra_group
        else:
            raise ValueError('No group provided and HYPOTHESIS_GROUP '
                             'is not set.')
    res = send_request('search', group=group, limit=200)
    annotations = res.get('rows', [])
    return annotations


def process_annotations(group=None, reader=None, grounder=None):
    """Process annotations in hypothes.is in a given group.

    Parameters
    ----------
    group : Optional[str]
        The hypothesi.is key of the group (not its name). If not given, the
        HYPOTHESIS_GROUP configuration in the config file or an environmental
        variable is used.
    reader : Optiona[function]
        A handle for a function which takes a single str argument
        (text to process) and returns a processor object with a statements
        attribute containing INDRA Statements. By default, the REACH reader's
        process_text function is used with default parameters. Note that
        if the function requires extra parameters other than the input text,
        functools.partial can be used to set those.
    grounder : Optional[function]
        A handle for a function which takes a positional str argument (entity
        text to ground) and an optional context key word argument and returns
        a list of objects matching the structure of gilda.grounder.ScoredMatch.
        By default, Gilda's ground function is used for grounding.

    Returns
    -------
    HypothesisProcessor
        A HypothesisProcessor object which contains a list of extracted
        INDRA Statements in its statements attribute, and a list of extracted
        grounding curations in its groundings attribute.
    """
    annotations = get_annotations(group=group)
    hp = HypothesisProcessor(annotations, reader=reader, grounder=grounder)
    hp.extract_statements()
    hp.extract_groundings()
    return hp
