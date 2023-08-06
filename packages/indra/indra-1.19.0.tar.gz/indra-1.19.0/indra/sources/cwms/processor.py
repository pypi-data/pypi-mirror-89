import logging
from datetime import datetime
import xml.etree.ElementTree as ET

from indra.statements import *
from indra.statements.statements import Migration
from indra.statements.context import MovementContext
from indra.util import UnicodeXMLTreeBuilder as UTB


logger = logging.getLogger(__name__)


class CWMSError(Exception):
    pass


POLARITY_DICT = {'CC': {'ONT::CAUSE': 1,
                        'ONT::INFLUENCE': 1},
                 'EVENT': {'ONT::INCREASE': 1,
                           'ONT::MODULATE': None,
                           'ONT::DECREASE': -1,
                           'ONT::INHIBIT': -1,
                           'ONT::TRANSFORM': None,
                           'ONT::STIMULATE': 1,
                           'ONT::ARRIVE': None,
                           'ONT::DEPART': None,
                           'ONT::MOVE': None,
                           'ONT::BE': None},
                 'EPI': {'ONT::ASSOCIATE': None}}


class CWMSProcessor(object):
    """The CWMSProcessor currently extracts causal relationships between
    terms (nouns) in EKB. In the future, this processor can be extended to
    extract other types of relations, or to extract relations involving
    events.

    For more details on the TRIPS EKB XML format, see
    http://trips.ihmc.us/parser/cgi/drum

    Parameters
    ----------
    xml_string : str
        A TRIPS extraction knowledge base (EKB) in XML format as a string.

    Attributes
    ----------
    tree : xml.etree.ElementTree.Element
        An ElementTree object representation of the TRIPS EKB XML.
    doc_id: str
        Document ID
    statements : list[indra.statements.Statement]
        A list of INDRA Statements that were extracted from the EKB.
    sentences : dict[str: str]
        The list of all sentences in the EKB with their IDs
    paragraphs : dict[str: str]
        The list of all paragraphs in the EKB with their IDs
    par_to_sec : dict[str: str]
        A map from paragraph IDs to their associated section types
    """

    def __init__(self, xml_string):
        self.statements = []
        # Parse XML
        try:
            self.tree = ET.XML(xml_string, parser=UTB())
        except ET.ParseError:
            logger.error('Could not parse XML string')
            self.tree = None
            return

        # Get the document ID from the EKB tag.
        self.doc_id = self.tree.attrib.get('id')

        # Store all paragraphs and store all sentences in a data structure
        paragraph_tags = self.tree.findall('input/paragraphs/paragraph')
        sentence_tags = self.tree.findall('input/sentences/sentence')
        self.paragraphs = {p.attrib['id']: p.text for p in paragraph_tags}
        self.sentences = {s.attrib['id']: s.text for s in sentence_tags}
        self.par_to_sec = {p.attrib['id']: p.attrib.get('sec-type')
                           for p in paragraph_tags}

        # Keep a list of events that are part of relations and events
        # subsumed by other events
        self.relation_events = set()
        self.subsumed_events = set()

        # Keep a list of unhandled events for development purposes
        self._unhandled_events = set()

        self._preprocess_events()

    def _preprocess_events(self):
        events = self.tree.findall("EVENT/[type]")
        for event in events:
            affected = event.find("*[@role=':AFFECTED']")
            if affected is not None:
                affected_id = affected.attrib.get('id')
                if affected_id:
                    self.subsumed_events.add(affected_id)

    def extract_causal_relations(self):
        """Extract Influence Statements from the EKB."""
        relations = self.tree.findall("CC/[type]")
        for relation in relations:
            st = self.influence_from_relation(relation)
            if st:
                self.statements.append(st)

        events = self.tree.findall("EVENT/[type]")
        for event in events:
            st = self.influence_from_event(event)
            if st:
                self.statements.append(st)
        # In some EKBs we get two redundant relations over the same arguments,
        # we eliminate these
        self._remove_multi_extraction_artifacts()

        # Print unhandled event types
        logger.debug('Unhandled event types: %s' %
                     (', '.join(sorted(self._unhandled_events))))

    def extract_events(self):
        """Extract standalone Events from the EKB."""
        events = [(1, self.tree.findall("EVENT/[type='ONT::INCREASE']")),
                  (-1, self.tree.findall("EVENT/[type='ONT::DECREASE']"))]
        for polarity, event_list in events:
            for event_term in event_list:
                event_id = event_term.attrib.get('id')
                if event_id in self.subsumed_events or \
                        event_id in self.relation_events:
                    continue
                event = self.event_from_event(event_term)
                if event:
                    # Here we set the polarity based on the polarity implied by
                    # the increase/decrease here
                    event.delta.set_polarity(polarity)
                    self.statements.append(event)

        self._remove_multi_extraction_artifacts()

    def extract_migrations(self, include_relation_arg=False):
        ev_types = ['ONT::MOVE', 'ONT::DEPART', 'ONT::ARRIVE']
        events = []
        for et in ev_types:
            evs = self.tree.findall("EVENT/[type='%s']" % et)
            events += evs

        for event_term in events:
            event_id = event_term.attrib.get('id')
            if event_id in self.subsumed_events or \
                    (not include_relation_arg and
                     event_id in self.relation_events):
                continue
            event = self.migration_from_event(event_term)
            if event is not None:
                self.statements.append(event)
        self._remove_multi_extraction_artifacts()

    def extract_correlations(self):
        correlations = self.tree.findall("EPI/[type='ONT::ASSOCIATE']")
        for cor in correlations:
            st = self._association_from_element(cor, 'EPI', 'NEUTRAL1',
                                                'NEUTRAL2', False)
            if st:
                self.statements.append(st)

        # self._remove_multi_extraction_artifacts()

    def _influence_from_element(self, element, element_type, subj_arg,
                                obj_arg, is_arg):
        components = self._statement_components_from_element(
            element, element_type, subj_arg, obj_arg, is_arg)
        if components is None:
            return None
        subj, obj, evidence, rel_type = components
        # If the object polarity is not given explicitly, we set it
        # based on the one implied by the relation
        if obj.delta.polarity is None:
            obj.delta.set_polarity(POLARITY_DICT[element_type][rel_type])

        st = Influence(subj, obj, evidence=[evidence])
        return st

    def influence_from_relation(self, relation):
        """Return an Influence from a CC element in the EKB."""
        return self._influence_from_element(relation, 'CC', 'FACTOR',
                                            'OUTCOME', True)

    def influence_from_event(self, event):
        """Return an Influence from an EVENT element in the EKB."""
        return self._influence_from_element(event, 'EVENT', 'AGENT',
                                            'AFFECTED', False)

    def _statement_components_from_element(self, element, element_type,
                                           member1_arg, member2_arg, is_arg):
        element_id = element.attrib.get('id')
        rel_type = element.find('type').text
        if rel_type not in POLARITY_DICT[element_type]:
            self._unhandled_events.add(rel_type)
            return None
        member1_id, member1_term = self._get_term_by_role(
            element, member1_arg, is_arg)
        member2_id, member2_term = self._get_term_by_role(
            element, member2_arg, is_arg)
        if member1_term is None or member2_term is None:
            return None

        member1 = self.get_event_or_migration(member1_term)
        member2 = self.get_event_or_migration(member2_term)
        if member1 is None or member2 is None:
            return None

        self.relation_events |= {member1_id, member2_id, element_id}

        evidence = self._get_evidence(element)

        return member1, member2, evidence, rel_type

    def _association_from_element(self, element, element_type, member1_arg,
                                  member2_arg, is_arg):
        components = self._statement_components_from_element(
            element, element_type, member1_arg, member2_arg, is_arg)
        if components is None:
            return None
        member1, member2, evidence, _ = components
        st = Association([member1, member2], evidence=[evidence])
        return st

    def event_from_event(self, event_term):
        """Return an Event from an EVENT element in the EKB."""
        arg_id, arg_term = self._get_term_by_role(event_term, 'AFFECTED',
                                                  False)
        if arg_term is None:
            return None
        # Make an Event statement if it is a standalone event
        evidence = self._get_evidence(event_term)
        event = self._get_event(arg_term, evidence=[evidence])
        if event is None:
            return None
        event.context = self.get_context(event_term)
        return event

    def migration_from_event(self, event_term):
        """Return a Migration event from an EVENT element in the EKB."""
        # First process at event level
        migration_grounding = ('wm/concept/causal_factor/'
                               'social_and_political/migration')
        concept_name = 'migration'
        concept_db_refs = {'WM': migration_grounding}
        # Get the element's text and use it to construct a Concept
        element_text_element = event_term.find('text')
        if element_text_element is not None:
            element_text = element_text_element.text
            concept_db_refs['TEXT'] = element_text
            concept_name = sanitize_name(element_text)
        concept = Concept(concept_name, db_refs=concept_db_refs)
        evidence = self._get_evidence(event_term)
        time = self._extract_time(event_term)
        # Locations can be at different levels, keep expanding the list
        locs = self._get_migration_locations(event_term)
        neutral_id, neutral_term = self._get_term_by_role(event_term,
                                                          'NEUTRAL',
                                                          is_arg=False)
        if neutral_term is not None:
            locs = self._get_migration_locations(neutral_term, locs, 'origin')
        # Arguments can be under AGENT or AFFECTED
        agent_arg_id, agent_arg_term = self._get_term_by_role(
            event_term, 'AGENT', False)
        affected_arg_id, affected_arg_term = self._get_term_by_role(
            event_term, 'AFFECTED', False)
        if agent_arg_term is None and affected_arg_term is None:
            context = MovementContext(locations=locs, time=time)
            event = Migration(concept, context=context, evidence=[evidence])
            return event

        # If there are argument terms, extract more data from them
        # Try to get the quantitative state associated with the event
        size = None
        for arg_term in [agent_arg_term, affected_arg_term]:
            if arg_term is not None:
                size_arg = arg_term.find('size')
                if size_arg is not None and size_arg.attrib.get('id'):
                    size = self._get_size(size_arg.attrib['id'])
                    break
        # Get more locations from arguments and inevents
        if agent_arg_term is not None:
            locs = self._get_migration_locations(
                agent_arg_term, locs, 'destination')
            inevent_term = self._get_inevent_term(agent_arg_term)
            if inevent_term is not None:
                locs = self._get_migration_locations(inevent_term, locs)
                if time is None:
                    time = self._extract_time(inevent_term)
                if size is None:
                    size = self._get_size_and_entity(inevent_term)
            other_event_term = self._get_other_event_term(agent_arg_term)
            if other_event_term is not None:
                locs = self._get_migration_locations(other_event_term, locs)
                if time is None:
                    time = self._extract_time(other_event_term)
                if size is None:
                    size = self._get_size_and_entity(other_event_term)
        if affected_arg_term is not None:
            locs = self._get_migration_locations(
                affected_arg_term, locs, 'destination')
        context = MovementContext(locations=locs, time=time)
        event = Migration(
            concept, delta=size, context=context, evidence=[evidence])
        return event

    def _get_inevent_term(self, arg_term):
        refset_arg = arg_term.find('refset')
        if refset_arg is None:
            return None
        refset_id = refset_arg.attrib['id']
        refset_term = self.tree.find("*[@id='%s']" % refset_id)
        if refset_term is None:
            return None
        features = refset_term.find('features')
        if features is None:
            return None
        inevent = features.find('inevent')
        if inevent is None:
            return None
        inevent_id = inevent.attrib['id']
        self.subsumed_events.add(inevent_id)
        inevent_term = self.tree.find("*[@id='%s']" % inevent_id)
        return inevent_term

    def _get_other_event_term(self, arg_term):
        refset_arg = arg_term.find('refset')
        potential_events = self.tree.findall("EVENT/[type].//arg1/..") + \
            self.tree.findall("EVENT/[type].//arg2/..")
        for ev in potential_events:
            arg1 = ev.find('arg1')
            arg2 = ev.find('arg2')
            for arg in [arg1, arg2]:
                if arg is not None:
                    if refset_arg is not None:
                        if arg.attrib.get('id') == refset_arg.attrib.get('id'):
                            event_id = ev.attrib['id']
                            self.subsumed_events.add(event_id)
                            event_term = self.tree.find("*[@id='%s']"
                                                        % event_id)
                            return event_term
                    else:
                        # Refset might be on a different level
                        if arg.attrib.get('id'):
                            term = self.tree.find("*[@id='%s']" % arg.attrib['id'])
                            arg_refset_arg = term.find('refset')
                            if arg_refset_arg is not None:
                                if arg_refset_arg.attrib.get('id') == \
                                        arg_term.attrib.get('id'):
                                    event_id = ev.attrib['id']
                                    self.subsumed_events.add(event_id)
                                    event_term = self.tree.find("*[@id='%s']"
                                                                % event_id)
                                    return event_term
        return None

    def _get_arg_event_term(self, term):
        potential_args = term.findall('arg1') + term.findall('arg2')
        for arg in potential_args:
            if arg.attrib.get('id'):
                new_term = self.tree.find("*[@id='%s']" % arg.attrib['id'])
                if new_term is not None:
                    self.subsumed_events.add(new_term.attrib['id'])
                    return new_term

    def _get_migration_locations(self, event_term, existing_locs=None,
                                 default_role='unknown'):
        if existing_locs is None:
            existing_locs = []
        new_locs = []

        loc = self._extract_geoloc(event_term, arg_link='location')
        if loc is not None:
            new_locs.append({'location': loc,
                             'role': default_role})

        loc = self._extract_geoloc(event_term, arg_link='to-location')
        if loc is not None:
            new_locs.append({'location': loc,
                             'role': 'destination'})

        loc = self._extract_geoloc(event_term, arg_link='from-location')
        if loc is not None:
            new_locs.append({'location': loc,
                             'role': 'origin'})
        for loc in new_locs:
            if loc not in existing_locs:
                existing_locs.append(loc)
        return existing_locs

    def _get_size(self, size_term_id):
        size_term = self.tree.find("*[@id='%s']" % size_term_id)
        value = size_term.find('value')
        if value is None:
            value = size_term.find('amount')
        if value is not None:
            mod = value.attrib.get('mod')
            if mod and mod.lower() == 'almost':
                mod = 'less_than'
            value_txt = value.text
            if value_txt is not None:
                value_str = value.text.strip()
                if value_str and not value_str.startswith('ONT') and \
                        not value_str.startswith('W'):
                    value = int(float(value_str))
                else:
                    value = None
            else:
                value = None
            unit = size_term.find('unit')
            if unit is not None:
                unit = unit.text.strip().lower()
            else:
                unit = 'absolute'
            text = size_term.find('text').text
            size = QuantitativeState(entity='person', value=value, unit=unit,
                                     modifier=mod, text=text)
        else:
            size = None
        return size

    def _get_size_and_entity(self, event_term):
        # For cases when entity (group) information and quantity are stored in
        # different arguments and we can overwrite default 'person' entity
        _, term1 = self._get_term_by_role(event_term, 'NEUTRAL', False)
        _, term2 = self._get_term_by_role(event_term, 'NEUTRAL1', False)
        size = None
        if term1 is not None:
            size_arg = term1.find('size')
            if size_arg is not None and size_arg.attrib.get('id'):
                size = self._get_size(size_arg.attrib['id'])
        if size is not None and term2 is not None:
            size.entity = term2.find('text').text
        return size

    def _get_term_by_role(self, term, role, is_arg):
        """Return the ID and the element corresponding to a role in a term."""
        element = term.find("%s[@role=':%s']" % ('arg/' if is_arg else '*',
                                                 role))
        if element is None:
            return None, None
        element_id = element.attrib.get('id')
        if element_id is None:
            return None, None
        element_term = self.tree.find("*[@id='%s']" % element_id)
        if element_term is None:
            return None, None
        return element_id, element_term

    def _get_event(self, event_term, evidence=None):
        """Extract and Event from the given EKB element."""
        # Now see if there is a modifier like assoc-with connected
        # to the main concept
        assoc_with = self._get_assoc_with_text(event_term)

        # Get the element's text and use it to construct a Concept
        element_text_element = event_term.find('text')
        if element_text_element is None:
            return None
        element_text = element_text_element.text
        if element_text is None:
            return None
        element_db_refs = {'TEXT': element_text.rstrip()}
        element_name = sanitize_name(element_text.rstrip())

        element_type_element = event_term.find('type')
        if element_type_element is not None:
            element_db_refs['CWMS'] = element_type_element.text
            # If there's an assoc-with, we tack it on as extra grounding
            if assoc_with is not None:
                element_db_refs['CWMS'] += ('|%s' % assoc_with)

        concept = Concept(element_name, db_refs=element_db_refs)

        ev_type = event_term.find('type').text
        polarity = POLARITY_DICT['EVENT'].get(ev_type)
        delta = QualitativeDelta(polarity=polarity)
        context = self.get_context(event_term)
        event_obj = Event(concept, delta=delta, context=context,
                          evidence=evidence)
        return event_obj

    def _get_wm_grounding(self, element):
        wm_gr = None
        wm_type_element = element.find('wm-type')
        if wm_type_element is not None:
            grounding_element = wm_type_element.find('grounding')
            if grounding_element is not None:
                wm_gr = (grounding_element.text, 0.7)
        return wm_gr

    def _add_start_end(self, term, starts, ends):
        start = term.attrib.get('start')
        end = term.attrib.get('end')
        if start:
            starts.append(int(start))
        if end:
            ends.append(int(end))
        return starts, ends

    def get_event_or_migration(self, event_term):
        #if event_term.find('type').text in [
        #   'ONT::MOVE', 'ONT::DEPART', 'ONT::ARRIVE']:
        #        return self.migration_from_event(event_term)
        #else:
        return self._get_event(event_term)

    def get_context(self, element):
        time = self._extract_time(element)
        geoloc = self._extract_geoloc(element)

        if time or geoloc:
            context = WorldContext(time=time, geo_location=geoloc)
        else:
            context = None
        return context

    def _extract_time(self, term):
        time = term.find('time')
        if time is None:
            time = term.find('features/time')
            if time is None:
                return None
        time_id = time.attrib.get('id')
        time_term = self.tree.find("*[@id='%s']" % time_id)
        if time_term is None:
            return None
        text = sanitize_name(time_term.findtext('text'))
        timex = time_term.find('timex')
        if timex is not None:
            start = self._process_timex(timex)
            if start is not None:
                time_context = TimeContext(text=text, start=start)
            else:
                time_context = TimeContext(text=text)
        else:
            start = None
            end = None
            from_time_el = time_term.find('from-time')
            to_time_el = time_term.find('to-time')
            if from_time_el is not None:
                from_time_id = from_time_el.attrib.get('id')
                from_time_term = self.tree.find("*[@id='%s']" % from_time_id)
                if time_term is not None:
                    timex = from_time_term.find('timex')
                    if timex is not None:
                        start = self._process_timex(timex)
            if to_time_el is not None:
                to_time_id = to_time_el.attrib.get('id')
                to_time_term = self.tree.find("*[@id='%s']" % to_time_id)
                if to_time_term is not None:
                    timex = to_time_term.find('timex')
                    if timex is not None:
                        end = self._process_timex(timex)
            if start and end:
                duration = int((end - start).total_seconds())
            else:
                duration = None
            time_context = TimeContext(
                text=text, start=start, end=end, duration=duration)
        return time_context

    @staticmethod
    def _process_timex(timex):
        year = timex.findtext('year')
        month = timex.findtext('month')
        day = timex.findtext('day')
        if year or month or day:
            try:
                year = int(year)
            except Exception:
                year = None
            try:
                # Month can be represented either by name, short name or
                # number (October, Oct or 10)
                month = int(month)
            except Exception:
                try:
                    month = datetime.strptime(month, '%B').month
                except Exception:
                    try:
                        month = datetime.strptime(month, '%b').month
                    except Exception:
                        month = 1
            try:
                day = int(day)
            except Exception:
                day = 1
            if year and month and day:
                time = datetime(year, month, day)
                return time
        return None

    def _extract_geoloc(self, term, arg_link='location'):
        """Get the location from a term (CC or TERM)"""
        loc = term.find(arg_link)
        if loc is None:
            return None
        loc_id = loc.attrib.get('id')
        loc_term = self.tree.find("*[@id='%s']" % loc_id)
        if loc_term is None:
            return None
        text = loc_term.findtext('text')
        grounding = loc_term.find('grounding')
        db_refs = {}
        if grounding is not None:
            places = grounding.findall('place')
            for place in places:
                nsid = place.attrib.get('id')
                db_ns, db_id = nsid.split(':')
                if db_ns == 'GNO':
                    db_ns = 'GEOID'
                # TODO: name spaces are sometimes repeated in the EKB, here we
                #  silently overwrite a key if it already exists
                db_refs[db_ns] = db_id
        # name = loc_term.findtext('name')
        geoloc_context = RefContext(name=text, db_refs=db_refs)
        return geoloc_context

    def _get_assoc_with_text(self, element_term):
        # NOTE: there could be multiple assoc-withs here that we may
        # want to handle
        assoc_with = element_term.find('assoc-with')
        if assoc_with is not None:
            # We first identify the ID of the assoc-with argument
            assoc_with_id = assoc_with.attrib.get('id')
            # In some cases the assoc-with has no ID but has a type
            # defined in place that we can get
            if assoc_with_id is None:
                assoc_with_grounding = assoc_with.find('type').text
                return assoc_with_grounding
            # If the assoc-with has an ID then find the TERM
            # corresponding to it
            assoc_with_term = self.tree.find("*[@id='%s']" % assoc_with_id)
            if assoc_with_term is not None:
                # We then get the grounding for the term
                assoc_with_grounding = assoc_with_term.find('type').text
                return assoc_with_grounding
        return None

    def _get_assoc_with_term(self, element_term):
        assoc_with = element_term.find('assoc-with')
        if assoc_with is not None:
            assoc_with_id = assoc_with.attrib.get('id')
            if assoc_with_id is not None:
                assoc_with_term = self.tree.find("*[@id='%s']" % assoc_with_id)
                return assoc_with_term

    def _get_evidence(self, event_tag):
        text = self._get_evidence_text(event_tag)
        sec = self._get_section(event_tag)
        epi = {'direct': False}
        if sec:
            epi['section_type'] = sec
        ev = Evidence(source_api='cwms', text=text, pmid=self.doc_id,
                      epistemics=epi)
        return ev

    def _get_evidence_text(self, event_tag):
        """Extract the evidence for an event.

        Pieces of text linked to an EVENT are fragments of a sentence. The
        EVENT refers to the paragraph ID and the "uttnum", which corresponds
        to a sentence ID. Here we find and return the full sentence from which
        the event was taken.
        """
        par_id = event_tag.attrib.get('paragraph')
        uttnum = event_tag.attrib.get('uttnum')
        event_text = event_tag.find('text')
        if self.sentences is not None and uttnum is not None:
            sentence = self.sentences[uttnum]
        elif event_text is not None:
            sentence = event_text.text
        else:
            sentence = None
        return sentence

    def _get_section(self, event_tag):
        par_id = event_tag.attrib.get('paragraph')
        sec = self.par_to_sec.get(par_id)
        return sec

    def _remove_multi_extraction_artifacts(self):
        # Build up a dict of evidence matches keys with statement UUIDs
        evmks = {}
        logger.debug('Starting with %d Statements.' % len(self.statements))
        for stmt in self.statements:
            if isinstance(stmt, Event):
                evmk = stmt.evidence[0].matches_key() + \
                    stmt.concept.matches_key()
            elif isinstance(stmt, Influence):
                evmk = (stmt.evidence[0].matches_key() +
                        stmt.subj.matches_key() + stmt.obj.matches_key())
            elif isinstance(stmt, Association):
                evmk = (stmt.evidence[0].matches_key() +
                        stmt.members[0].matches_key() +
                        stmt.members[1].matches_key())
            if evmk not in evmks:
                evmks[evmk] = [stmt.uuid]
            else:
                evmks[evmk].append(stmt.uuid)
        # This is a list of groups of statement UUIDs that are redundant
        multi_evmks = [v for k, v in evmks.items() if len(v) > 1]
        # We now figure out if anything needs to be removed
        to_remove = []
        # Remove redundant statements
        for uuids in multi_evmks:
            # Influence statements to be removed
            infl_stmts = [s for s in self.statements if (
                            s.uuid in uuids and isinstance(s, Influence))]
            infl_stmts = sorted(infl_stmts, key=lambda x: x.polarity_count(),
                                reverse=True)
            to_remove += [s.uuid for s in infl_stmts[1:]]
            # Association statements to be removed
            assn_stmts = [s for s in self.statements if (
                            s.uuid in uuids and isinstance(s, Association))]
            assn_stmts = sorted(assn_stmts, key=lambda x: x.polarity_count(),
                                reverse=True)
            # Standalone events to be removed
            events = [s for s in self.statements if (
                        s.uuid in uuids and isinstance(s, Event))]
            events = sorted(events, key=lambda x: event_delta_score(x),
                            reverse=True)
            to_remove += [e.uuid for e in events[1:]]

        # Remove all redundant statements
        if to_remove:
            logger.debug('Found %d Statements to remove' % len(to_remove))
        self.statements = [s for s in self.statements
                           if s.uuid not in to_remove]


