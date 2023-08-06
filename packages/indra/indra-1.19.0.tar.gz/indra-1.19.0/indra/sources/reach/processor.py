import os
import re
import logging
import objectpath
from collections import defaultdict

from indra.statements import *
from indra.util import read_unicode_csv
from indra.databases import go_client, uniprot_client
from indra.ontology.standardize import \
    standardize_db_refs, standardize_agent_name, \
    standardize_name_db_refs
from indra.statements.validate import validate_text_refs
from collections import namedtuple

logger = logging.getLogger(__name__)

Site = namedtuple('Site', ['residue', 'position'])


class ReachProcessor(object):
    """The ReachProcessor extracts INDRA Statements from REACH parser output.

    Parameters
    ----------
    json_dict : dict
        A JSON dictionary containing the REACH extractions.
    pmid : Optional[str]
        The PubMed ID associated with the extractions. This can be passed
        in case the PMID cannot be determined from the extractions alone.`

    Attributes
    ----------
    tree : objectpath.Tree
        The objectpath Tree object representing the extractions.
    statements : list[indra.statements.Statement]
        A list of INDRA Statements that were extracted by the processor.
    citation : str
        The PubMed ID associated with the extractions.
    all_events : dict[str, str]
        The frame IDs of all events by type in the REACH extraction.
    organism_priority : list[str]
        A list of Taxonomy IDs providing prioritization among organisms
        when choosing protein grounding. If not given, the default behavior
        takes the first match produced by Reach, which is prioritized to be
        a human protein if such a match exists.
    """
    def __init__(self, json_dict, pmid=None, organism_priority=None):
        self.tree = objectpath.Tree(json_dict)
        self.organism_priority = organism_priority
        self.statements = []
        self.citation = pmid
        if pmid is None:
            if self.tree is not None:
                self.citation =\
                    self.tree.execute("$.events.object_meta.doc_id")
                if not validate_text_refs({'PMID': self.citation}):
                    logger.debug('The citation added is not a valid '
                                 'PMID, removing.')
                    self.citation = None
        self.get_all_events()

    def print_event_statistics(self):
        """Print the number of events in the REACH output by type."""
        logger.info('All events by type')
        logger.info('-------------------')
        for k, v in self.all_events.items():
            logger.info('%s, %s' % (k, len(v)))
        logger.info('-------------------')

    def get_all_events(self):
        """Gather all event IDs in the REACH output by type.

        These IDs are stored in the self.all_events dict.
        """
        self.all_events = {}
        events = self.tree.execute("$.events.frames")
        if events is None:
            return
        for e in events:
            event_type = e.get('type')
            frame_id = e.get('frame_id')
            try:
                self.all_events[event_type].append(frame_id)
            except KeyError:
                self.all_events[event_type] = [frame_id]

    def print_regulations(self):
        qstr = "$.events.frames[(@.type is 'regulation')]"
        res = self.tree.execute(qstr)
        if res is None:
            return
        for r in res:
            print(r['subtype'])
            for a in r['arguments']:
                print(a['type'], '/', a['argument-type'], ':', a['text'])

    def get_modifications(self):
        """Extract Modification INDRA Statements."""
        # Find all event frames that are a type of protein modification
        qstr = "$.events.frames[(@.type is 'protein-modification')]"
        res = self.tree.execute(qstr)
        if res is None:
            return
        # Extract each of the results when possible
        for r in res:
            # The subtype of the modification
            modification_type = r.get('subtype')

            # Skip negated events (i.e. something doesn't happen)
            epistemics = self._get_epistemics(r)
            if epistemics.get('negated'):
                continue

            annotations, context = self._get_annot_context(r)
            frame_id = r['frame_id']
            args = r['arguments']
            site = None
            theme = None

            # Find the substrate (the "theme" agent here) and the
            # site and position it is modified on
            for a in args:
                if self._get_arg_type(a) == 'theme':
                    theme = a['arg']
                elif self._get_arg_type(a) == 'site':
                    site = a['text']
            theme_agent, theme_coords = self._get_agent_from_entity(theme)
            if site is not None:
                mods = self._parse_site_text(site)
            else:
                mods = [(None, None)]

            for mod in mods:
                # Add up to one statement for each site
                residue, pos = mod

                # Now we need to look for all regulation event to get to the
                # enzymes (the "controller" here)
                qstr = "$.events.frames[(@.type is 'regulation') and " + \
                       "(@.arguments[0].arg is '%s')]" % frame_id
                reg_res = self.tree.execute(qstr)
                reg_res = list(reg_res)
                for reg in reg_res:
                    controller_agent, controller_coords = None, None
                    for a in reg['arguments']:
                        if self._get_arg_type(a) == 'controller':
                            controller = a.get('arg')
                            if controller is not None:
                                controller_agent, controller_coords = \
                                    self._get_agent_from_entity(controller)
                                break
                    # Check the polarity of the regulation and if negative,
                    # flip the modification type.
                    # For instance, negative-regulation of a phosphorylation
                    # will become an (indirect) dephosphorylation
                    reg_subtype = reg.get('subtype')
                    if reg_subtype == 'negative-regulation':
                        modification_type = \
                            modtype_to_inverse.get(modification_type)
                        if not modification_type:
                            logger.warning('Unhandled modification type: %s' %
                                           modification_type)
                            continue 

                    sentence = reg['verbose-text']
                    annotations['agents']['coords'] = [controller_coords,
                                                       theme_coords]
                    ev = Evidence(source_api='reach', text=sentence,
                                  annotations=annotations, pmid=self.citation,
                                  context=context, epistemics=epistemics)
                    args = [controller_agent, theme_agent, residue, pos, ev]

                    # Here ModStmt is a sub-class of Modification
                    ModStmt = modtype_to_modclass.get(modification_type)
                    if ModStmt is None:
                        logger.warning('Unhandled modification type: %s' %
                                       modification_type)
                    else:
                        # Handle this special case here because only
                        # enzyme argument is needed
                        if modification_type == 'autophosphorylation':
                            args = [theme_agent, residue, pos, ev]
                        self.statements.append(ModStmt(*args))

    def get_regulate_amounts(self):
        """Extract RegulateAmount INDRA Statements."""
        qstr = "$.events.frames[(@.type is 'transcription')]"
        res = self.tree.execute(qstr)
        all_res = []
        if res is not None:
            all_res += list(res)
        qstr = "$.events.frames[(@.type is 'amount')]"
        res = self.tree.execute(qstr)
        if res is not None:
            all_res += list(res)

        for r in all_res:
            subtype = r.get('subtype')
            epistemics = self._get_epistemics(r)
            if epistemics.get('negated'):
                continue
            annotations, context = self._get_annot_context(r)
            frame_id = r['frame_id']
            args = r['arguments']
            theme = None
            for a in args:
                if self._get_arg_type(a) == 'theme':
                    theme = a['arg']
                    break
            if theme is None:
                continue
            theme_agent, theme_coords = self._get_agent_from_entity(theme)
            qstr = "$.events.frames[((@.type is 'regulation') or "\
                   "(@.type is 'activation')) and " + \
                   "(@.arguments[0].arg is '%s')]" % frame_id
            reg_res = self.tree.execute(qstr)
            for reg in reg_res:
                controller_agent, controller_coords = None, None
                for a in reg['arguments']:
                    if self._get_arg_type(a) == 'controller':
                        controller_agent, controller_coords = \
                            self._get_controller_agent(a)
                sentence = reg['verbose-text']
                annotations['agents']['coords'] = [controller_coords,
                                                   theme_coords]
                ev = Evidence(source_api='reach', text=sentence,
                              annotations=annotations, pmid=self.citation,
                              context=context, epistemics=epistemics)
                args = [controller_agent, theme_agent, ev]
                subtype = reg.get('subtype')
                if subtype.startswith('positive'):
                    st = IncreaseAmount(*args)
                else:
                    st = DecreaseAmount(*args)
                self.statements.append(st)

    def get_complexes(self):
        """Extract INDRA Complex Statements."""
        qstr = "$.events.frames[@.type is 'complex-assembly']"
        res = self.tree.execute(qstr)
        if res is None:
            return

        for r in res:
            epistemics = self._get_epistemics(r)
            if epistemics.get('negated'):
                continue
            # Due to an issue with the REACH output serialization
            # (though seemingly not with the raw mentions), sometimes
            # a redundant complex-assembly event is reported which can
            # be recognized by the missing direct flag, which we can filter
            # for here
            if epistemics.get('direct') is None:
                continue
            annotations, context = self._get_annot_context(r)
            args = r['arguments']
            sentence = r['verbose-text']
            members = []
            agent_coordinates = []
            for a in args:
                agent, coords = self._get_agent_from_entity(a['arg'])
                members.append(agent)
                agent_coordinates.append(coords)
            annotations['agents']['coords'] = agent_coordinates
            ev = Evidence(source_api='reach', text=sentence,
                          annotations=annotations, pmid=self.citation,
                          context=context, epistemics=epistemics)
            stmt = Complex(members, ev)
            self.statements.append(stmt)

    def get_activation(self):
        """Extract INDRA Activation Statements."""
        qstr = "$.events.frames[@.type is 'activation']"
        res = self.tree.execute(qstr)
        if res is None:
            return
        for r in res:
            epistemics = self._get_epistemics(r)
            if epistemics.get('negated'):
                continue
            sentence = r['verbose-text']
            annotations, context = self._get_annot_context(r)
            ev = Evidence(source_api='reach', text=sentence,
                          pmid=self.citation, annotations=annotations,
                          context=context, epistemics=epistemics)
            args = r['arguments']
            controller_agent = None
            for a in args:
                if self._get_arg_type(a) == 'controller':
                    controller_agent, controller_coords = \
                        self._get_controller_agent(a)
                if self._get_arg_type(a) == 'controlled':
                    controlled = a['arg']
            controlled_agent, controlled_coords = \
                self._get_agent_from_entity(controlled)
            if controller_agent is None or controlled_agent is None:
                continue
            annotations['agents']['coords'] = [controller_coords,
                                               controlled_coords]
            positive = (r['subtype'] == 'positive-activation')
            # By default, we choose Activation/Inhibition based on polarity
            stmt_cls = Activation if positive else Inhibition
            stmt_kwargs = {}
            # Here we handle a special case where we have the activation of
            # a modified form, which we transform into a modification
            # statement, e.g., Phosphorylation
            if controlled_agent.mods:
                # NOTE: can there be more than one mods here?
                mod = controlled_agent.mods[0]
                # We check all modification classes here
                if mod.mod_type in modtype_to_modclass:
                    stmt_cls = modtype_to_modclass[mod.mod_type]
                    # We take the residue/position information from
                    # the modificatio, if available
                    if mod.residue:
                        stmt_kwargs['residue'] = mod.residue
                    if mod.position:
                        stmt_kwargs['position'] = mod.position
                controlled_agent.mods = []
            st = stmt_cls(controller_agent, controlled_agent, **stmt_kwargs,
                          evidence=ev)
            self.statements.append(st)

    def get_translocation(self):
        """Extract INDRA Translocation Statements."""
        qstr = "$.events.frames[@.type is 'translocation']"
        res = self.tree.execute(qstr)
        if res is None:
            return
        for r in res:
            epistemics = self._get_epistemics(r)
            if epistemics.get('negated'):
                continue
            sentence = r['verbose-text']
            annotations, context = self._get_annot_context(r)
            args = r['arguments']
            from_location = None
            to_location = None
            for a in args:
                if self._get_arg_type(a) == 'theme':
                    agent, theme_coords = self._get_agent_from_entity(a['arg'])
                    if agent is None:
                        continue
                elif self._get_arg_type(a) == 'source':
                    from_location = self._get_location_by_id(a['arg'])
                elif self._get_arg_type(a) == 'destination':
                    to_location = self._get_location_by_id(a['arg'])
            # We skip statements that have no locations associated with them
            # at all
            if not from_location and not to_location:
                continue
            annotations['agents']['coords'] = [theme_coords]
            ev = Evidence(source_api='reach', text=sentence,
                          pmid=self.citation, annotations=annotations,
                          context=context, epistemics=epistemics)
            st = Translocation(agent, from_location, to_location,
                               evidence=ev)
            self.statements.append(st)

    def get_conversion(self):
        qstr = "$.events.frames[@.type is 'conversion']"
        res = self.tree.execute(qstr)
        if res is None:
            return
        for r in res:
            epistemics = self._get_epistemics(r)
            if epistemics.get('negated'):
                continue
            sentence = r['verbose-text']
            annotations, context = self._get_annot_context(r)
            ev = Evidence(source_api='reach', text=sentence,
                          pmid=self.citation, annotations=annotations,
                          context=context, epistemics=epistemics)
            args = r['arguments']
            controller_agent = substrate_agent = product_agent = None
            for a in args:
                if self._get_arg_type(a) == 'controller':
                    controller_agent, controller_coords = \
                        self._get_controller_agent(a)
                if self._get_arg_type(a) == 'substrate':
                    substrate_agent, substrate_coords = \
                        self._get_agent_from_entity(a['arg'])
                if self._get_arg_type(a) == 'product':
                    product_agent, product_coords = \
                        self._get_agent_from_entity(a['arg'])
            if not all({controller_agent, substrate_agent, product_agent}):
                continue
            annotations['agents']['coords'] = [controller_coords,
                                               substrate_coords,
                                               product_coords]
            st = Conversion(controller_agent, [substrate_agent],
                            [product_agent], evidence=[ev])
            self.statements.append(st)

    def _get_location_by_id(self, loc_id):
        qstr = "$.entities.frames[(@.frame_id is \'%s\')]" % loc_id
        res = self.tree.execute(qstr)
        if res is None:
            return None
        try:
            entity_term = next(res)
        except StopIteration:
            logger.debug(' %s is not an entity' % loc_id)
            return None
        name = entity_term.get('text')
        go_id = None
        for xr in entity_term['xrefs']:
            ns = xr['namespace']
            if ns == 'go':
                go_id = xr['id']

        # If there is no GO ID, we try to "ground" the name to an ID
        if go_id is None:
            go_id = go_client.get_go_id_from_label_or_synonym(name.lower())

        # Try to get valid location based on GO id
        if go_id is not None:
            loc = go_client.get_go_label(go_id)
            if loc:
                return loc
        return None

    def _get_agent_from_entity(self, entity_id):
        qstr = "$.entities.frames[(@.frame_id is \'%s\')]" % entity_id
        res = self.tree.execute(qstr)
        if res is None:
            return None, None
        try:
            entity_term = next(res)
        except StopIteration:
            logger.debug(' %s is not an entity' % entity_id)
            return None, None

        # This is the default name, which can be overwritten
        # below for specific database entries
        agent_name = entity_term['text']
        db_refs = self._get_db_refs(entity_term, self.organism_priority)

        mod_terms = entity_term.get('modifications')
        mods, muts = self._get_mods_and_muts_from_mod_terms(mod_terms)

        # get sentence coordinates of the entity
        coords = self._get_entity_coordinates(entity_term)

        agent = Agent(agent_name, db_refs=db_refs, mods=mods, mutations=muts)
        standardize_agent_name(agent, standardize_refs=True)
        return agent, coords

    @staticmethod
    def _get_db_refs(entity_term, organism_priority=None):
        db_refs = {}
        for xr in entity_term['xrefs']:
            ns = xr['namespace']
            if ns == 'uniprot':
                # Note: we add both full protein and protein chain
                # IDs here so that we can appli organism prioritization in
                # a uniform way. Later these will be separated out.
                up_id = xr['id']
                db_refs['UP'] = up_id
            elif ns == 'hgnc':
                db_refs['HGNC'] = xr['id']
            elif ns == 'pfam':
                fplx_id = famplex_map.get(('PF', xr['id']))
                if fplx_id:
                    db_refs['FPLX'] = fplx_id
                db_refs['PF'] = xr['id']
            elif ns == 'interpro':
                fplx_id = famplex_map.get(('IP', xr['id']))
                if fplx_id:
                    db_refs['FPLX'] = fplx_id
                db_refs['IP'] = xr['id']
            elif ns == 'chebi':
                db_refs['CHEBI'] = xr['id']
            elif ns == 'pubchem':
                db_refs['PUBCHEM'] = xr['id']
            elif ns == 'go':
                go_id = xr['id']
                # Handle secondary to primary mapping if necessary
                pri = go_client.get_primary_id(go_id)
                if pri:
                    go_id = pri
                db_refs['GO'] = go_id
            elif ns == 'mesh':
                db_refs['MESH'] = xr['id']
            elif ns == 'hmdb':
                db_refs['HMDB'] = xr['id']
            elif ns == 'simple_chemical':
                if xr['id'].startswith('HMDB'):
                    db_refs['HMDB'] = xr['id']
            # We handle "be" here for compatibility with older versions
            elif ns in ('fplx', 'be'):
                db_refs['FPLX'] = xr['id']
            elif ns == 'proonto':
                db_refs['PR'] = xr['id']
            # These name spaces are ignored
            elif ns in ['uaz']:
                pass
            else:
                logger.warning('Unhandled xref namespace: %s' % ns)
        db_refs['TEXT'] = entity_term['text']

        # If we have a UniProt grounding and we have a non-default
        # organism priority list, we call the prioritization function
        if db_refs.get('UP'):
            if organism_priority:
                # These are all the unique groundings in the alt-xrefs list,
                # which redundantly lists the same match multiple times because
                # it enumerates multiple synonyms for organisms redundantly
                unique_altxrefs = \
                    set((axr['namespace'], axr['id'])
                        for axr in entity_term.get('alt-xrefs', []))
                # This returns a single prioritized UniProt ID or None
                prioritized_id = \
                    prioritize_organism_grounding(db_refs['UP'],
                                                  unique_altxrefs,
                                                  organism_priority)
                # If we got an ID, we set the UP grounding to that, otherwise
                # we keep what we already got from the primary xref
                if prioritized_id:
                    db_refs['UP'] = prioritized_id
            # After all this, we need to separate protein chain grounding
            # and so if we are dealing with one of those, we pop out the UP
            # key, split the ID to get the chain ID and add that in the UPPRO
            # namespace.
            if '#' in db_refs['UP']:
                up_id = db_refs.pop('UP', None)
                db_refs['UPPRO'] = up_id.split('#')[1]

        db_refs = standardize_db_refs(db_refs)
        return db_refs

    def _get_mods_and_muts_from_mod_terms(self, mod_terms):
        mods = []
        muts = []
        if mod_terms is not None:
            for m in mod_terms:
                if m['type'].lower() == 'mutation':
                    # Evidence is usualy something like "V600E"
                    # We could parse this to get the amino acid
                    # change that happened.
                    mutation_str = m.get('evidence')
                    # TODO: sometimes mutation_str is "mutant", "Mutant",
                    # "mutants" - this indicates that there is a mutation
                    # but not the specific type. We should encode this
                    # somehow as a "blank" mutation condition
                    mut = self._parse_mutation(mutation_str)
                    if mut is not None:
                        muts.append(mut)
                else:
                    mcs = self._get_mod_conditions(m)
                    mods.extend(mcs)
        return mods, muts

    def _get_mod_conditions(self, mod_term):
        """Return a list of ModConditions given a mod term dict."""
        site = mod_term.get('site')
        if site is not None:
            mods = self._parse_site_text(site)
        else:
            mods = [Site(None, None)]

        mcs = []
        for mod in mods:
            mod_res, mod_pos = mod
            mod_type_str = mod_term['type'].lower()
            if mod_type_str == 'unknown':
                continue
            mod_state = agent_mod_map.get(mod_type_str)
            # We skip unknown modifications since they are very often
            # unrelated to PTMs, representing things like "expression"
            # These are real PTM states
            if mod_state is not None:
                mc = ModCondition(mod_state[0], residue=mod_res,
                                  position=mod_pos, is_modified=mod_state[1])
                mcs.append(mc)
            else:
                logger.warning('Unhandled entity modification type: %s'
                               % mod_type_str)
        return mcs

    def _get_entity_coordinates(self, entity_term):
        """Return sentence coordinates for a given entity.

        Given an entity term return the associated sentence coordinates as
        a tuple of the form (int, int). Returns None if for any reason the
        sentence coordinates cannot be found.
        """
        # The following lines get the starting coordinate of the sentence
        # containing the entity.
        sent_id = entity_term.get('sentence')
        if sent_id is None:
            return None
        qstr = "$.sentences.frames[(@.frame_id is \'%s')]" % sent_id
        res = self.tree.execute(qstr)
        if res is None:
            return None
        try:
            sentence = next(res)
        except StopIteration:
            return None
        sent_start = sentence.get('start-pos')
        if sent_start is None:
            return None
        sent_start = sent_start.get('offset')
        if sent_start is None:
            return None
        # Get the entity coordinate in the entire text and subtract the
        # coordinate of the first character in the associated sentence to
        # get the sentence coordinate of the entity. Return None if entity
        # coordinates are missing
        entity_start = entity_term.get('start-pos')
        entity_stop = entity_term.get('end-pos')
        if entity_start is None or entity_stop is None:
            return None
        entity_start = entity_start.get('offset')
        entity_stop = entity_stop.get('offset')
        if entity_start is None or entity_stop is None:
            return None
        return (entity_start - sent_start, entity_stop - sent_start)

    def _get_annot_context(self, frame_term):
        annotations = {'found_by': frame_term['found_by'],
                       'agents': {}}
        try:
            context_id = frame_term['context']
        except KeyError:
            return annotations, None
        # For backwards compatibility with older versions
        # of REACH
        if isinstance(context_id, dict):
            context_term = context_id
            species = context_term.get('Species')
            cell_type = context_term.get('CellType')
            cell_line = None
            location = None
            tissue = None
            organ = None
        else:
            qstr = "$.entities.frames[(@.frame_id is \'%s\')]" % context_id[0]
            res = self.tree.execute(qstr)
            if res is None:
                return annotations, None
            context_frame = next(res)
            facets = context_frame['facets']
            cell_line = facets.get('cell-line')
            cell_type = facets.get('cell-type')
            species = facets.get('organism')
            location = facets.get('location')
            tissue = facets.get('tissue_type')
            organ = facets.get('organ')

        def get_ref_context(lst):
            if not lst:
                return None
            db_name, db_id = lst[0].split(':', 1)
            db_name = db_name.upper()
            # Here we are dealing with UniProt subcellular components
            # so we use a different namespace for those
            if db_name == 'UNIPROT':
                db_name = 'UPLOC'
            # These aren't real groundings
            elif db_name == 'UAZ':
                return None
            standard_name, db_refs = \
                standardize_name_db_refs({db_name: db_id})
            return RefContext(standard_name, db_refs=db_refs)

        context = BioContext()
        # Example: ['taxonomy:9606']
        context.species = get_ref_context(species)
        # Example: ['cl:CL:0000148']
        context.cell_type = get_ref_context(cell_type)
        # Example: ['cellosaurus:CVCL_0504']
        context.cell_line = get_ref_context(cell_line)
        # Example: ['go:GO:0005886']
        context.location = get_ref_context(location)
        # Example: ['uberon:UBERON:0000105']
        context.organ = get_ref_context(organ)
        # NOTE: we can't handle tissue currently
        # context['tissue'] = tissue
        # This is so we don't add a blank BioContext as context and rather
        # just add None
        if not context:
            context = None
        return annotations, context

    def _get_epistemics(self, event):
        epistemics = {}
        # Check whether information is negative
        neg = event.get('is_negated')
        if neg is True:
            epistemics['negated'] = True
        # Check if it is a hypothesis
        hyp = event.get('is_hypothesis')
        if hyp is True:
            epistemics['hypothesis'] = True
        # Check if it is direct
        if 'is_direct' in event:
            direct = event['is_direct']
            epistemics['direct'] = direct
        # Get the section of the paper it comes from
        section = self._get_section(event)
        epistemics['section_type'] = section
        return epistemics

    _section_list = ['title', 'abstract', 'introduction', 'background',
                     'results', 'methods', 'discussion', 'conclusion',
                     'supplementary', 'figure']

    def _get_section(self, event):
        """Get the section of the paper that the event is from."""
        sentence_id = event.get('sentence')
        section = None
        if sentence_id:
            qstr = "$.sentences.frames[(@.frame_id is \'%s\')]" % sentence_id
            res = self.tree.execute(qstr)
            if res:
                sentence_frame = list(res)[0]
                passage_id = sentence_frame.get('passage')
                if passage_id:
                    qstr = "$.sentences.frames[(@.frame_id is \'%s\')]" % \
                            passage_id
                    res = self.tree.execute(qstr)
                    if res:
                        passage_frame = list(res)[0]
                        section = passage_frame.get('section-id')
        # If the section is in the standard list, return as is
        if section in self._section_list:
            return section
        # Next, handle a few special cases that come up in practice
        elif section.startswith('fig'):
            return 'figure'
        elif section.startswith('supm'):
            return 'supplementary'
        elif section == 'article-title':
            return 'title'
        elif section in ['subjects|methods', 'methods|subjects']:
            return 'methods'
        elif section == 'conclusions':
            return 'conclusion'
        elif section == 'intro':
            return 'introduction'
        else:
            return None

    def _get_controller_agent(self, arg):
        """Return a single or a complex controller agent."""
        controller_agent = None
        controller = arg.get('arg')
        # There is either a single controller here
        if controller is not None:
            controller_agent, coords = self._get_agent_from_entity(controller)
        # Or the controller is a complex
        elif arg['argument-type'] == 'complex':
            controllers = list(arg.get('args').values())
            controller_agent, coords = \
                self._get_agent_from_entity(controllers[0])
            bound_agents = [self._get_agent_from_entity(c)[0]
                            for c in controllers[1:]]
            bound_conditions = [BoundCondition(ba, True) for
                                ba in bound_agents]
            controller_agent.bound_conditions = bound_conditions
        return controller_agent, coords

    @staticmethod
    def _get_arg_type(arg):
        """Return the type of the argument with backwards compatibility."""
        if arg.get('argument_label') is not None:
            return arg.get('argument_label')
        else:
            return arg.get('type')

    @staticmethod
    def _parse_mutation(s):
        m = re.match(r'([A-Z]+)([0-9]+)([A-Z]+)', s.upper())
        if m is not None:
            parts = [str(g) for g in m.groups()]
            try:
                residue_from = get_valid_residue(parts[0])
            except Exception as e:
                return None
            try:
                residue_to = get_valid_residue(parts[2])
            except Exception as e:
                return None
            position = parts[1]
            mut = MutCondition(position, residue_from, residue_to)
            return mut
        elif s.lower() in ('mutation', 'mutations', 'mutant', 'mutants',
                           'mutational'):
            mut = MutCondition(None, None, None)
            return mut
        else:
            logger.warning('Unhandled mutation string: %s' % s)
        return None

    @staticmethod
    def _parse_site_text(s):
        has_comma = ',' in s
        has_slash = '/' in s

        has_both = has_comma and has_slash
        if has_both:
            logger.error(s + ' is not a valid site text string')
            return []

        if has_comma:
            texts = s.split(',')
        else:
            texts = s.split('/')

        sites = [parse_amino_acid_string(t) for t in texts]

        # If the first site has a residue, and the remaining sites do not
        # explicitly give a residue (example: Tyr-577/576), then apply the
        # first site's residue to all sites in the site text.
        only_first_site_has_residue = sites[0].residue is not None
        for i in range(1, len(sites)):
            if sites[i].residue is not None:
                only_first_site_has_residue = False
        if only_first_site_has_residue:
            for i in range(1, len(sites)):
                sites[i] = Site(sites[0].residue, sites[i].position)

        return sites


