# -*- coding: utf-8 -*-

"""Processor for PyBEL."""

import os
import re
import logging
import pybel.dsl as dsl
import pybel.constants as pc
import pybel.language
from collections import defaultdict
from pybel.struct import has_protein_modification
from pybel.canonicalize import edge_to_bel
from bel_resources import get_bel_resource
from indra.statements import *
from indra.util import read_unicode_csv
from indra.databases import (
    chebi_client, go_client, hgnc_client, mesh_client,
    mirbase_client, uniprot_client, taxonomy_client,
    identifiers
)
from indra.ontology.standardize import standardize_name_db_refs
from indra.assemblers.pybel.assembler import _pybel_indra_act_map

__all__ = [
    'PybelProcessor',
    'get_agent',
]

logger = logging.getLogger(__name__)


_pybel_indra_pmod_map_helper = {
    'Ph': 'phosphorylation',
    'Hy': 'hydroxylation',
    'Sumo': 'sumoylation',
    'Ac': 'acetylation',
    'Glyco': 'glycosylation',
    'ADPRib': 'ribosylation',
    'Ub': 'ubiquitination',
    'Farn': 'farnesylation',
    'Gerger': 'geranylgeranylation',
    'Palm': 'palmitoylation',
    'Myr': 'myristoylation',
    'Me': 'methylation',
}
_pybel_indra_pmod_map = {
    v['xrefs'][0]: _pybel_indra_pmod_map_helper[k]
    for k, v in pybel.language.pmod_mappings.items()
    if k in _pybel_indra_pmod_map_helper  # More indra statements could be proposed based on this
}

#: A mapping from the BEL text location annotation to the INDRA ones at
#: :py:data:`indra.reach.processor._section_list`
#: see https://arty.scai.fraunhofer.de/artifactory/bel/annotation/text-location/text-location-1.0.0.belanno
_pybel_text_location_map = {
    "Abstract": 'abstract',
    "Results": 'results',
    "Legend": 'figure',
    "Review": None,
    'Introduction': 'introduction',
    'Methods': 'methods',
    'Discussion': 'discussion',
    'Conclusion': 'conclusion'
}