class CWMSProcessorCompositional(CWMSProcessor):
    def _get_event(self, event_term, evidence=None):
        """Extract and Event from the given EKB element."""
        # Now see if there is a modifier like assoc-with connected
        # to the main concept
        assoc_with = self._get_assoc_with_text(event_term)

        # We're using a union of texts from multiple terms instead
        # Get the element's text and use it to construct a Concept

        # element_text_element = event_term.find('text')
        # if element_text_element is None:
        #     return None
        # element_text = element_text_element.text
        # element_db_refs = {'TEXT': element_text}
        # element_name = sanitize_name(element_text)

        element_db_refs = {}
        par = event_term.attrib['paragraph']
        starts, ends = self._add_start_end(event_term, [], [])

        element_type_element = event_term.find('type')
        if element_type_element is not None:
            element_db_refs['CWMS'] = element_type_element.text
            # If there's an assoc-with, we tack it on as extra grounding
            if assoc_with is not None:
                element_db_refs['CWMS'] += ('|%s' % assoc_with)

        theme_gr, theme_prop_gr, theme_proc_gr, theme_proc_prop_gr = \
            None, None, None, None
        # Grounding can be provided on multiple levels
        theme_gr = self._get_wm_grounding(event_term)
        if not theme_gr:
            arg_term = self._get_arg_event_term(event_term)
            if arg_term is not None:
                starts, ends = self._add_start_end(arg_term, starts, ends)
                assoc_term = self._get_assoc_with_term(arg_term)
                if assoc_term is not None:
                    starts, ends = self._add_start_end(
                        assoc_term, starts, ends)
                    new_arg_term = self._get_arg_event_term(assoc_term)
                    # Theme grounding is usually at the "deepest" level
                    if new_arg_term is not None:
                        starts, ends = self._add_start_end(
                            new_arg_term, starts, ends)
                        theme_gr = self._get_wm_grounding(new_arg_term)
                        theme_proc_gr = self._get_wm_grounding(assoc_term)
                        theme_proc_prop_gr = self._get_wm_grounding(arg_term)
                    else:
                        theme_gr = self._get_wm_grounding(assoc_term)
                        extra_gr = self._get_wm_grounding(arg_term)
                        # This can be process or property, look at ontology
                        if extra_gr:
                            if 'process' in extra_gr[0]:
                                theme_proc_gr = extra_gr
                            else:
                                theme_prop_gr = extra_gr

        # Get a union of all texts
        element_text = self.paragraphs[par][min(starts): max(ends)].rstrip()
        element_db_refs['TEXT'] = element_text
        element_name = sanitize_name(element_text)

        # Promote process grounding to theme if theme is missing
        if not theme_gr and theme_proc_gr:
            theme_gr = theme_proc_gr
            theme_proc_gr = None
        # Drop process property grounding in process is missing
        if not theme_proc_gr:
            theme_proc_prop_gr = None

        # Only add WM grounding if there's a theme grounding
        if theme_gr:
            element_db_refs['WM'] = [(theme_gr, theme_prop_gr, theme_proc_gr,
                                      theme_proc_prop_gr)]
        concept = Concept(element_name, db_refs=element_db_refs)

        ev_type = event_term.find('type').text
        polarity = POLARITY_DICT['EVENT'].get(ev_type)
        delta = QualitativeDelta(polarity=polarity)
        context = self.get_context(event_term)
        event_obj = Event(concept, delta=delta, context=context,
                          evidence=evidence)
        return event_obj


def sanitize_name(txt):
    name = txt.replace('\n', '')
    return name


def event_delta_score(stmt):
    if stmt.delta is None:
        return 0
    pol_score = 1 if stmt.delta.polarity is not None else 0
    if isinstance(stmt.delta, QualitativeDelta):
        adj_score = len(stmt.delta.adjectives)
        return (pol_score + adj_score)
    if isinstance(stmt.delta, QuantitativeState):
        value_score = 1 if stmt.delta.value is not None else 0
        return (pol_score + value_score)