def parse_amino_acid_string(s):
    s = s.strip()
    for p in (_site_pattern1, _site_pattern2, _site_pattern3):
        m = re.match(p, s.upper())
        if m is not None:
            residue = get_valid_residue(m.groups()[0])
            site = m.groups()[1]
            return Site(residue, site)
    m = re.match(_site_pattern4, s.upper())
    if m is not None:
        site = m.groups()[0]
        residue = m.groups()[1]
        return Site(residue, site)
    for p in (_site_pattern5, _site_pattern6, _site_pattern7):
        m = re.match(p, s.upper())
        if m is not None:
            residue = get_valid_residue(m.groups()[0])
            site = None
            return Site(residue, site)
    m = re.match(_site_pattern8, s.upper())
    if m is not None:
        site = m.groups()[0]
        residue = None
        return Site(residue, site)
    logger.warning('Could not parse site text %s' % s)
    return Site(None, None)


_site_pattern1 = '([' + ''.join(list(amino_acids.keys())) + '])[-]?([0-9]+)$'
_site_pattern2 = '(' + '|'.join([v['short_name'].upper() for
                                 v in amino_acids.values()]) + \
                        ')[- ]?([0-9]+)$'
_site_pattern3 = '(' + '|'.join([v['indra_name'].upper() for
                                 v in amino_acids.values()]) + \
                        ')[^0-9]*([0-9]+)$'