class PybelProcessor(object):
    """Extract INDRA Statements from a PyBEL Graph.

    Currently does not handle non-causal relationships (positiveCorrelation,
    (negativeCorrelation, hasVariant, etc.)

    Parameters
    ----------
    graph : pybel.BELGraph
        PyBEL graph containing the BEL content.

    Attributes
    ----------
    statements : list[indra.statements.Statement]
        A list of extracted INDRA Statements representing BEL Statements.
    """
    def __init__(self, graph):
        self.graph = graph
        self.statements = []
        self.unhandled = []
        self.annot_manager = AnnotationManager(self.graph.annotation_url)

    # FIXME: Handle reactions
    def get_statements(self):
        for u_data, v_data, k, d in self.graph.edges(keys=True, data=True):
            # We only interpret causal relations, not correlations
            if d[pc.RELATION] not in pc.CAUSAL_RELATIONS:
                self.unhandled.append((u_data, v_data, k, d))
                continue
            # If the left or right-hand sides involve complex abundances,
            # add them as statements
            for node_ix, node in enumerate((u_data, v_data)):
                if isinstance(node, dsl.ComplexAbundance):
                    self._get_enum_complex(u_data, v_data, k, d, node_ix)
            subj_activity = _get_activity_condition(d.get(pc.SOURCE_MODIFIER))
            obj_activity = _get_activity_condition(d.get(pc.TARGET_MODIFIER))
            obj_to_loc = _get_translocation_target(d.get(pc.TARGET_MODIFIER))
            # If the object is a translocation, this represents a controlled
            # translocation, which we currently do not represent
            if obj_to_loc:
                self.unhandled.append((u_data, v_data, k, d))
                logger.info("Controlled translocations are currently not "
                            "handled: %s)", edge_to_bel(u_data, v_data, d))
                continue

            # Modification, e.g.
            #   x(Foo) -> p(Bar, pmod(Ph))
            #   act(x(Foo)) -> p(Bar, pmod(Ph))
            if isinstance(v_data, dsl.Protein) and \
                    has_protein_modification(v_data):
                if obj_activity:
                    logger.info("Ignoring object activity modifier in "
                                "modification statement: %s, %s, %s, %s",
                                u_data, v_data, k, d)
                else:
                    self._get_modification(u_data, v_data, k, d)
            elif obj_activity:
                # If the agents on the left and right hand sides are the same,
                # then get an active form:
                # ActiveForm
                #   p(Foo, {variants}) ->/-| act(p(Foo))
                # Also Composite active forms:
                #   compositeAbundance(p(Foo, pmod('Ph', 'T')),
                #                       p(Foo, pmod('Ph', 'Y'))) ->/-|
                #                            act(p(Foo))
                if not subj_activity and _proteins_match(u_data, v_data):
                    self._get_active_form(u_data, v_data, k, d)
                # Gef
                #   act(p(Foo)) => gtp(p(Foo))
                # Gap
                #   act(p(Foo)) =| gtp(p(Foo))
                elif subj_activity and _rel_is_direct(d) and \
                    obj_activity.activity_type == 'gtpbound':
                    self._get_gef_gap(u_data, v_data, k, d)
                # Activation/Inhibition
                #   x(Foo) -> act(x(Foo))
                #   act(x(Foo)) -> act(x(Foo))
                # GtpActivation
                #   gtp(p(Foo)) => act(p(Foo))
                else:
                    self._get_regulate_activity(u_data, v_data, k, d)
            # Activations involving biological processes or pathologies
            #   x(Foo) -> bp(Bar)
            elif isinstance(v_data, (dsl.BiologicalProcess, dsl.Pathology)):
                self._get_regulate_activity(u_data, v_data, k, d)
            # Regulate amount
            #   x(Foo) -> p(Bar)
            #   x(Foo) -> r(Bar)
            #   act(x(Foo)) -> p(Bar):
            #   x(Foo) -> deg(p(Bar))
            #   act(x(Foo)) ->/-| deg(p(Bar))
            elif (
                isinstance(v_data, (
                    dsl.Protein, dsl.Rna, dsl.Abundance, dsl.MicroRna,
                    dsl.NamedComplexAbundance,
                ))
                and not obj_activity
            ):
                self._get_regulate_amount(u_data, v_data, k, d)
            # Controlled conversions
            #   x(Foo) -> rxn(reactants(r1,...,rn), products(p1,...pn))
            #   act(x(Foo)) -> rxn(reactants(r1,...,rn), products(p1,...pn))
            # Note that we can't really handle statements where the relation
            # is decreases, as inhibition of a reaction match the semantics
            # of a controlled conversion
            elif (
                isinstance(v_data, dsl.Reaction)
                and d[pc.RELATION] in pc.CAUSAL_INCREASE_RELATIONS
            ):
                self._get_conversion(u_data, v_data, k, d)
            # UNHANDLED
            # rxn(reactants(r1,...,rn), products(p1,...pn))
            # Complex(a,b)
            # p(A, pmod('ph')) -> Complex(A, B)
            # Complex(A-Ph, B)
            # Complexes
            #   complex(x(Foo), x(Bar), ...)
            else:
                self.unhandled.append((u_data, v_data, k, d))

    def _get_enum_complex(self, u_data, v_data, k, edge_data, node_ix):
        # Get an agent with bound conditions from the Complex
        assert node_ix in (0, 1)
        node = [u_data, v_data][node_ix]
        cplx_agent = get_agent(node, None)
        if cplx_agent is None:
            return
        agents = [bc.agent for bc in cplx_agent.bound_conditions]
        cplx_agent.bound_conditions = []
        agents.append(cplx_agent)
        ev = self._get_evidence(u_data, v_data, k, edge_data)
        stmt = Complex(agents, evidence=[ev])
        self.statements.append(stmt)

    def _get_regulate_amount(self, u_data, v_data, k, edge_data):
        subj_agent = get_agent(u_data, edge_data.get(pc.SOURCE_MODIFIER))
        obj_agent = get_agent(v_data, edge_data.get(pc.TARGET_MODIFIER))
        if subj_agent is None or obj_agent is None:
            self.unhandled.append((u_data, v_data, edge_data))
            return
        obj_mod = edge_data.get(pc.TARGET_MODIFIER)
        has_deg = (obj_mod and obj_mod.get(pc.MODIFIER) == pc.DEGRADATION)
        rel = edge_data[pc.RELATION]
        if rel == pc.REGULATES:
            # TODO: once generic regulations work, we can make this an
            #  actual statement
            # stmt_class = RegulateAmount
            return
        elif has_deg:
            stmt_class = (DecreaseAmount if rel in
                          pc.CAUSAL_INCREASE_RELATIONS else IncreaseAmount)
        else:
            stmt_class = (IncreaseAmount if rel in
                          pc.CAUSAL_INCREASE_RELATIONS else DecreaseAmount)
        ev = self._get_evidence(u_data, v_data, k, edge_data)
        stmt = stmt_class(subj_agent, obj_agent, evidence=[ev])
        self.statements.append(stmt)

    def _get_modification(self, u_data, v_data, k, edge_data):
        subj_agent = get_agent(u_data, edge_data.get(pc.SOURCE_MODIFIER))
        mods, muts = _get_mods_and_muts(v_data)
        v_data_no_mods = v_data.get_parent()
        obj_agent = get_agent(v_data_no_mods, edge_data.get(pc.TARGET_MODIFIER))
        if subj_agent is None or obj_agent is None:
            self.unhandled.append((u_data, v_data, k, edge_data))
            return
        for mod in mods:
            modclass = modtype_to_modclass[mod.mod_type]
            ev = self._get_evidence(u_data, v_data, k, edge_data)
            stmt = modclass(subj_agent, obj_agent, mod.residue, mod.position,
                            evidence=[ev])
            self.statements.append(stmt)

    def _get_regulate_activity(self, u_data, v_data, k, edge_data):
        # Subject info
        subj_agent = get_agent(u_data, edge_data.get(pc.SOURCE_MODIFIER))
        subj_activity = _get_activity_condition(edge_data.get(pc.SOURCE_MODIFIER))
        # Object info
        # Note: Don't pass the object modifier data because we don't want to
        # put an activity on the agent
        obj_agent = get_agent(v_data, None)
        # If it's a bioprocess object, we won't have an activity in the edge
        if isinstance(v_data, (dsl.BiologicalProcess, dsl.Pathology)):
            activity_type = 'activity'
        else:
            obj_activity_condition = \
                            _get_activity_condition(edge_data.get(pc.TARGET_MODIFIER))
            activity_type = obj_activity_condition.activity_type
            assert obj_activity_condition.is_active is True
        # Check for valid subject/object
        if subj_agent is None or obj_agent is None:
            self.unhandled.append((u_data, v_data, edge_data))
            return
        # Check which kind of statement we need to make
        # GtpActivation
        if subj_activity and subj_activity.activity_type == 'gtpbound' and \
            isinstance(u_data, dsl.Protein) and isinstance(v_data, dsl.Protein) and \
            edge_data[pc.RELATION] == pc.DIRECTLY_INCREASES:
            stmt_class = GtpActivation
        elif edge_data[pc.RELATION] in pc.CAUSAL_INCREASE_RELATIONS:
            stmt_class = Activation
        elif edge_data[pc.RELATION] == pc.REGULATES:
            # TODO: once generic regulations work, we can make this an
            #  actual statement
            # stmt_class = RegulateActivity
            return
        else:
            stmt_class = Inhibition
        ev = self._get_evidence(u_data, v_data, k, edge_data)
        stmt = stmt_class(subj_agent, obj_agent, activity_type, evidence=[ev])
        self.statements.append(stmt)

    def _get_active_form(self, u_data, v_data, k, edge_data):
        subj_agent = get_agent(u_data, edge_data.get(pc.SOURCE_MODIFIER))
        # Don't pass the object modifier info because we don't want an activity
        # condition applied to the agent
        obj_agent = get_agent(v_data)
        if subj_agent is None or obj_agent is None:
            self.unhandled.append((u_data, v_data, edge_data))
            return
        obj_activity_condition = \
                        _get_activity_condition(edge_data.get(pc.TARGET_MODIFIER))
        activity_type = obj_activity_condition.activity_type
        # If the relation is DECREASES, this means that this agent state
        # is inactivating
        is_active = edge_data[pc.RELATION] in pc.CAUSAL_INCREASE_RELATIONS
        ev = self._get_evidence(u_data, v_data, k, edge_data)
        stmt = ActiveForm(subj_agent, activity_type, is_active, evidence=[ev])
        self.statements.append(stmt)

    def _get_gef_gap(self, u_data, v_data, k, edge_data):
        subj_agent = get_agent(u_data, edge_data.get(pc.SOURCE_MODIFIER))
        obj_agent = get_agent(v_data)
        if subj_agent is None or obj_agent is None:
            self.unhandled.append((u_data, v_data, k, edge_data))
            return
        ev = self._get_evidence(u_data, v_data, k, edge_data)
        if edge_data[pc.RELATION] in pc.CAUSAL_INCREASE_RELATIONS:
            stmt_class = Gef
        else:
            stmt_class = Gap
        stmt = stmt_class(subj_agent, obj_agent, evidence=[ev])
        self.statements.append(stmt)

    def _get_conversion(self, u_data, v_data, k, edge_data):
        subj_agent = get_agent(u_data, edge_data.get(pc.SOURCE_MODIFIER))
        # Get the nodes for the reactants and products
        reactant_agents = [get_agent(r) for r in v_data[pc.REACTANTS]]
        product_agents = [get_agent(p) for p in v_data[pc.PRODUCTS]]
        # We are not handling the following degenerate cases:
        # If there is no subject agent
        if (subj_agent is None or
                # If get_agent returned None for any of the reactants or
                # products
                any(r is None for r in reactant_agents) or
                any(p is None for p in product_agents) or
                # If there are no reactants and or no products
                (not reactant_agents and not product_agents)):
            self.unhandled.append((u_data, v_data, k, edge_data))
            return
        ev = self._get_evidence(u_data, v_data, k, edge_data)
        stmt = Conversion(subj_agent, obj_from=reactant_agents,
                          obj_to=product_agents, evidence=ev)
        self.statements.append(stmt)

    def _get_evidence(self, u_data, v_data, k, edge_data):
        ev_text = edge_data.get(pc.EVIDENCE)
        ev_citation = edge_data.get(pc.CITATION)
        ev_pmid = None
        if ev_citation:
            cit_type = ev_citation.namespace
            cit_ref = ev_citation.identifier
            if cit_type == pc.CITATION_TYPE_PUBMED:
                ev_pmid = cit_ref
                ev_ref = None
            else:
                ev_pmid = None
                ev_ref = '%s: %s' % (cit_type, cit_ref)
        epistemics = {'direct': _rel_is_direct(edge_data)}
        annotations = edge_data.get(pc.ANNOTATIONS, {})
        annotations['bel'] = edge_to_bel(u_data, v_data, edge_data)
        if ev_ref:  # FIXME what if ev_citation is Falsy?
            annotations['citation_ref'] = ev_ref

        context = extract_context(annotations, self.annot_manager)

        text_location = annotations.pop('TextLocation', None)
        if text_location:
            text_location = text_location[0].identifier
            epistemics['section_type'] = \
                _pybel_text_location_map.get(text_location)

        ev = Evidence(text=ev_text, pmid=ev_pmid, source_api='bel',
                      source_id=k, epistemics=epistemics,
                      annotations=annotations, context=context)
        return ev


