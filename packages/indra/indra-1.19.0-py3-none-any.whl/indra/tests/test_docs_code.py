"""tests the code found in the documentation

Any code changed in here needs to be updated in their place in the
documentation and vice versa, since we are copy pasting code between its
occurence to the tests.

In general, try to separate tests to one test per chunk of interdependent code
"""
import copy
from indra.statements import Event, Concept, Influence, Evidence
from nose.plugins.attrib import attr
from unittest import skip


def _get_gene_network_stmts():
    from indra.tools.gene_network import GeneNetwork
    gn = GeneNetwork(['H2AX'])
    return gn.get_statements()


gn_stmts = _get_gene_network_stmts()

# CODE IN README.md #

# From stmt assembly pipeline description in README.md
def test_readme_pipeline():
    stmts = gn_stmts  # Added only here, not in docs
    from indra.tools import assemble_corpus as ac
    stmts = ac.filter_no_hypothesis(stmts)
    stmts = ac.map_grounding(stmts)
    stmts = ac.filter_grounded_only(stmts)
    stmts = ac.filter_human_only(stmts)
    stmts = ac.map_sequence(stmts)
    stmts = ac.run_preassembly(stmts, return_toplevel=False)
    stmts = ac.filter_belief(stmts, 0.8)
    assert stmts, 'Update example to yield statements list of non-zero length'


# From description of wm stmt assembly pipeline in README.md
def test_readme_wm_pipeline():
    from indra.tools import assemble_corpus as ac
    from indra.belief.wm_scorer import get_eidos_scorer
    from indra.ontology.world import world_ontology
    stmts = wm_raw_stmts
    # stmts = ac.filter_grounded_only(stmts)  # Does not work on test stmts
    belief_scorer = get_eidos_scorer()
    stmts = ac.run_preassembly(stmts,
                               return_toplevel=False,
                               belief_scorer=belief_scorer,
                               ontology=world_ontology,
                               normalize_opposites=True,
                               normalize_ns='WM')
    stmts = ac.filter_belief(stmts, 0.8)    # Apply belief cutoff of e.g., 0.8
    assert stmts, 'Update example to yield statements list of non-zero length'


# From 1st example under "Using INDRA"
def test_readme_using_indra1():
    from indra.sources import trips
    from indra.assemblers.pysb import PysbAssembler
    pa = PysbAssembler()
    # Process a natural language description of a mechanism
    trips_processor = trips.process_text(
        'MEK2 phosphorylates ERK1 at Thr-202 and Tyr-204')
    # Collect extracted mechanisms in PysbAssembler
    pa.add_statements(trips_processor.statements)
    # Assemble the model
    model = pa.make_model(policies='two_step')
    assert model


# From 2nd example under "Using INDRA"
@attr('notravis')  # This test takes 10+ minutes, stalling Travis
def test_readme_using_indra2():
    from indra.sources import reach
    reach_processor = reach.process_pmc('3717945', url=reach.local_nxml_url)
    assert reach_processor.statements


# From 3rd example under "Using INDRA"
@attr('slow', 'notravis')
def test_readme_using_indra3():
    from indra.sources import reach
    from indra.literature import pubmed_client
    # Search for 10 most recent abstracts in PubMed on 'BRAF'
    pmids = pubmed_client.get_ids('BRAF', retmax=10)
    all_statements = []
    for pmid in pmids:
        abs = pubmed_client.get_abstract(pmid)
        if abs is not None:
            reach_processor = reach.process_text(abs, url=reach.local_text_url)
            if reach_processor is not None:
                all_statements += reach_processor.statements
    assert len(all_statements) > 0


# From 4th example under "Using INDRA"
@attr('slow')
def test_readme_using_indra4():
    from indra.sources import bel
    # Process the neighborhood of BRAF and MAP2K1
    bel_processor = bel.process_pybel_neighborhood(['BRAF', 'MAP2K1'])
    assert bel_processor.statements