_site_pattern4 = '([0-9]+)[ ]?([' + ''.join(list(amino_acids.keys())) + '])$'
_site_pattern5 = '^([' + ''.join(list(amino_acids.keys())) + '])$'
_site_pattern6 = '^(' + '|'.join([v['short_name'].upper() for
                                 v in amino_acids.values()]) + ')$'
_site_pattern7 = '.*(' + '|'.join([v['indra_name'].upper() for
                                   v in amino_acids.values()]) + ').*'
_site_pattern8 = '([0-9]+)$'

# Subtypes that exist but we don't handle: hydrolysis
agent_mod_map = {
    'phosphorylation': ('phosphorylation', True),
    'phosphorylated': ('phosphorylation', True),
    'dephosphorylation': ('phosphorylation', False),
    'acetylation': ('acetylation', True),
    'deacetylation': ('acetylation', False),
    'ubiquitination': ('ubiquitination', True),
    'deubiquitination': ('ubiquitination', False),
    'hydroxylation': ('hydroxylation', True),
    'dehydroxylation': ('hydroxylation', False),
    'sumoylation': ('sumoylation', True),
    'desumoylation': ('sumoylation', False),
    'glycosylation': ('glycosylation', True),
    'deglycosylation': ('glycosylation', False),
    'farnesylation': ('farnesylation', True),
    'defarnesylation': ('farnesylation', False),
    'ribosylation': ('ribosylation', True),
    'deribosylation': ('ribosylation', False),
    'methylation': ('methylation', True),
    'demethylation': ('methylation', False),
}