def get_agent(node_data, node_modifier_data=None):
    """Get an INDRA agent from a PyBEL node."""
    # Check the node type/function
    if not isinstance(node_data, dsl.BaseEntity):
        raise TypeError('Non-pybel dict given: ({}) {}'.format(
            type(node_data), node_data))

    if not isinstance(node_data, (
        dsl.Protein, dsl.Rna, dsl.BiologicalProcess, dsl.ComplexAbundance,
        dsl.NamedComplexAbundance, dsl.Pathology, dsl.Abundance,
        dsl.MicroRna, dsl.Gene,
    )):
        mod_data = node_modifier_data or 'No node data'
        logger.info("Nodes of type %s not handled: %s",
                    node_data.function, mod_data)
        return None

    # Skip gene/protein fusions
    if isinstance(node_data, dsl.FusionBase):
        logger.info("Gene and protein fusions not handled: %s", node_data)
        return None
    # COMPLEXES ------------
    # First, handle complexes, which will consist recursively of other agents
    if isinstance(node_data, dsl.ComplexAbundance):
        # First, check for members: if there are no members, we assume this
        # is a named complex
        members = node_data.members
        if members is None:
            return None
        # Otherwise, get the "main" agent, to which the other members will be
        # attached as bound conditions
        main_agent = get_agent(members[0])
        # If we can't get the main agent, return None
        if main_agent is None:
            return None
        bound_conditions = [BoundCondition(get_agent(m), True)
                            for m in members[1:]]
        # Check the bound_conditions for any None agents
        if any([bc.agent is None for bc in bound_conditions]):
            return None
        main_agent.bound_conditions = bound_conditions
        # Get activity of main agent
        ac = _get_activity_condition(node_modifier_data)
        main_agent.activity = ac
        return main_agent
    # OTHER NODE TYPES -----
    # Get node identifier information
    name = node_data.name
    ns = node_data.namespace.upper()
    ident = node_data.identifier
    # No ID present, get identifier using the name, namespace
    if not ident:
        assert name, "Node must have a name if lacking an identifier."
        name, db_refs = get_db_refs_by_name(ns, name, node_data)
    # We've already got an identifier, look up other identifiers if necessary
    else:
        name, db_refs = get_db_refs_by_ident(ns, ident, node_data)
    if db_refs is None:
        logger.info('Unable to get identifier information for node: %s',
                    node_data)
        return None

    # Get modification conditions
    mods, muts = _get_mods_and_muts(node_data)
    # Get activity condition
    ac = _get_activity_condition(node_modifier_data)
    to_loc = _get_translocation_target(node_modifier_data)
    # Check for unhandled node modifiers, skip if so
    if _has_unhandled_modifiers(node_modifier_data):
        return None
    if not name:
        return None
    # Make the agent
    ag = Agent(name, db_refs=db_refs, mods=mods, mutations=muts, activity=ac,
               location=to_loc)
    return ag


