import re
import os
import nltk
import zlib
import codecs
import shutil
import logging
from unidecode import unidecode
from indra.literature.pmc_client import extract_text
from indra.resources.greek_alphabet import greek_alphabet

logger = logging.getLogger(__name__)


class IsiPreprocessor(object):
    """Preprocess a set of documents, one by one, and add the preprocessed
    text to a temporary directory in a format suitable for the ISI reader.
    The ISI reader requires plain text with one sentence per line.

    Attributes
    ----------
    preprocessed_dir : str
        The directory holding the literature text preprocessed and sentence
        tokenized in a format suitable for the ISI reader
    next_file_id : int
        The next file with preprocessed text will be named next_file_id.txt
    pmids : dict
        A dictionary mapping file ids to the pmid of the text corresponding
        to that file, can be None if unknown
    extra_annotations : dict
        A dictionary mapping file ids to a (possibly empty) dictionary with
        additional annotations to include for statements extracted from this
        document
    """

    def __init__(self, preprocessed_dir):
        preprocessed_dir = os.path.abspath(preprocessed_dir)
        self.preprocessed_dir = preprocessed_dir
        self.next_file_id = 1
        self.pmids = {}
        self.extra_annotations = {}

        # This directory should be empty
        contents = os.listdir(preprocessed_dir)
        if len(contents) != 0:
            logger.warning('IsiPreprocessor should get an empty directory in' +
                           ' which to store preprocessed files.')

    def register_preprocessed_file(self, infile, pmid, extra_annotations):
        """Set up already preprocessed text file for reading with ISI reader.

        This is essentially a mock function to "register" already preprocessed
        files and get an IsiPreprocessor object that can be passed to
        the IsiProcessor.

        Parameters
        ----------
        infile : str
            Path to an already preprocessed text file (i.e. one ready to
            be sent for reading to ISI reader).
        pmid : str
            The PMID corresponding to the file
        extra_annotations : dict
            Extra annotations to be added to each statement, possibly including
            metadata about the source (annotations with the key "interaction"
            will be overridden)
        """
        infile_base = os.path.basename(infile)
        outfile = os.path.join(self.preprocessed_dir, infile_base)
        shutil.copyfile(infile, outfile)

        infile_key = os.path.splitext(infile_base)[0]

        self.pmids[infile_key] = pmid
        self.extra_annotations[infile_key] = extra_annotations

    def preprocess_plain_text_string(self, text, pmid, extra_annotations):
        """Preprocess plain text string for use by ISI reader.

        Preprocessing is done by tokenizing into sentences and writing
        each sentence on its own line in a plain text file. All other
        preprocessing functions ultimately call this one.

        Parameters
        ----------
        text : str
            The plain text of the article of abstract
        pmid : str
            The PMID from which it comes, or None if not specified
        extra_annotations : dict
            Extra annotations to be added to each statement, possibly including
            metadata about the source (annotations with the key "interaction"
            will be overridden)
        """
        output_file = '%s.txt' % self.next_file_id
        output_file = os.path.join(self.preprocessed_dir, output_file)

        # Replace greek characters with corresponding strings
        for greek_letter, spelled_letter in greek_alphabet.items():
            text = text.replace(greek_letter, spelled_letter)

        # Replace all other unicode characters with nearest ascii equivalents
        text = unidecode(text)

        # Tokenize sentence
        sentences = nltk.sent_tokenize(text)

        # Write sentences to text file
        first_sentence = True
        with codecs.open(output_file, 'w', encoding='utf-8') as f:
            for sentence in sentences:
                if not first_sentence:
                    f.write('\n')
                f.write(sentence.rstrip())
                first_sentence = False

        # Store annotations
        self.pmids[str(self.next_file_id)] = pmid
        self.extra_annotations[str(self.next_file_id)] = extra_annotations

        # Increment file id
        self.next_file_id += 1

    def preprocess_plain_text_file(self, filename, pmid, extra_annotations):
        """Preprocess a plain text file for use with ISI reder.

        Preprocessing results in a new text file with one sentence
        per line.

        Parameters
        ----------
        filename : str
            The name of the plain text file
        pmid : str
            The PMID from which it comes, or None if not specified
        extra_annotations : dict
            Extra annotations to be added to each statement, possibly including
            metadata about the source (annotations with the key "interaction"
            will be overridden)
        """
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            self.preprocess_plain_text_string(content, pmid,
                                              extra_annotations)

    def preprocess_nxml_file(self, filename, pmid, extra_annotations):
        """Preprocess an NXML file for use with the ISI reader.

        Preprocessing is done by extracting plain text from NXML and then
        creating a text file with one sentence per line.

        Parameters
        ----------
        filename : str
            Filename (more specifically the file path) of an nxml file to
            process
        pmid : str
            The PMID from which it comes, or None if not specified
        extra_annotations : dict
            Extra annotations to be added to each statement, possibly including
            metadata about the source (annotations with the key "interaction"
            will be overridden)
        """
        with open(filename, 'r') as fh:
            txt_content = extract_text(fh.read())

        # We need to remove some common LaTEX commands from the converted text
        # or the reader will get confused
        cmd1 = r'[^ \{\}]+\{[^\{\}]+\}\{[^\{\}]+\}'
        cmd2 = r'[^ \{\}]+\{[^\{\}]+\}'
        txt_content = re.sub(cmd1, '', txt_content)
        txt_content = re.sub(cmd2, '', txt_content)

        # Prepocess text extracted from nxml
        self.preprocess_plain_text_string(txt_content, pmid, extra_annotations)

    def preprocess_abstract_list(self, abstract_list):
        """Preprocess abstracts in database pickle dump format for ISI reader.

        For each abstract, creates a plain text file with one sentence per
        line, and stores metadata to be included with each statement from
        that abstract.

        Parameters
        ----------
        abstract_list : list[dict]
            Compressed abstracts with corresopnding metadata in INDRA database
            pickle dump format.
        """
        for abstract_struct in abstract_list:
            abs_format = abstract_struct['format']
            content_type = abstract_struct['text_type']
            content_zipped = abstract_struct['content']
            tcid = abstract_struct['tcid']
            trid = abstract_struct['trid']

            assert(abs_format == 'text')
            assert(content_type == 'abstract')

            pmid = None  # Don't worry about pmid for now
            extra_annotations = {'tcid': tcid, 'trid': trid}

            # Uncompress content
            content = zlib.decompress(content_zipped,
                                      zlib.MAX_WBITS+16).decode('utf-8')

            self.preprocess_plain_text_string(content, pmid, extra_annotations)

    def iter_outputs(self, output_dir):
        """Iterate over the outputs in a given directory using stored metadata.

        For each of the output JSONs, retrieve the extra annotations for that
        file, and link the file with its corresponding PMID.

        Parameters
        ----------
        output_dir : str
            The path to the directory where the JSON outputs were dumped.
        """
        for basename, pmid in self.pmids.items():
            fname = os.path.join(output_dir, '%s.json' % basename)
            extra_annotations = self.extra_annotations.get(fname, {})
            yield fname, pmid, extra_annotations