def _read_famplex_map():
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         '../../resources/famplex_map.tsv')
    famplex_map = {}
    csv_rows = read_unicode_csv(fname, delimiter='\t')
    for row in csv_rows:
        source_ns = row[0]
        source_id = row[1]
        be_id = row[2]
        famplex_map[(source_ns, source_id)] = be_id
    return famplex_map


famplex_map = _read_famplex_map()


def _read_reach_rule_regexps():
    """Load in a file with the regular expressions corresponding to each
    reach rule. Why regular expression matching?
    The rule name in found_by has instances of some reach rules for each
    possible event type
    (activation, binding, etc). This makes for too many different types of
    rules for practical curation of examples.
    We use regular expressions to only match the rule used for extraction,
    independently of what the event is.
    """
    reach_rule_filename = \
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'reach_rule_regexps.txt')
    with open(reach_rule_filename, 'r') as f:
        reach_rule_regexp = []
        for line in f:
            reach_rule_regexp.append(line.rstrip())
    return reach_rule_regexp


reach_rule_regexps = _read_reach_rule_regexps()


def determine_reach_subtype(event_name):
    """Returns the category of reach rule from the reach rule instance.

    Looks at a list of regular
    expressions corresponding to reach rule types, and returns the longest
    regexp that matches, or None if none of them match.

    Parameters
    ----------
    evidence : indra.statements.Evidence
        A reach evidence object to subtype

    Returns
    -------
    best_match : str
        A regular expression corresponding to the reach rule that was used to
        extract this evidence
    """

    best_match_length = None
    best_match = None
    for ss in reach_rule_regexps:
        if re.search(ss, event_name):
            if best_match is None or len(ss) > best_match_length:
                best_match = ss
                best_match_length = len(ss)

    return best_match


def prioritize_organism_grounding(first_id, xrefs, organism_priority):
    """Pick a prioritized organism-specific UniProt ID for a protein."""
    # We find the organism for the first ID picked by Reach
    first_organism = uniprot_client.get_organism_id(first_id.split('#')[0])
    # We take only UniProt groundings from the xrefs list
    uniprot_ids = [xr[1] for xr in xrefs if xr[0] == 'uniprot']
    # We group UniProt IDs by their organism ID
    groundings_by_organism = defaultdict(list)
    for up_id in uniprot_ids:
        organism_id = uniprot_client.get_organism_id(up_id.split('#')[0])
        groundings_by_organism[organism_id].append(up_id)
    # We then go down the list of prioritized organisms and if we find a match
    # we return immediately
    for organism in organism_priority:
        # If the organism matches the organism of the first xref match given by
        # Reach then we return that ID
        if organism == first_organism:
            return first_id
        # Otherwiser, if we have a group of matches for the current organism,
        # we sort the list of matches and return the first one (so that the
        # result is deterministic, though arbitrary).
        if organism in groundings_by_organism:
            return sorted(groundings_by_organism[organism])[0]
    # If there is no prioritized organism-specific match, we return None
    # and let the upstream code handle what to do.
    return None