def get_db_refs_by_name(ns, name, node_data):
    """Return standard name and grounding based on a namespace and a name.

    Parameters
    ----------
    ns : str
        A name space in which the given name is interpreted.
    name : str
        The name in the given name space to get grounding for.
    node_data : dict
        Node data for logging purposes.

    Returns
    -------
    name : str
        The standardized name for the given entity.
    db_refs : dict
        The grounding for the given entity.

    """
    db_refs = None
    if ns == 'HGNC':
        # Assumption: name is an HGNC symbol
        hgnc_id = hgnc_client.get_current_hgnc_id(name)
        if not hgnc_id:
            logger.info("Invalid HGNC name: %s (%s)" % (name, node_data))
            return name, None
        elif isinstance(hgnc_id, list):
            logger.info('More than one current HGNC ID for %s, choosing %s'
                        % (name, hgnc_id[0]))
            hgnc_id = hgnc_id[0]
        name = hgnc_client.get_hgnc_name(hgnc_id)
        db_refs = {'HGNC': hgnc_id}
        up_id = _get_up_id(hgnc_id)
        if up_id:
            db_refs['UP'] = up_id
        mirbase_id = mirbase_client.get_mirbase_id_from_hgnc_id(hgnc_id)
        if mirbase_id:
            db_refs['MIRBASE'] = mirbase_id

    elif ns in ('UNIPROT', 'UP'):
        up_id = None
        # This is a simple test to see if name is a valid UniProt ID,
        # if we can't get a mnemonic, we assume it's not a UP ID
        if uniprot_client.get_mnemonic(name, web_fallback=False):
            up_id = name
        # We next check if it's a mnemonic
        else:
            up_id_from_mnem = uniprot_client.get_id_from_mnemonic(name)
            if up_id_from_mnem:
                up_id = up_id_from_mnem
        if not up_id:
            logger.info('Couldn\'t get UP ID from %s' % name)
            return name, None
        db_refs = {'UP': up_id}
        hgnc_id = uniprot_client.get_hgnc_id(up_id)
        if hgnc_id:
            db_refs['HGNC'] = hgnc_id
            name = hgnc_client.get_hgnc_name(hgnc_id)
        else:
            name = uniprot_client.get_gene_name(up_id)
    elif ns == 'FPLX':
        db_refs = {'FPLX': name}
    elif ns in ('GO', 'GOBP', 'GOCC'):
        if name == 'cell proliferation':
            name = 'cell population proliferation'
        go_id = go_client.get_go_id_from_label(name)
        if not go_id:
            logger.info('Could not find GO ID for %s' % name)
            return name, None
        db_refs = {'GO': go_id}
        name = go_client.get_go_label(go_id)
    elif ns in ('MESHPP', 'MESHD', 'MESH'):
        mesh_id, mesh_name = mesh_client.get_mesh_id_name(name)
        if not mesh_id:
            logger.info('Could not find MESH ID from %s' % name)
            return name, None
        name = mesh_name
        db_refs = {'MESH': mesh_id}
    # For now, handle MGI/RGD but putting the name into the db_refs so
    # it's clear what namespace the name belongs to
    # FIXME: Full implementation would look up MGI/RGD identifiers from
    # the names, and obtain corresponding Uniprot IDs
    elif ns == 'MGI':
        up_id = mouse_lookup.get(name)
        if up_id:
            db_refs = {'UP': up_id}
    elif ns == 'RGD':
        up_id = rat_lookup.get(name)
        if up_id:
            db_refs = {'UP': up_id}
    # Map Selventa families and complexes to FamPlex
    elif ns == 'SFAM':
        db_refs = {'SFAM': name}
        indra_name = bel_to_indra.get(name)
        if indra_name is None:
            logger.info('Could not find mapping for BEL/SFAM family: '
                        '%s (%s)' % (name, node_data))
        else:
            db_refs['FPLX'] = indra_name
            name = indra_name
    elif ns == 'SCOMP':
        db_refs = {'SCOMP': name}
        indra_name = bel_to_indra.get(name)
        if indra_name is None:
            logger.info('Could not find mapping for BEL/SCOMP complex: '
                        '%s (%s)' % (name, node_data))
        else:
            db_refs['FPLX'] = indra_name
            name = indra_name
    # Map Entrez genes to HGNC/UP
    elif ns in ('EGID', 'ENTREZ', 'NCBIGENE'):
        hgnc_id = hgnc_client.get_hgnc_from_entrez(name)
        db_refs = {'EGID': name}
        if hgnc_id is not None:
            db_refs['HGNC'] = hgnc_id
            name = hgnc_client.get_hgnc_name(hgnc_id)
            up_id = hgnc_client.get_uniprot_id(hgnc_id)
            if up_id:
                db_refs['UP'] = up_id
            else:
                logger.info('HGNC entity %s with HGNC ID %s has no '
                            'corresponding Uniprot ID.',
                            name, hgnc_id)
            mirbase_id = mirbase_client.get_mirbase_id_from_hgnc_id(hgnc_id)
            if mirbase_id:
                db_refs['MIRBASE'] = mirbase_id
        else:
            logger.debug('Could not map EGID%s to HGNC.' % name)
            name = 'E%s' % name
    elif ns == 'MIRBASE':
        mirbase_id = mirbase_client.get_mirbase_id_from_mirbase_name(name)
        if not mirbase_id:
            logger.info('Could not map miRBase name %s to ID', name)
            return name, None
        db_refs = {'MIRBASE': mirbase_id}
        hgnc_id = mirbase_client.get_hgnc_id_from_mirbase_id(mirbase_id)
        if hgnc_id:
            db_refs['HGNC'] = hgnc_id
            name = hgnc_client.get_hgnc_name(hgnc_id)
    # CHEBI
    elif ns == 'CHEBI':
        # We first look up BEL's own namespace map for ChEBI names to IDs
        chebi_id = chebi_name_id.get(name)
        # If that fails, we look up INDRA's ChEBI name to ID mapping
        if not chebi_id:
            chebi_id = chebi_client.get_chebi_id_from_name(name)
        if chebi_id:
            db_refs = {'CHEBI': chebi_id}
        else:
            logger.info('CHEBI name %s not found in map.' % name)
    # These appear in the name slot but are actually IDs
    elif ns == 'CHEBIID':
        chebi_id = identifiers.ensure_chebi_prefix(name)
        db_refs = {'CHEBI': chebi_id}
        name = chebi_client.get_chebi_name_from_id(chebi_id)
    # SDIS, SCHEM: Include the name as the ID for the namespace
    elif ns in ('SDIS', 'SCHEM', 'TEXT'):
        db_refs = {ns: name}
    elif ns == 'TAX':
        tid = taxonomy_client.get_taxonomy_id(name)
        if tid:
            db_refs = {'TAXONOMY': tid}
        else:
            logger.info('Could not get taxonomy ID for %s' % name)
    else:
        logger.info("Unhandled namespace: %s: %s (%s)" % (ns, name,
                                                          node_data))
    return name, db_refs