# From 5th example under "Using INDRA"
@attr('slow')
def test_readme_using_indra5():
    from indra.sources import biopax
    # Process the neighborhood of BRAF and MAP2K1
    biopax_processor = biopax.process_pc_pathsfromto(['BRAF', 'RAF1'],
                                                     ['MAP2K1', 'MAP2K2'])
    assert biopax_processor.statements


# CODE IN nl_modeling.rst #
def test_nl_modeling():
    # 1 code chunk
    from indra.sources import trips
    model_text = 'MAP2K1 phosphorylates MAPK1 and DUSP6 dephosphorylates MAPK1.'
    tp = trips.process_text(model_text)

    # 2nd code chunk
    for st in tp.statements:
        assert st.evidence[0].text  # Replaces a print statement in the doc

    # 3rd code chunk
    from indra.assemblers.pysb import PysbAssembler
    pa = PysbAssembler()
    pa.add_statements(tp.statements)
    pa.make_model(policies='two_step')

    # 4th code chunk
    for monomer in pa.model.monomers:
        assert monomer  # This replaces a print statements in the doc

    # 5th code chunk
    for rule in pa.model.rules:
        assert rule  # This replaces a print statements in the doc

    # 6th code chunk
    for parameter in pa.model.parameters:
        assert parameter  # This replaces a print statements in the doc

    # 7th code chunk
    for annotation in pa.model.annotations:
        assert annotation  # This replaces a print statements in the doc

    # 8th code chunk (this code is currently in a commented out section)
    pa.set_context('A375_SKIN')
    for monomer_pattern, parameter in pa.model.initial_conditions:
        assert monomer_pattern
        assert parameter.value

    # 9th code chunk
    _ = pa.export_model('sbml')
    assert _
    _ = pa.export_model('bngl')
    assert _

    # 10th code chunk
    # pa.export_model('sbml', 'example_model.sbml')  # Don't save file


# CODE IN gene_network.rst
@attr('slow', 'notravis')
def test_gene_network():
    # Chunk 1: this is tested in _get_gene_network_stmts
    # from indra.tools.gene_network import GeneNetwork
    # gn = GeneNetwork(['H2AX'])
    # biopax_stmts = gn.get_biopax_stmts()
    # bel_stmts = gn.get_bel_stmts()

    # Chunk 2
    from indra import literature
    pmids = literature.pubmed_client.get_ids_for_gene('H2AX')

    # Chunk 3
    from indra import literature
    paper_contents = {}
    for pmid in pmids:
        content, content_type = literature.get_full_text(pmid, 'pmid')
        if content_type == 'abstract':
            paper_contents[pmid] = content
        if len(paper_contents) == 5:  # Is 10 in actual code
            break

    # Chunk 4
    from indra.sources import reach

    literature_stmts = []
    for pmid, content in paper_contents.items():
        rp = reach.process_text(content, url=reach.local_text_url)
        literature_stmts += rp.statements
    print('Got %d statements' % len(literature_stmts))
    assert literature_stmts  # replaces a print statements

    # Chunk 6
    from indra.tools import assemble_corpus as ac
    # stmts = biopax_stmts + bel_stmts + literature_stmts  # tested elsewhere
    stmts = gn_stmts + literature_stmts  # Added instead of above line
    stmts = ac.map_grounding(stmts)
    stmts = ac.map_sequence(stmts)
    stmts = ac.run_preassembly(stmts)
    assert stmts

    # Chunk 7
    from indra.assemblers.cx import CxAssembler
    from indra.databases import ndex_client
    cxa = CxAssembler(stmts)
    cx_str = cxa.make_model()
    assert cx_str

    # Chunk 8
    # ndex_cred = {'user': 'myusername', 'password': 'xxx'}
    # network_id = ndex_client.create_network(cx_str, ndex_cred)
    # print(network_id)

    # Chunk 9
    from indra.assemblers.indranet import IndraNetAssembler
    indranet_assembler = IndraNetAssembler(statements=stmts)
    indranet = indranet_assembler.make_model()
    assert len(indranet.nodes) > 0, 'indranet conatins no nodes'
    assert len(indranet.edges) > 0, 'indranet conatins no edges'

    # Chunk 10
    import networkx as nx
    paths = nx.single_source_shortest_path(G=indranet, source='H2AX',
                                           cutoff=1)
    assert paths

    # Chunk 11
    from indra.assemblers.pysb import PysbAssembler
    pysb = PysbAssembler(statements=stmts)
    pysb_model = pysb.make_model()
    assert pysb_model


