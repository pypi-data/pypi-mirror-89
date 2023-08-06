import os
import json
import datetime
from indra import get_config


# Before the import, we have to deal with the CLASSPATH to avoid clashes
# with REACH.
def _set_classpath():
    clp = os.environ.get('CLASSPATH')
    eip = get_config('EIDOSPATH')
    rep = get_config('REACHPATH')
    clp_parts = clp.split(':') if clp else []
    new_clp_parts = []
    has_eidos = False
    # Look at all the parts of the CLASSPATH
    for part in clp_parts:
        # If REACH is on the CLASSPATH, remove it
        if not rep or os.path.abspath(part) != rep:
            new_clp_parts.append(part)
        # If Eidos is not on the CLASSPATH, add it
        if eip and os.path.abspath(part) == eip:
            has_eidos = True
    if eip and not has_eidos:
        new_clp_parts.append(eip)
    # Set the new CLASSPATH
    new_clp = ':'.join(new_clp_parts)
    os.environ['CLASSPATH'] = new_clp
_set_classpath()

from indra.java_vm import autoclass


eidos_package = 'org.clulab.wm.eidos'


class EidosReader(object):
    """Reader object keeping an instance of the Eidos reader as a singleton.

    This allows the Eidos reader to need initialization when the first piece of
    text is read, the subsequent readings are done with the same
    instance of the reader and are therefore faster.

    Attributes
    ----------
    eidos_reader : org.clulab.wm.eidos.EidosSystem
        A Scala object, an instance of the Eidos reading system. It is
        instantiated only when first processing text.
    """

    def __init__(self):
        self.eidos_reader = None
        self.default_ontology = None

    def get_default_ontology(self):
        if self.default_ontology is None:
            from indra.ontology.world import world_ontology
            self.default_ontology = world_ontology.dump_yml_str()
        return self.default_ontology

    def initialize_reader(self):
        """Instantiate the Eidos reader attribute of this reader."""
        eidos = autoclass(eidos_package + '.EidosSystem')
        self.eidos_reader = eidos()

    def reground_texts(self, texts, yaml_str=None, topk=10,
                       is_canonicalized=False, filter=True):
        if self.eidos_reader is None:
            self.initialize_reader()
        if yaml_str is None:
            yaml_str = self.get_default_ontology()
        text_seq = _list_to_seq(texts)
        raw_groundings = \
            self.eidos_reader.components().ontologyHandler().reground(
                'Custom',  # name
                yaml_str,  # ontologyYaml
                text_seq,  # texts
                filter,  # filter
                topk,  # topk
                is_canonicalized  # isAlreadyCanonicalized
            )
        # Process the return values into a proper Python representation
        groundings = [[_get_scored_grounding(entry) for entry in text_grounding]
                      for text_grounding in raw_groundings]
        return groundings

    def process_text(self, text):
        """Return a mentions JSON object given text.

        Parameters
        ----------
        text : str
            Text to be processed.

        Returns
        -------
        json_dict : dict
            A JSON object of mentions extracted from text.
        """
        if self.eidos_reader is None:
            self.initialize_reader()
        default_arg = lambda x: autoclass('scala.Some')(x)
        today = datetime.date.today().strftime("%Y-%m-%d")
        fname = 'default_file_name'

        annot_doc = self.eidos_reader.extractFromText(
            text,
            False,  # CAG-relevant only
            default_arg(today),  # doc creation time
            default_arg(fname)  # file name
            )
        # We need to get a Scala Seq of annot docs here
        ml = _list_to_seq([annot_doc])
        # We currently do not need toinstantiate the adjective grounder
        # if we want to reinstate it, we would need to do the following
        # ag = EidosAdjectiveGrounder.fromConfig(
        #   EidosSystem.defaultConfig.getConfig("adjectiveGrounder"))
        # We now create a JSON-LD corpus
        jc = autoclass(eidos_package + '.serialization.json.JLDCorpus')
        corpus = jc(ml)
        # Finally, serialize the corpus into JSON string
        mentions_json = corpus.toJsonStr()
        json_dict = json.loads(mentions_json)
        return json_dict


def _list_to_seq(lst):
    """Return a scala.collection.Seq from a Python list."""
    ml = autoclass('scala.collection.mutable.MutableList')()
    for element in lst:
        ml.appendElem(element)
    return ml


def _get_scored_grounding(tpl):
    ts = tpl.toString()
    parts = ts[1:-1].rsplit(',', maxsplit=1)
    return parts[0], float(parts[1])