def get_db_refs_by_ident(ns, ident, node_data):
    """Return standard name and grounding based on a namespace and an ID.

    Parameters
    ----------
    ns : str
        A name space in which the given identifier is interpreted.
    ident : str
        The identifier in the given name space to get grounding for.
    node_data : pybel.dsl.BaseAbundance
        Node data for logging purposes.

    Returns
    -------
    name : str
        The standardized name for the given entity.
    db_refs : dict
        The grounding for the given entity.

    """
    ns_list = ['HGNC', 'UNIPROT', 'UP', 'FPLX', 'GO', 'GOBP', 'GOCC',
               'MESHPP', 'MESHD', 'MESH', 'MGI', 'RGD', 'SFAM', 'EGID',
               'ENTREZ', 'NCBIGENE', 'MIRBASE', 'CHEBI', 'ECCODE' 'SDIS',
               'SCHEM', 'TEXT', 'DOID', 'EFO', 'HP', 'PFAM', 'ECCODE',
               'HGNC.GENEFAMILY', 'HGNC_GROUP', 'NCBITAXON', 'PUBCHEM']
    ns_mappings = {'UNIPROT': 'UP',
                   'GOBP': 'GO',
                   'GOCC': 'GO',
                   'MESHPP': 'MESH',
                   'MESHD': 'MESH',
                   'ENTREZ': 'EGID',
                   'NCBIGENE': 'EGID',
                   'NCBITAXON': 'TAXONOMY',
                   'HGNC.GENEFAMILY': 'HGNC_GROUP',
                   'CHEBIID': 'CHEBI'}
    raw_name = node_data.name
    if ns in ns_list:
        mapped_ns = ns_mappings.get(ns, ns)
        raw_db_refs = {mapped_ns: ident}
        std_name, std_db_refs = standardize_name_db_refs(raw_db_refs)
        if std_name is None:
            std_name = raw_name
        if std_db_refs is None:
            std_db_refs = raw_db_refs
    else:
        logger.info("Unhandled namespace %s with name %s and "
                    "identifier %s (%s)." % (ns, raw_name, ident, node_data))
        std_name = raw_name
        std_db_refs = None
    return std_name, std_db_refs