# CODE IN getting_started.rst
def test_getting_started1_2():
    # Chunks 1 & 2
    from indra.sources import bel
    from indra.assemblers.pysb import PysbAssembler
    assert bel
    assert PysbAssembler


def test_getting_started3():
    # Chunk 3
    from indra.sources import trips
    sentence = 'MAP2K1 phosphorylates MAPK3 at Thr-202 and Tyr-204'
    trips_processor = trips.process_text(sentence)
    assert trips_processor.statements


@skip('Same as test_readme_using_indra2')
def test_getting_started4():
    # Chunk 4
    from indra.sources import reach
    reach_processor = reach.process_pmc('3717945')
    assert reach_processor.statements


@attr('slow')
def test_getting_started5():
    # Chunk 5
    from indra.sources import bel
    bel_processor = bel.process_pybel_neighborhood(['KRAS', 'BRAF'])
    assert bel_processor.statements


def test_getting_started6():
    # Chunk 6
    from indra.statements import Phosphorylation, Agent
    braf = Agent('BRAF')
    map2k1 = Agent('MAP2K1')
    stmt = Phosphorylation(braf, map2k1)
    assert stmt


@attr('notravis')
def test_getting_started7_8():
    # Chunk 7
    stmts = gn_stmts  # Added only in this test, not in docs
    from indra.assemblers.pysb import PysbAssembler
    pa = PysbAssembler()
    pa.add_statements(stmts)
    model = pa.make_model()
    assert model

    # Chunk 8
    sbml_model = pa.export_model('sbml')
    assert sbml_model


def test_getting_started9_10():
    # Chunk 9
    # pa.export_model('sbml', file_name='model.sbml')

    # Chunk 10
    from indra.assemblers.indranet import IndraNetAssembler
    indranet_assembler = IndraNetAssembler(statements=gn_stmts)
    indranet = indranet_assembler.make_model()
    assert len(indranet.nodes) > 0, 'indranet contains no nodes'
    assert len(indranet.edges) > 0, 'indranet contains no edges'

    # Chunk 11
    signed_graph = indranet.to_signed_graph()
    assert len(signed_graph.nodes) > 0, 'signed graph contains no nodes'
    assert len(signed_graph.edges) > 0, 'signed graph conatins no edges'


def _make_wm_stmts():
    ev1 = Evidence(source_api='eidos', text='A',
                   annotations={'found_by': 'ported_syntax_1_verb-Causal'})
    ev2 = Evidence(source_api='eidos', text='B',
                   annotations={'found_by': 'dueToSyntax2-Causal'})
    ev3 = Evidence(source_api='hume', text='C')
    ev4 = Evidence(source_api='cwms', text='D')
    ev5 = Evidence(source_api='sofia', text='E')
    ev6 = Evidence(source_api='sofia', text='F')
    x = Event(Concept('x', db_refs={'TEXT': 'dog'}))
    y = Event(Concept('y', db_refs={'TEXT': 'cat'}))
    stmt1 = Influence(x, y, evidence=[ev1, ev2])
    stmt2 = Influence(x, y, evidence=[ev1, ev3])
    stmt3 = Influence(x, y, evidence=[ev3, ev4, ev5])
    stmt4 = Influence(x, y, evidence=[ev5])
    stmt5 = Influence(x, y, evidence=[ev6])
    stmt1.uuid = '1'
    stmt2.uuid = '2'
    stmt3.uuid = '3'
    stmt4.uuid = '4'
    stmt5.uuid = '5'
    stmts = [stmt1, stmt2, stmt3, stmt4]
    return stmts


wm_raw_stmts = _make_wm_stmts()