def extract_context(annotations, annot_manager):
    """Return a BioContext object extracted from the annotations.

    The entries that are extracted into the BioContext are popped from the
    annotations.

    Parameters
    ----------
    annotations : dict
        PyBEL annotations dict
    annot_manager : AnnotationManager
        An annotation manager to get name/db reference mappings for each ot the
        annotation types.

    Returns
    -------
    bc : BioContext
        An INDRA BioContext object
    """
    def get_annot(annotations, key):
        """Return a specific annotation given a key."""
        val_list = annotations.pop(key, None)
        if val_list:
            if len(val_list) > 1:
                logger.warning('More than one "%s" in annotations' % key)
            elif not val_list:
                return None
            return val_list[0].identifier
        return None

    bc = BioContext()
    species = get_annot(annotations, 'Species')
    if species:
        name = annot_manager.get_mapping('Species', species)
        bc.species = RefContext(name=name, db_refs={'TAXONOMY': species})

    mappings = (('CellLine', 'cell_line', None),
                ('Disease', 'disease', None),
                ('Anatomy', 'organ', None),
                ('Cell', 'cell_type', None),
                ('CellStructure', 'location', 'MESH'))
    for bel_name, indra_name, ns in mappings:
        ann = get_annot(annotations, bel_name)
        if ann:
            ref = annot_manager.get_mapping(bel_name, ann)
            if ref is None:
                continue
            if not ns:
                db_ns, db_id = ref.split('_', 1)
            else:
                db_ns, db_id = ns, ref
            if db_ns == 'CLO':
                db_ns = 'CL'
            if db_ns in {'CL', 'UBERON', 'DOID'}:
                db_id = identifiers.ensure_prefix(db_ns, db_id)
            setattr(bc, indra_name,
                    RefContext(name=ann, db_refs={db_ns: db_id}))
    # Overwrite blank BioContext
    if not bc:
        bc = None
    return bc


def _rel_is_direct(d):
    return d[pc.RELATION] in (pc.DIRECTLY_INCREASES, pc.DIRECTLY_DECREASES)


def _get_up_id(hgnc_id):
    hgnc_id = str(hgnc_id)
    up_id = hgnc_client.get_uniprot_id(hgnc_id)
    if not up_id:
        logger.info("No Uniprot ID for HGNC ID %s" % hgnc_id)
        return None
    if ',' in up_id:
        return None
    return up_id


class AnnotationManager(object):
    def __init__(self, annotation_urls):
        self.resources = {}
        for key, url in annotation_urls.items():
            res = get_bel_resource(url)
            self.resources[key] = res

        self.failures = defaultdict(set)

    def get_mapping(self, key, value):
        resource = self.resources.get(key)
        if resource is None:
            return None

        term = resource['Values'].get(value)
        if term is not None:
            return term

        logger.warning('unhandled annotation: %s:%s',
                       key, value)
        self.failures[key].add(value)


def _get_mods_and_muts(node_data: dsl.CentralDogma):
    """Get all modifications and mutations on the PyBEL node.

    Parameters
    ----------
    node_data : pybel.dsl.CentralDogma
        A PyBEL node

    Returns
    -------
    mods : List[ModCondition]
        A list of modifications to the given abundance
    muts : List[MutCondition]
        A list of mutations to the given abundance
    """
    mods = []
    muts = []
    variants = node_data.get(pc.VARIANTS)
    if not variants:
        return mods, muts

    for var in variants:
        if isinstance(var, dsl.Hgvs):
            if isinstance(node_data, dsl.Gene):
                logger.debug('Unhandled genetic variant: %s', node_data)
                continue

            hgvs_str = var.variant
            position, res_from, res_to = _parse_mutation(hgvs_str)
            if position is None and res_from is None and res_to is None:
                logger.info("Could not parse HGVS string %s", hgvs_str)
            else:
                mut_cond = MutCondition(position, res_from, res_to)
                muts.append(mut_cond)

        elif isinstance(var, dsl.ProteinModification):
            var_ns = var.entity.namespace
            if var_ns == 'go':
                mod_type = _pybel_indra_pmod_map.get(var.entity)
                if mod_type is None:
                    logger.info("Unhandled modification type %s (%s)",
                                var.entity.name, node_data)
                    continue
                mc = ModCondition(mod_type, var.get(pc.PMOD_CODE),
                                  var.get(pc.PMOD_POSITION))
                mods.append(mc)
        # FIXME These unhandled mod types should result in throwing out
        # the node (raise, or return None)
        elif isinstance(var, dsl.GeneModification):
            logger.debug('Unhandled node variant GMOD: %s', node_data)
        elif isinstance(var, dsl.Fragment):
            logger.debug('Unhandled node variant FRAG: %s', node_data)
        else:
            logger.debug('Unknown node variant type: %s', node_data)
    return mods, muts


def _get_activity_condition(node_modifier_data):
    if node_modifier_data is None or node_modifier_data == {}:
        return None
    modifier = node_modifier_data.get(pc.MODIFIER)
    if modifier is None or modifier != pc.ACTIVITY:
        return None
    effect = node_modifier_data.get(pc.EFFECT)
    # No specific effect, just return generic activity
    if not effect:
        return ActivityCondition('activity', True)

    activity_ns = effect.namespace
    if activity_ns == 'go':
        activity_type = _pybel_indra_act_map.get(effect)
        # If an activity type in BEL/PyBEL that is not implemented in INDRA,
        # return generic activity
        if activity_type is None:
            return ActivityCondition('activity', True)
        return ActivityCondition(activity_type, True)
    # If an unsupported namespace, simply return generic activity
    return ActivityCondition('activity', True)


def _get_translocation_target(node_modifier_data):
    # First check if there is a translocation modifier
    if node_modifier_data is None or node_modifier_data == {}:
        return None
    modifier = node_modifier_data.get(pc.MODIFIER)
    if modifier is None or modifier != pc.TRANSLOCATION:
        return None
    # Next, make sure there is information on the translocation target
    transloc_data = node_modifier_data.get(pc.EFFECT)
    if transloc_data is None:
        return None
    to_loc_info = transloc_data.get(pc.TO_LOC)
    if not to_loc_info:
        return None
    to_loc_ns = to_loc_info.namespace
    to_loc_id = to_loc_info.identifier
    to_loc_name = to_loc_info.name
    # Only use GO Cellular Component location names
    if to_loc_ns not in ('GO', 'GOCC', 'GOCCID') or (not to_loc_name and not to_loc_id):
        return None
    return go_client.get_valid_location(to_loc_id or to_loc_name)


def _has_unhandled_modifiers(node_modifier_data):
    # First check if there is a translocation modifier
    if node_modifier_data is None or node_modifier_data == {}:
        return False
    mod = node_modifier_data.get(pc.MODIFIER)
    if mod is None:
        return False
    if mod in (pc.CELL_SECRETION, pc.CELL_SURFACE_EXPRESSION):
        logger.info("Unhandled node modifier data: %s", node_modifier_data)
        return True


def _proteins_match(u_data, v_data):
    return (
        isinstance(u_data, dsl.Protein) and
        isinstance(v_data, dsl.Protein) and
        u_data.namespace and
        v_data.namespace and
        u_data.name and
        v_data.name and
        u_data.namespace == v_data.namespace and
        u_data.name == v_data.name
    )


_hgvs_protein_mutation = re.compile(r'^p.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})')


def _parse_mutation(s):
    m = _hgvs_protein_mutation.match(s)
    if not m:
        return None, None, None
    from_aa, position, to_aa = m.groups()
    return position, from_aa, to_aa


def _build_famplex_map():
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         os.pardir, os.pardir, 'resources',
                         'famplex_map.tsv')
    bel_to_indra = {}
    csv_rows = read_unicode_csv(fname, delimiter='\t')
    for row in csv_rows:
        namespace = row[0]
        entry = row[1]
        indra_name = row[2]
        if namespace == 'BEL':
            bel_to_indra[entry] = indra_name
    return bel_to_indra


def _build_chebi_map():
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         os.pardir, os.pardir, 'resources',
                         'bel_chebi_map.tsv')
    chebi_name_id = {}
    csv_rows = read_unicode_csv(fname, delimiter='\t')
    for row in csv_rows:
        chebi_name = row[0]
        chebi_id = row[1]
        chebi_name_id[chebi_name] = chebi_id
    return chebi_name_id


bel_to_indra = _build_famplex_map()
chebi_name_id = _build_chebi_map()


mouse_lookup = {gene_name: up_id for up_id, gene_name in
                uniprot_client.um.uniprot_gene_name.items()
                if uniprot_client.is_mouse(up_id)}

rat_lookup = {gene_name: up_id for up_id, gene_name in
              uniprot_client.um.uniprot_gene_name.items()
              if uniprot_client.is_rat(up_id)}
