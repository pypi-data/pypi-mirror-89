import os

from indra.preassembler import Preassembler, render_stmt_graph, \
    flatten_evidence, flatten_stmts, bio_ontology_refinement_filter
from indra.sources import reach
from indra.statements import *
from indra.ontology.bio import bio_ontology
from indra.ontology.world import world_ontology


def test_duplicates():
    src = Agent('SRC', db_refs = {'HGNC': '11283'})
    ras = Agent('RAS', db_refs = {'FA': '03663'})
    st1 = Phosphorylation(src, ras)
    st2 = Phosphorylation(src, ras)
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    pa.combine_duplicates()
    assert len(pa.unique_stmts) == 1


def test_duplicates_copy():
    src = Agent('SRC', db_refs = {'HGNC': '11283'})
    ras = Agent('RAS', db_refs = {'FA': '03663'})
    st1 = Phosphorylation(src, ras, evidence=[Evidence(text='Text 1')])
    st2 = Phosphorylation(src, ras, evidence=[Evidence(text='Text 2')])
    stmts = [st1, st2]
    pa = Preassembler(bio_ontology, stmts=stmts)
    pa.combine_duplicates()
    assert len(pa.unique_stmts) == 1
    assert len(stmts) == 2
    assert len(stmts[0].evidence) == 1
    assert len(stmts[1].evidence) == 1


def test_duplicates_sorting():
    mc = ModCondition('phosphorylation')
    map2k1_1 = Agent('MAP2K1', mods=[mc])
    mc1 = ModCondition('phosphorylation', 'serine', '218')
    mc2 = ModCondition('phosphorylation', 'serine', '222')
    mc3 = ModCondition('phosphorylation', 'serine', '298')
    map2k1_2 = Agent('MAP2K1', mods=[mc1, mc2, mc3])
    mapk3 = Agent('MAPK3')
    st1 = Phosphorylation(map2k1_1, mapk3, position='218')
    st2 = Phosphorylation(map2k1_2, mapk3)
    st3 = Phosphorylation(map2k1_1, mapk3, position='218')
    stmts = [st1, st2, st3]
    pa = Preassembler(bio_ontology, stmts=stmts)
    pa.combine_duplicates()
    assert len(pa.unique_stmts) == 2


def test_combine_duplicates():
    raf = Agent('RAF1')
    mek = Agent('MEK1')
    erk = Agent('ERK2')
    p1 = Phosphorylation(raf, mek,
            evidence=Evidence(text='foo'))
    p2 = Phosphorylation(raf, mek,
            evidence=Evidence(text='bar'))
    p3 = Phosphorylation(raf, mek,
            evidence=Evidence(text='baz'))
    p4 = Phosphorylation(raf, mek,
            evidence=Evidence(text='beep'))
    p5 = Phosphorylation(mek, erk,
            evidence=Evidence(text='foo2'))
    p6 = Dephosphorylation(mek, erk,
            evidence=Evidence(text='bar2'))
    p7 = Dephosphorylation(mek, erk,
            evidence=Evidence(text='baz2'))
    p8 = Dephosphorylation(mek, erk,
            evidence=Evidence(text='beep2'))
    p9 = Dephosphorylation(Agent('SRC'), Agent('KRAS'),
                           evidence=Evidence(text='beep'))
    stmts = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
    pa = Preassembler(bio_ontology, stmts=stmts)
    pa.combine_duplicates()
    # The statements come out sorted by their matches_key
    assert len(pa.unique_stmts) == 4, len(pa.unique_stmts)
    num_evs =[len(s.evidence) for s in pa.unique_stmts]
    assert pa.unique_stmts[0].matches(p6) # MEK dephos ERK
    assert num_evs[0] == 3, num_evs[0]
    assert pa.unique_stmts[1].matches(p9) # SRC dephos KRAS
    assert num_evs[1] == 1, num_evs[1]
    assert pa.unique_stmts[2].matches(p5) # MEK phos ERK
    assert num_evs[2] == 1, num_evs[2]
    assert pa.unique_stmts[3].matches(p1) # RAF phos MEK
    assert num_evs[3] == 4, num_evs[3]


def test_combine_evidence_exact_duplicates():
    raf = Agent('RAF1')
    mek = Agent('MEK1')
    p1 = Phosphorylation(raf, mek,
            evidence=Evidence(text='foo'))
    p2 = Phosphorylation(raf, mek,
            evidence=Evidence(text='bar'))
    p3 = Phosphorylation(raf, mek,
            evidence=Evidence(text='bar'))
    stmts = [p1, p2, p3]
    pa = Preassembler(bio_ontology, stmts=stmts)
    pa.combine_duplicates()
    # The statements come out sorted by their matches_key
    assert len(pa.unique_stmts) == 1
    assert len(pa.unique_stmts[0].evidence) == 2
    assert set(ev.text for ev in pa.unique_stmts[0].evidence) == \
        set(['foo', 'bar'])


def test_combine_evidence_exact_duplicates_different_raw_text():
    raf1 = Agent('RAF1', db_refs={'TEXT': 'Raf'})
    raf2 = Agent('RAF1', db_refs={'TEXT': 'RAF'})
    mek = Agent('MEK1')
    p1 = Phosphorylation(raf1, mek,
            evidence=Evidence(text='foo'))
    p2 = Phosphorylation(raf1, mek,
            evidence=Evidence(text='bar'))
    p3 = Phosphorylation(raf2, mek,
            evidence=Evidence(text='bar'))
    stmts = [p1, p2, p3]
    pa = Preassembler(bio_ontology, stmts=stmts)
    pa.combine_duplicates()
    # The statements come out sorted by their matches_key
    assert len(pa.unique_stmts) == 1
    assert len(pa.unique_stmts[0].evidence) == 3
    assert set(ev.text for ev in pa.unique_stmts[0].evidence) == \
        set(['foo', 'bar', 'bar'])


def test_superfamily_refinement():
    """A gene-level statement should be supported by a family-level
    statement."""
    src = Agent('SRC', db_refs = {'HGNC': '11283'})
    ras = Agent('RAS', db_refs = {'FPLX': 'RAS'})
    nras = Agent('NRAS', db_refs = {'HGNC': '7989'})
    st1 = Phosphorylation(src, ras, 'tyrosine', '32')
    st2 = Phosphorylation(src, nras, 'tyrosine', '32')
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    stmts = pa.combine_related()
    # The top-level list should contain only one statement, the gene-level
    # one, supported by the family one.
    assert len(stmts) == 1
    assert (stmts[0].equals(st2))
    assert (len(stmts[0].supported_by) == 1)
    assert (stmts[0].supported_by[0].equals(st1))


def test_superfamily_refinement_isa_or_partof():
    src = Agent('SRC', db_refs = {'HGNC': '11283'})
    prkag1 = Agent('PRKAG1', db_refs = {'HGNC': '9385'})
    ampk = Agent('AMPK', db_refs = {'FPLX': 'AMPK'})
    st1 = Phosphorylation(src, ampk, 'tyrosine', '32')
    st2 = Phosphorylation(src, prkag1, 'tyrosine', '32')
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    stmts = pa.combine_related()
    # The top-level list should contain only one statement, the gene-level
    # one, supported by the family one.
    assert len(stmts) == 1
    assert stmts[0].equals(st2)
    assert len(stmts[0].supported_by) == 1
    assert stmts[0].supported_by[0].equals(st1)


def test_modification_refinement():
    """A more specific modification statement should be supported by a more
    generic modification statement."""
    src = Agent('SRC', db_refs = {'HGNC': '11283'})
    nras = Agent('NRAS', db_refs = {'HGNC': '7989'})
    st1 = Phosphorylation(src, nras, 'tyrosine', '32')
    st2 = Phosphorylation(src, nras)
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    stmts = pa.combine_related()
    # The top-level list should contain only one statement, the more specific
    # modification, supported by the less-specific modification.
    assert len(stmts) == 1
    assert stmts[0].equals(st1)
    assert len(stmts[0].supported_by) == 1
    assert stmts[0].supported_by[0].equals(st2)


def test_modification_refinement_residue_noenz():
    erbb3 = Agent('Erbb3')
    st1 = Phosphorylation(None, erbb3)
    st2 = Phosphorylation(None, erbb3, 'Y')
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    pa.combine_related()
    assert len(pa.related_stmts) == 1


def test_modification_refinement_noenz():
    """A more specific modification statement should be supported by a more
    generic modification statement."""
    src = Agent('SRC', db_refs = {'HGNC': '11283'})
    nras = Agent('NRAS', db_refs = {'HGNC': '7989'})
    st1 = Phosphorylation(src, nras, 'tyrosine', '32')
    st2 = Phosphorylation(None, nras, 'tyrosine', '32')
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    stmts = pa.combine_related()
    # The top-level list should contain only one statement, the more specific
    # modification, supported by the less-specific modification.
    assert len(stmts) == 1
    assert stmts[0].equals(st1)
    assert len(stmts[0].supported_by) == 1
    assert stmts[0].supported_by[0].equals(st2)
    assert stmts[0].supported_by[0].supports[0].equals(st1)


def test_modification_refinement_noenz2():
    """A more specific modification statement should be supported by a more
    generic modification statement.

    Similar to test_modification_refinement_noenz for statements where one
    argument is associated with a component in the hierarchy (SIRT1 in this
    case) but the other is not (BECN1).
    """
    sirt1 = Agent('SIRT1', db_refs={'HGNC':'14929', 'UP':'Q96EB6',
                                    'TEXT':'SIRT1'})
    becn1 = Agent('BECN1', db_refs={'HGNC': '1034', 'UP': 'Q14457',
                                    'TEXT': 'Beclin 1'})
    st1 = Deacetylation(sirt1, becn1)
    st2 = Deacetylation(None, becn1)
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    stmts = pa.combine_related()
    # The top-level list should contain only one statement, the more specific
    # modification, supported by the less-specific modification.
    assert (len(stmts) == 1)
    assert (stmts[0].equals(st1))
    assert (len(stmts[0].supported_by) == 1)
    assert (stmts[0].supported_by[0].equals(st2))
    assert (stmts[0].supported_by[0].supports[0].equals(st1))


def test_modification_norefinement_noenz():
    """A more specific modification statement should be supported by a more
    generic modification statement."""
    src = Agent('SRC', db_refs = {'HGNC': '11283'})
    nras = Agent('NRAS', db_refs = {'HGNC': '7989'})
    st1 = Phosphorylation(src, nras)
    st2 = Phosphorylation(None, nras, 'Y', '32',
                          evidence=[Evidence(text='foo')])
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    stmts = pa.combine_related()
    # Modification is less specific, enzyme more specific in st1, therefore
    # these statements shouldn't be combined. 
    assert len(stmts) == 2
    assert len(stmts[1].evidence)==1


def test_modification_norefinement_subsfamily():
    """A more specific modification statement should be supported by a more
    generic modification statement."""
    src = Agent('SRC', db_refs = {'HGNC': '11283'})
    nras = Agent('NRAS', db_refs = {'HGNC': '7989'})
    ras = Agent('RAS', db_refs = {'FPLX': 'RAS'})
    st1 = Phosphorylation(src, nras)
    st2 = Phosphorylation(src, ras, 'Y', '32',
                          evidence=[Evidence(text='foo')])
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    stmts = pa.combine_related()
    # Modification is less specific, enzyme more specific in st1, therefore
    # these statements shouldn't be combined. 
    assert len(stmts) == 2
    assert len(stmts[0].evidence) == 1, stmts


def test_modification_norefinement_enzfamily():
    """A more specific modification statement should be supported by a more
    generic modification statement."""
    mek = Agent('MEK')
    raf = Agent('RAF')
    braf = Agent('BRAF')
    st1 = Phosphorylation(raf, mek, 'Y', '32',
                          evidence=[Evidence(text='foo')])
    st2 = Phosphorylation(braf, mek)
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    stmts = pa.combine_related()
    # Modification is less specific, enzyme more specific in st1, therefore
    # these statements shouldn't be combined. 
    assert len(stmts) == 2
    assert len(stmts[1].evidence)==1


def test_bound_condition_refinement():
    """A statement with more specific bound context should be supported by a
    less specific statement."""
    src = Agent('SRC', db_refs = {'HGNC': '11283'})
    gtp = Agent('GTP', db_refs = {'CHEBI': '15996'})
    nras = Agent('NRAS', db_refs = {'HGNC': '7989'})
    nrasgtp = Agent('NRAS', db_refs = {'HGNC': '7989'},
        bound_conditions=[BoundCondition(gtp, True)])
    st1 = Phosphorylation(src, nras, 'tyrosine', '32')
    st2 = Phosphorylation(src, nrasgtp, 'tyrosine', '32')
    # The top-level list should contain only one statement, the more specific
    # modification, supported by the less-specific modification.
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    stmts = pa.combine_related()
    assert len(stmts) == 1
    assert stmts[0].equals(st2)
    assert len(stmts[0].supported_by) == 1
    assert stmts[0].supported_by[0].equals(st1)


def test_bound_condition_norefinement():
    """A statement with more specific bound context should be supported by a
    less specific statement."""
    src = Agent('SRC', db_refs = {'HGNC': '11283'})
    gtp = Agent('GTP', db_refs = {'CHEBI': '15996'})
    nras = Agent('NRAS', db_refs = {'HGNC': '7989'})
    nrasgtp = Agent('NRAS', db_refs = {'HGNC': '7989'},
        bound_conditions=[BoundCondition(gtp, True)])
    st1 = Phosphorylation(src, nras, 'tyrosine', '32')
    st2 = Phosphorylation(src, nrasgtp)
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    stmts = pa.combine_related()
    # The bound condition is more specific in st2 but the modification is less
    # specific. Therefore these statements should not be combined.
    assert len(stmts) == 2


def test_bound_condition_deep_refinement():
    """A statement with more specific bound context should be supported by a
    less specific statement."""
    src = Agent('SRC', db_refs = {'HGNC': '11283'})
    gtp1 = Agent('GTP', db_refs = {'CHEBI': '15996'})
    gtp2 = Agent('GTP', mods=[ModCondition('phosphorylation')],
                 db_refs = {'CHEBI': '15996'})
    nrasgtp1 = Agent('NRAS', db_refs = {'HGNC': '7989'},
        bound_conditions=[BoundCondition(gtp1, True)])
    nrasgtp2 = Agent('NRAS', db_refs = {'HGNC': '7989'},
        bound_conditions=[BoundCondition(gtp2, True)])
    st1 = Phosphorylation(src, nrasgtp1, 'tyrosine', '32')
    st2 = Phosphorylation(src, nrasgtp2, 'tyrosine', '32')
    # The top-level list should contain only one statement, the more specific
    # modification, supported by the less-specific modification.
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    stmts = pa.combine_related()
    assert len(stmts) == 1
    assert stmts[0].equals(st2)
    assert len(stmts[0].supported_by) == 1
    assert stmts[0].supported_by[0].equals(st1)


def test_complex_refinement():
    ras = Agent('RAS')
    raf = Agent('RAF')
    mek = Agent('MEK')
    st1 = Complex([ras, raf])
    st2 = Complex([mek, ras, raf])
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    pa.combine_related()
    assert len(pa.unique_stmts) == 2
    assert len(pa.related_stmts) == 2


def test_complex_agent_refinement():
    ras = Agent('RAS')
    raf1 = Agent('RAF', mods=[ModCondition('ubiquitination', None, None, True)])
    raf2 = Agent('RAF', mods=[ModCondition('ubiquitination', None, None, False)])
    st1 = Complex([ras, raf1])
    st2 = Complex([ras, raf2])
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    pa.combine_related()
    assert len(pa.unique_stmts) == 2
    assert len(pa.related_stmts) == 2


def test_mod_sites_refinement():
    """A statement with more specific modification context should be supported
    by a less-specific statement."""
    # TODO
    assert True


def test_binding_site_refinement():
    """A statement with information about a binding site for an interaction
    between two proteins should be supported by a statement without this
    information."""
    # TODO
    assert True


def test_activating_substitution_refinement():
    """Should only be refinement if entities are a refinement and all
    fields match."""
    mc1 = MutCondition('12', 'G', 'D')
    mc2 = MutCondition('61', 'Q', 'L')
    nras1 = Agent('NRAS', mutations=[mc1], db_refs = {'HGNC': '7989'})
    nras2 = Agent('NRAS', mutations=[mc2], db_refs = {'HGNC': '7989'})
    ras = Agent('RAS', mutations=[mc1], db_refs={'FPLX': 'RAS'})
    st1 = ActiveForm(ras, 'gtpbound', True,
                     evidence=Evidence(text='bar'))
    st2 = ActiveForm(nras1, 'gtpbound', True,
                     evidence=Evidence(text='foo'))
    st3 = ActiveForm(nras2, 'gtpbound', True,
                     evidence=Evidence(text='bar'))
    st4 = ActiveForm(nras1, 'phosphatase', True,
                     evidence=Evidence(text='bar'))
    st5 = ActiveForm(nras1, 'gtpbound', False,
                     evidence=Evidence(text='bar'))
    assert st2.refinement_of(st1, bio_ontology)
    assert not st3.refinement_of(st1, bio_ontology)
    assert not st4.refinement_of(st1, bio_ontology)
    assert not st5.refinement_of(st1, bio_ontology)

    assert not st1.refinement_of(st2, bio_ontology)
    assert not st3.refinement_of(st2, bio_ontology)
    assert not st4.refinement_of(st2, bio_ontology)
    assert not st5.refinement_of(st2, bio_ontology)

    assert not st1.refinement_of(st3, bio_ontology)
    assert not st2.refinement_of(st3, bio_ontology)
    assert not st4.refinement_of(st3, bio_ontology)
    assert not st5.refinement_of(st3, bio_ontology)

    assert not st1.refinement_of(st4, bio_ontology)
    assert not st2.refinement_of(st4, bio_ontology)
    assert not st3.refinement_of(st4, bio_ontology)
    assert not st5.refinement_of(st4, bio_ontology)

    assert not st1.refinement_of(st5, bio_ontology)
    assert not st2.refinement_of(st5, bio_ontology)
    assert not st3.refinement_of(st5, bio_ontology)
    assert not st4.refinement_of(st5, bio_ontology)


def test_translocation():
    st1 = Translocation(Agent('AKT'), None, None)
    st2 = Translocation(Agent('AKT'), None, 'plasma membrane')
    st3 = Translocation(Agent('AKT'), None, 'nucleus')
    pa = Preassembler(bio_ontology, stmts=[st1, st2, st3])
    pa.combine_related()
    assert len(pa.related_stmts) == 2, pa.related_stmts


def test_grounding_aggregation():
    braf1 = Agent('BRAF', db_refs={'TEXT': 'braf', 'HGNC': '1097'})
    braf2 = Agent('BRAF', db_refs={'TEXT': 'BRAF'})
    braf3 = Agent('BRAF', db_refs={'TEXT': 'Braf', 'UP': 'P15056'})
    braf4 = Agent('BRAF', db_refs={'TEXT': 'B-raf', 'UP': 'P15056',
                                   'HGNC': '1097'})
    st1 = Phosphorylation(None, braf1)
    st2 = Phosphorylation(None, braf2)
    st3 = Phosphorylation(None, braf3)
    st4 = Phosphorylation(None, braf4)
    pa = Preassembler(bio_ontology, stmts=[st1, st2, st3, st4])
    unique_stmts = pa.combine_duplicates()
    assert len(unique_stmts) == 3, unique_stmts


def test_grounding_aggregation_complex():
    mek = Agent('MEK')
    braf1 = Agent('BRAF', db_refs={'TEXT': 'braf', 'HGNC': '1097'})
    braf2 = Agent('BRAF', db_refs={'TEXT': 'BRAF', 'dummy': 'dummy'})
    braf3 = Agent('BRAF', db_refs={'TEXT': 'Braf', 'UP': 'P15056'})
    st1 = Complex([mek, braf1])
    st2 = Complex([braf2, mek])
    st3 = Complex([mek, braf3])
    pa = Preassembler(bio_ontology, stmts=[st1, st2, st3])
    unique_stmts = pa.combine_duplicates()
    assert len(unique_stmts) == 3, unique_stmts


def test_render_stmt_graph():
    braf = Agent('BRAF', db_refs={'HGNC': '1097'})
    mek1 = Agent('MAP2K1', db_refs={'HGNC': '6840'})
    mek = Agent('MEK', db_refs={'FPLX':'MEK'})
    # Statements
    p0 = Phosphorylation(braf, mek)
    p1 = Phosphorylation(braf, mek1)
    p2 = Phosphorylation(braf, mek1, position='218')
    p3 = Phosphorylation(braf, mek1, position='222')
    p4 = Phosphorylation(braf, mek1, 'serine')
    p5 = Phosphorylation(braf, mek1, 'serine', '218')
    p6 = Phosphorylation(braf, mek1, 'serine', '222')
    stmts = [p0, p1, p2, p3, p4, p5, p6]
    pa = Preassembler(bio_ontology, stmts=stmts)
    pa.combine_related()
    graph = render_stmt_graph(pa.related_stmts, reduce=False)
    # One node for each statement
    assert len(graph.nodes()) == 7
    # Edges:
    # p0 supports p1-p6 = 6 edges
    # p1 supports p2-p6 = 5 edges
    # p2 supports p5 = 1 edge
    # p3 supports p6 = 1 edge
    # p4 supports p5-p6 = 2 edges
    # (p5 and p6 support none--they are top-level)
    # 6 + 5 + 1 + 1 + 2 = 15 edges
    assert len(graph.edges()) == 15


def test_flatten_evidence_hierarchy():
    braf = Agent('BRAF')
    mek = Agent('MAP2K1')
    st1 = Phosphorylation(braf, mek, evidence=[Evidence(text='foo')])
    st2 = Phosphorylation(braf, mek, 'S', '218',
                          evidence=[Evidence(text='bar')])
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    pa.combine_related()
    assert len(pa.related_stmts) == 1
    flattened = flatten_evidence(pa.related_stmts)
    assert len(flattened) == 1
    top_stmt = flattened[0]
    assert len(top_stmt.evidence) == 2
    assert 'bar' in [e.text for e in top_stmt.evidence]
    assert 'foo' in [e.text for e in top_stmt.evidence]
    assert len(top_stmt.supported_by) == 1
    supporting_stmt = top_stmt.supported_by[0]
    assert len(supporting_stmt.evidence) == 1
    assert supporting_stmt.evidence[0].text == 'foo'
    supporting_stmt.evidence[0].text = 'changed_foo'
    assert supporting_stmt.evidence[0].text == 'changed_foo'
    assert 'changed_foo' not in [e.text for e in top_stmt.evidence]
    assert 'foo' in [e.text for e in top_stmt.evidence]
    assert {ev.annotations.get('support_type') for ev in top_stmt.evidence} \
        == {'direct', 'supported_by'}


def test_flatten_evidence_multilevel():
    braf = Agent('BRAF')
    mek = Agent('MAP2K1')
    st1 = Phosphorylation(braf, mek, evidence=[Evidence(text='foo')])
    st2 = Phosphorylation(braf, mek, 'S',
                          evidence=[Evidence(text='bar')])
    st3 = Phosphorylation(braf, mek, 'S', '218',
                          evidence=[Evidence(text='baz')])
    pa = Preassembler(bio_ontology, stmts=[st1, st2, st3])
    pa.combine_related()
    assert len(pa.related_stmts) == 1
    flattened = flatten_evidence(pa.related_stmts)
    assert len(flattened) == 1
    top_stmt = flattened[0]
    assert len(top_stmt.evidence) == 3, len(top_stmt.evidence)
    anns = [ev.annotations['support_type'] for ev in top_stmt.evidence]
    assert anns.count('direct') == 1
    assert anns.count('supported_by') == 2


def test_flatten_evidence_hierarchy_supports():
    braf = Agent('BRAF')
    mek = Agent('MAP2K1')
    st1 = Phosphorylation(braf, mek, evidence=[Evidence(text='foo')])
    st2 = Phosphorylation(braf, mek, 'S', '218',
                          evidence=[Evidence(text='bar')])
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    pa_stmts = pa.combine_related(return_toplevel=False)
    assert len(pa_stmts) == 2
    flattened = flatten_evidence(pa_stmts, collect_from='supports')
    assert len(flattened) == 2
    top_stmt = flattened[1]
    assert len(top_stmt.evidence) == 1
    assert 'bar' in [e.text for e in top_stmt.evidence]
    assert len(top_stmt.supported_by) == 1
    supporting_stmt = top_stmt.supported_by[0]
    assert len(supporting_stmt.evidence) == 2
    assert set([e.text for e in supporting_stmt.evidence]) == {'foo', 'bar'}


def test_flatten_stmts():
    st1 = Phosphorylation(Agent('MAP3K5'), Agent('RAF1'), 'S', '338')
    st2 = Phosphorylation(None, Agent('RAF1'), 'S', '338')
    st3 = Phosphorylation(None, Agent('RAF1'))
    st4 = Phosphorylation(Agent('PAK1'), Agent('RAF1'), 'S', '338')
    st5 = Phosphorylation(None, Agent('RAF1'), evidence=Evidence(text='foo'))
    pa = Preassembler(bio_ontology, stmts=[st1, st2, st3, st4, st5])
    pa.combine_duplicates()
    pa.combine_related()
    assert len(pa.related_stmts) == 2
    assert len(flatten_stmts(pa.unique_stmts)) == 4
    assert len(flatten_stmts(pa.related_stmts)) == 4


def test_complex_refinement_order():
    st1 = Complex([Agent('MED23'), Agent('ELK1')])
    st2 = Complex([Agent('ELK1', mods=[ModCondition('phosphorylation')]),
                   Agent('MED23')])
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    pa.combine_duplicates()
    pa.combine_related()
    assert len(pa.related_stmts) == 1


def test_activation_refinement():
    subj = Agent('alcohol', db_refs={'CHEBI': 'CHEBI:16236',
                                     'HMDB': 'HMDB00108',
                                     'PUBCHEM': '702',
                                     'TEXT': 'alcohol'})
    obj = Agent('endotoxin', db_refs={'TEXT': 'endotoxin'})
    st1 = Inhibition(subj, obj)
    st2 = Activation(subj, obj)
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    pa.combine_duplicates()
    assert len(pa.unique_stmts) == 2
    pa.combine_related()
    assert len(pa.related_stmts) == 2


def test_homodimer_refinement():
    egfr = Agent('EGFR')
    erbb = Agent('ERBB2')
    st1 = Complex([erbb, erbb])
    st2 = Complex([erbb, egfr])
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    pa.combine_duplicates()
    assert len(pa.unique_stmts) == 2
    pa.combine_related()
    assert len(pa.related_stmts) == 2


def test_return_toplevel():
    src = Agent('SRC', db_refs = {'HGNC': '11283'})
    nras = Agent('NRAS', db_refs = {'HGNC': '7989'})
    st1 = Phosphorylation(src, nras, 'tyrosine', '32')
    st2 = Phosphorylation(src, nras)
    pa = Preassembler(bio_ontology, stmts=[st1, st2])
    stmts = pa.combine_related(return_toplevel=True)
    assert len(stmts) == 1
    assert len(stmts[0].supported_by) == 1
    assert len(stmts[0].supported_by[0].supports) == 1
    stmts = pa.combine_related(return_toplevel=False)
    assert len(stmts) == 2
    ix = 1 if stmts[0].residue else 0
    assert len(stmts[1-ix].supported_by) == 1
    assert len(stmts[1-ix].supported_by[0].supports) == 1
    assert len(stmts[ix].supports) == 1
    assert len(stmts[ix].supports[0].supported_by) == 1


def test_conversion_refinement():
    ras = Agent('RAS', db_refs={'FPLX': 'RAS'})
    hras = Agent('HRAS', db_refs={'HGNC': '5173'})
    gtp = Agent('GTP')
    gdp = Agent('GDP')
    st1 = Conversion(ras, gtp, gdp)
    st2 = Conversion(hras, gtp, gdp)
    st3 = Conversion(hras, [gtp, gdp], gdp)
    st4 = Conversion(hras, [gdp, gtp], gdp)
    pa = Preassembler(bio_ontology, stmts=[st1, st2, st3, st4])
    toplevel_stmts = pa.combine_related()
    assert len(toplevel_stmts) == 2


def test_influence_duplicate():
    gov = 'wm/concept/causal_factor/social_and_political/government'
    agr = 'wm/concept/causal_factor/agriculture/crop_production'
    cgov = Event(Concept('government', db_refs={'WM': [(gov, 1.0)]}))
    cagr = Event(Concept('agriculture', db_refs={'WM': [(agr, 1.0)]}))
    print(cgov.matches_key())
    stmt1 = Influence(cgov, cagr, evidence=[Evidence(source_api='eidos1')])
    stmt2 = Influence(cagr, cgov, evidence=[Evidence(source_api='eidos2')])
    stmt3 = Influence(cgov, cagr, evidence=[Evidence(source_api='eidos3')])
    pa = Preassembler(world_ontology, [stmt1, stmt2, stmt3])
    unique_stmts = pa.combine_duplicates()
    unique_stmts = sorted(unique_stmts, key=lambda x: len(x.evidence))
    assert len(unique_stmts) == 2
    assert len(unique_stmts[0].evidence) == 1
    assert len(unique_stmts[1].evidence) == 2, unique_stmts
    sources = [e.source_api for e in unique_stmts[1].evidence]
    assert set(sources) == {'eidos1', 'eidos3'}


def test_influence_refinement():
    tran = 'wm/concept/causal_factor/access/infrastructure_access/'\
           'transportation'
    ship = 'wm/concept/causal_factor/access/infrastructure_access/' \
        'transportation/shipping'
    agr = 'wm/concept/causal_factor/economic_and_commerce/' \
        'economic_activity/livelihood'
    ctran = Event(Concept('transportation', db_refs={'WM': [(tran, 1.0)]}))
    cship = Event(Concept('trucking', db_refs={'WM': [(ship, 1.0)]}))
    cagr = Event(Concept('agriculture', db_refs={'WM': [(agr, 1.0)]}))
    stmt1 = Influence(ctran, cagr, evidence=[Evidence(source_api='eidos1')])
    stmt2 = Influence(cship, cagr, evidence=[Evidence(source_api='eidos2')])
    stmt3 = Influence(cagr, ctran, evidence=[Evidence(source_api='eidos3')])
    pa = Preassembler(world_ontology, [stmt1, stmt2, stmt3])
    rel_stmts = pa.combine_related()
    assert len(rel_stmts) == 2, rel_stmts
    truck_stmt = [st for st in rel_stmts if st.subj.concept.name ==
                  'trucking'][0]
    assert len(truck_stmt.supported_by) == 1
    assert truck_stmt.supported_by[0].subj.concept.name == 'transportation'


def test_find_contradicts():
    st1 = Inhibition(Agent('a'), Agent('b'))
    st2 = Activation(Agent('a'), Agent('b'))
    st3 = IncreaseAmount(Agent('a'), Agent('b'))
    st4 = DecreaseAmount(Agent('a'), Agent('b'))
    st5 = ActiveForm(Agent('a',
            mods=[ModCondition('phosphorylation', None, None, True)]),
            'kinase', True)
    st6 = ActiveForm(Agent('a',
            mods=[ModCondition('phosphorylation', None, None, True)]),
            'kinase', False)
    pa = Preassembler(bio_ontology, [st1, st2, st3, st4, st5, st6])
    contradicts = pa.find_contradicts()
    assert len(contradicts) == 3
    for s1, s2 in contradicts:
        assert {s1.uuid, s2.uuid} in ({st1.uuid, st2.uuid},
                                      {st3.uuid, st4.uuid},
                                      {st5.uuid, st6.uuid})


def test_find_contradicts_refinement():
    ras = Agent('RAS', db_refs={'FPLX': 'RAS'})
    kras = Agent('KRAS', db_refs={'HGNC': '6407'})
    hras = Agent('HRAS', db_refs={'HGNC': '5173'})
    st1 = Phosphorylation(Agent('x'), ras)
    st2 = Dephosphorylation(Agent('x'), kras)
    st3 = Dephosphorylation(Agent('x'), hras)
    pa = Preassembler(bio_ontology, [st1, st2, st3])
    contradicts = pa.find_contradicts()
    assert len(contradicts) == 2
    for s1, s2 in contradicts:
        assert {s1.uuid, s2.uuid} in ({st1.uuid, st2.uuid},
                                      {st1.uuid, st3.uuid})


def test_preassemble_related_complex():
    ras = Agent('RAS', db_refs={'FPLX': 'RAS'})
    kras = Agent('KRAS', db_refs={'HGNC': '6407'})
    hras = Agent('HRAS', db_refs={'HGNC': '5173'})
    st1 = Complex([kras, hras])
    st2 = Complex([kras, ras])
    st3 = Complex([hras, kras])
    st4 = Complex([ras, kras])
    pa = Preassembler(bio_ontology, [st1, st2, st3, st4])
    uniq = pa.combine_duplicates()
    assert len(uniq) == 2
    top = pa.combine_related()
    assert len(top) == 1


def test_normalize_opposites():
    concept1 = 'wm/concept/causal_factor/food_security/food_stability'
    concept2 = 'wm/concept/causal_factor/food_insecurity/food_instability'
    concept3 = ('wm/concept/causal_factor/crisis_and_disaster/'
                'environmental_disasters/natural_disaster/flooding')

    # First test the inherently positive being the main grounding
    dbr = {'WM': [(concept1, 1.0), (concept2, 0.5), (concept3, 0.1)]}
    ev = Event(Concept('x', db_refs=dbr),
               delta=QualitativeDelta(polarity=1))
    pa = Preassembler(world_ontology, stmts=[ev])
    pa.normalize_opposites(ns='WM')
    # We are normalizing to food supply since that is the inherently
    # positive concept
    assert pa.stmts[0].concept.db_refs['WM'][0] == \
        (concept1, 1.0), pa.stmts[0].concept.db_refs['WM']
    assert pa.stmts[0].concept.db_refs['WM'][1] == \
        (concept1, 0.5), pa.stmts[0].concept.db_refs['WM']
    assert pa.stmts[0].concept.db_refs['WM'][2] == \
        (concept3, 0.1), pa.stmts[0].concept.db_refs['WM']
    assert pa.stmts[0].delta.polarity == 1

    # Next test the inherently negative being the main grounding
    dbr = {'WM': [(concept2, 1.0), (concept1, 0.5), (concept3, 0.1)]}
    ev = Event(Concept('x', db_refs=dbr),
               delta=QualitativeDelta(polarity=1))
    pa = Preassembler(world_ontology, stmts=[ev])
    pa.normalize_opposites(ns='WM')
    # We are normalizing to food supply since that is the inherently
    # positive concept
    assert pa.stmts[0].concept.db_refs['WM'][0] == \
           (concept1, 1.0), pa.stmts[0].concept.db_refs['WM']
    assert pa.stmts[0].concept.db_refs['WM'][1] == \
           (concept1, 0.5), pa.stmts[0].concept.db_refs['WM']
    assert pa.stmts[0].concept.db_refs['WM'][2] == \
           (concept3, 0.1), pa.stmts[0].concept.db_refs['WM']
    assert pa.stmts[0].delta.polarity == -1


def test_normalize_opposites_influence():
    concept1 = 'wm/concept/causal_factor/food_security/food_stability'
    concept2 = 'wm/concept/causal_factor/food_insecurity/food_instability'
    dbr1 = {'WM': [(concept1, 1.0), (concept2, 0.5)]}
    dbr2 = {'WM': [(concept2, 1.0), (concept1, 0.5)]}
    stmt = Influence(Event(Concept('x', db_refs=dbr1),
                           delta=QualitativeDelta(polarity=1)),
                     Event(Concept('y', db_refs=dbr2),
                           delta=QualitativeDelta(polarity=-1)))
    pa = Preassembler(world_ontology, stmts=[stmt])
    pa.normalize_opposites(ns='WM')
    assert pa.stmts[0].subj.delta.polarity == 1
    assert pa.stmts[0].obj.delta.polarity == 1


def test_normalize_opposites_association():
    concept1 = 'wm/concept/causal_factor/food_security/food_stability'
    concept2 = 'wm/concept/causal_factor/food_insecurity/food_instability'
    dbr1 = {'WM': [(concept1, 1.0), (concept2, 0.5)]}
    dbr2 = {'WM': [(concept2, 1.0), (concept1, 0.5)]}
    stmt = Association([Event(Concept('x', db_refs=dbr1),
                              delta=QualitativeDelta(polarity=1)),
                        Event(Concept('y', db_refs=dbr2),
                              delta=QualitativeDelta(polarity=-1))])
    pa = Preassembler(world_ontology, stmts=[stmt])
    pa.normalize_opposites(ns='WM')
    assert pa.stmts[0].members[0].delta.polarity == 1
    assert pa.stmts[0].members[1].delta.polarity == 1


def test_agent_text_storage():
    A1 = Agent('A', db_refs={'TEXT': 'A'})
    A2 = Agent('A', db_refs={'TEXT': 'alpha'})
    B1 = Agent('B', db_refs={'TEXT': 'bag'})
    B2 = Agent('B', db_refs={'TEXT': 'bug'})
    C = Agent('C')
    D = Agent('D')
    inp = [
        Complex([A1, B1], evidence=Evidence(text='A complex bag.')),
        Complex([B2, A2], evidence=Evidence(text='bug complex alpha once.')),
        Complex([B2, A2], evidence=Evidence(text='bug complex alpha again.')),
        Complex([A1, C, B2], evidence=Evidence(text='A complex C bug.')),
        Phosphorylation(A1, B1, evidence=Evidence(text='A phospo bags.')),
        Phosphorylation(A2, B2, evidence=Evidence(text='alpha phospho bugs.')),
        Conversion(D, [A1, B1], [C, D],
                   evidence=Evidence(text='D: A bag -> C D')),
        Conversion(D, [B1, A2], [C, D],
                   evidence=Evidence(text='D: bag a -> C D')),
        Conversion(D, [B2, A2], [D, C],
                   evidence=Evidence(text='D: bug a -> D C')),
        Conversion(D, [B1, A1], [C, D],
                   evidence=Evidence(text='D: bag A -> C D')),
        Conversion(D, [A1], [A1, C],
                   evidence=Evidence(text='D: A -> A C'))
        ]
    pa = Preassembler(bio_ontology, inp)
    unq1 = pa.combine_duplicates()
    assert len(unq1) == 5, len(unq1)
    assert all([len(ev.annotations['prior_uuids']) == 1
                for s in unq1 for ev in s.evidence
                if len(s.evidence) > 1]),\
        'There can only be one prior evidence per uuid at this stage.'
    ev_uuid_dict = {ev.annotations['prior_uuids'][0]: ev.annotations['agents']
                    for s in unq1 for ev in s.evidence}
    for s in inp:
        raw_text = [ag.db_refs.get('TEXT')
                    for ag in s.agent_list(deep_sorted=True)]
        assert raw_text == ev_uuid_dict[s.uuid]['raw_text'],\
            str(raw_text) + '!=' + str(ev_uuid_dict[s.uuid]['raw_text'])

    # Now run pa on the above corpus plus another statement.
    inp2 = unq1 + [
        Complex([A1, C, B1], evidence=Evidence(text='A complex C bag.'))
        ]
    pa2 = Preassembler(bio_ontology, inp2)
    unq2 = pa2.combine_duplicates()
    assert len(unq2) == 5, len(unq2)
    old_ev_list = []
    new_ev = None
    for s in unq2:
        for ev in s.evidence:
            if ev.text == inp2[-1].evidence[0].text:
                new_ev = ev
            else:
                old_ev_list.append(ev)
    assert all([len(ev.annotations['prior_uuids']) == 2 for ev in old_ev_list])
    assert new_ev
    assert len(new_ev.annotations['prior_uuids']) == 1


def test_agent_coordinates():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'reach_coordinates.json')
    stmts = reach.process_json_file(path).statements
    pa = Preassembler(bio_ontology, stmts)
    unique_stmt = pa.combine_duplicates()[0]
    agent_annots = [ev.annotations['agents'] for ev in unique_stmt.evidence]
    assert all(a['raw_text'] == ['MEK1', 'ERK2'] for a in agent_annots)
    assert {tuple(a['coords']) for a in agent_annots} == {((21, 25), (0, 4)),
                                                          ((0, 4), (15, 19))}


def test_association_duplicate():
    ev1 = Event(Concept('a'))
    ev2 = Event(Concept('b'))
    ev3 = Event(Concept('c'))
    # Order of members does not matter
    st1 = Association([ev1, ev2], evidence=[Evidence(source_api='eidos1')])
    st2 = Association([ev1, ev3], evidence=[Evidence(source_api='eidos2')])
    st3 = Association([ev2, ev1], evidence=[Evidence(source_api='eidos3')])
    st4 = Association([ev2, ev3], evidence=[Evidence(source_api='eidos4')])
    st5 = Association([ev2, ev3], evidence=[Evidence(source_api='eidos5')])
    eidos_ont = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '../sources/eidos/eidos_ontology.rdf')
    pa = Preassembler(world_ontology, [st1, st2, st3, st4, st5])
    unique_stmts = pa.combine_duplicates()
    assert len(unique_stmts) == 3
    assert len(unique_stmts[0].evidence) == 2
    assert len(unique_stmts[1].evidence) == 1
    assert len(unique_stmts[2].evidence) == 2
    sources = [e.source_api for e in unique_stmts[0].evidence]
    assert set(sources) == {'eidos1', 'eidos3'}


def test_association_refinement():
    unrelated = 'wm/concept/causal_factor/wild_food_sources'
    parent = 'wm/concept/causal_factor/health_and_life'
    child = 'wm/concept/causal_factor/health_and_life/' \
        'living_condition/food_safety'
    parent_event = Event(Concept('parent', db_refs={'WM': [(parent, 1.0)]}))
    unrelated_event = \
        Event(Concept('unrelated', db_refs={'WM': [(unrelated, 1.0)]}))
    child_event = Event(Concept('child',
                                db_refs={'WM': [(child, 1.0)]}))
    st1 = Association([parent_event, unrelated_event],
                      evidence=[Evidence(source_api='eidos1')])
    st2 = Association([unrelated_event, parent_event],
                      evidence=[Evidence(source_api='eidos2')])
    st3 = Association([parent_event, child_event],
                      evidence=[Evidence(source_api='eidos3')])
    st4 = Association([unrelated_event, child_event],
                      evidence=[Evidence(source_api='eidos4')])
    pa = Preassembler(world_ontology, [st1, st2, st3, st4])
    unique_stmts = pa.combine_duplicates()
    assert len(unique_stmts) == 3
    top_level_stmts = pa.combine_related()
    assert len(top_level_stmts) == 2, top_level_stmts

    names = {tuple(sorted(e.concept.name for e in stmt.members)): stmt
             for stmt in top_level_stmts}
    stmt = names[('child', 'unrelated')]
    assert len(stmt.supported_by) == 1
    assert {e.concept.name for e in stmt.supported_by[0].members} == \
           {'parent', 'unrelated'}


def test_matches_key_fun():
    from indra.statements import WorldContext, RefContext

    def has_location(stmt):
        if not stmt.context or not stmt.context.geo_location or \
                not stmt.context.geo_location.db_refs.get('GEOID'):
            return False
        return True

    def event_location_matches(stmt):
        if isinstance(stmt, Event):
            if not has_location(stmt):
                context_key = None
            else:
                context_key = stmt.context.geo_location.db_refs['GEOID']

            matches_key = str((stmt.concept.matches_key(), context_key))
        else:
            matches_key = stmt.matches_key()
        return matches_key

    def event_location_refinement(st1, st2, ontology, entities_refined):
        if isinstance(st1, Event) and isinstance(st2, Event):
            ref = st1.refinement_of(st2, ontology)
            if not ref:
                return False
            if not has_location(st2):
                return True
            elif not has_location(st1) and has_location(st2):
                return False
            else:
                return st1.context.geo_location.db_refs['GEOID'] == \
                    st2.context.geo_location.db_refs['GEOID']

    context1 = WorldContext(geo_location=RefContext('x',
                                                    db_refs={'GEOID': '1'}))
    context2 = WorldContext(geo_location=RefContext('x',
                                                    db_refs={'GEOID': '2'}))

    health = 'wm/concept/causal_factor/health_and_life'
    e1 = Event(Concept('health', db_refs={'WM': [(health, 1.0)]}),
               context=context1,
               evidence=Evidence(text='1', source_api='eidos'))
    e2 = Event(Concept('health', db_refs={'WM': [(health, 1.0)]}),
               context=context2,
               evidence=Evidence(text='2', source_api='eidos'))
    e3 = Event(Concept('health', db_refs={'WM': [(health, 1.0)]}),
               context=context2,
               evidence=Evidence(text='3', source_api='eidos'))

    pa = Preassembler(world_ontology, [e1, e2, e3],
                      matches_fun=event_location_matches,
                      refinement_fun=event_location_refinement)

    unique_stmts = pa.combine_duplicates()
    assert len(unique_stmts) == 2, unique_stmts

    from indra.tools.assemble_corpus import run_preassembly
    stmts = run_preassembly([e1, e2, e3], matches_fun=event_location_matches,
                            refinement_fun=event_location_refinement)
    assert len(stmts) == 2, stmts


def test_uppro_assembly():
    ag1 = Agent('x', db_refs={'UP': 'P01019', 'UPPRO': 'PRO_0000032457'})
    ag2 = Agent('y', db_refs={'UP': 'P01019', 'UPPRO': 'PRO_0000032458'})
    assert ag1.get_grounding() == ('UPPRO', ag1.db_refs['UPPRO'])
    assert ag2.get_grounding() == ('UPPRO', ag2.db_refs['UPPRO'])
    stmt1 = Phosphorylation(None, ag1)
    stmt2 = Phosphorylation(None, ag2)
    assert stmt1.matches_key() != stmt2.matches_key()
    pa = Preassembler(bio_ontology, [stmt1, stmt2])
    unique_stmts = pa.combine_duplicates()
    assert len(unique_stmts) == 2, unique_stmts

    from indra.tools import assemble_corpus as ac
    stmts = ac.map_grounding([stmt1, stmt2])
    pa = Preassembler(bio_ontology, stmts)
    unique_stmts = pa.combine_duplicates()
    assert len(unique_stmts) == 2


def test_split_idx():
    ras = Agent('RAS', db_refs={'FPLX': 'RAS'})
    kras = Agent('KRAS', db_refs={'HGNC': '6407'})
    hras = Agent('HRAS', db_refs={'HGNC': '5173'})
    st1 = Phosphorylation(Agent('x'), ras)
    st2 = Phosphorylation(Agent('x'), kras)
    st3 = Phosphorylation(Agent('x'), hras)
    pa = Preassembler(bio_ontology)
    maps = pa._generate_id_maps([st1, st2, st3])
    assert (1, 0) in maps, maps
    assert (2, 0) in maps, maps
    assert pa._comparison_counter == 2
    pa = Preassembler(bio_ontology)
    maps = pa._generate_id_maps([st1, st2, st3], split_idx=1)
    assert (2, 0) in maps, maps
    assert (1, 0) not in maps, maps
    assert pa._comparison_counter == 1


def test_refinement_filters():
    ras = Agent('RAS', db_refs={'FPLX': 'RAS'})
    kras = Agent('KRAS', db_refs={'HGNC': '6407'})
    hras = Agent('HRAS', db_refs={'HGNC': '5173'})
    st1 = Phosphorylation(Agent('x'), ras)
    st2 = Phosphorylation(Agent('x'), kras)
    st3 = Phosphorylation(Agent('x'), hras)

    # This filters everything out so no comparisons will be done
    def filter_empty(stmts_by_hash, stmts_to_compare, *args):
        return {k: set() for k in stmts_by_hash}
    # No comparisons here
    pa = Preassembler(bio_ontology, stmts=[st1, st2, st3])
    pa.combine_related(filters=[bio_ontology_refinement_filter,
                                filter_empty])
    assert pa._comparison_counter == 0

    # This is a superset of all comparisons constrained by the ontology
    # so will not change what the preassembler does internally
    def filter_all(stmts_by_hash, stmts_to_compare, *args):
        filter_set = {k: (set(stmts_by_hash) - {k}) for k in stmts_by_hash}
        if stmts_to_compare is None:
            return filter_set
        else:
            for k in filter_set:
                filter_set[k] &= stmts_to_compare.get(k, set())
            return filter_set
    # The same number of comparisons here as without the filter
    pa = Preassembler(bio_ontology, stmts=[st1, st2, st3])
    pa.combine_related(filters=[bio_ontology_refinement_filter,
                                filter_all])
    assert pa._comparison_counter == 2, pa._comparison_counter

    # Just to make sure lists of more than one filter are correctly handled
    pa = Preassembler(bio_ontology, stmts=[st1, st2, st3])
    pa.combine_related(filters=[filter_all, filter_empty,
                                bio_ontology_refinement_filter])
    assert pa._comparison_counter == 0, pa._comparison_counter

    # Now try adding more statement types
    st4 = Activation(Agent('x'), ras)
    st5 = Activation(Agent('x'), kras)
    st6 = Activation(Agent('x'), hras)

    # The same number of comparisons here as without the filter
    pa = Preassembler(bio_ontology, stmts=[st1, st2, st3, st4, st5, st6])
    pa.combine_related(filters=[bio_ontology_refinement_filter,
                                filter_all])
    assert pa._comparison_counter == 4, pa._comparison_counter

    pa = Preassembler(bio_ontology, stmts=[st1, st2, st3, st4, st5, st6])
    pa.combine_related(filters=[filter_all,
                                bio_ontology_refinement_filter])
    assert pa._comparison_counter == 4, pa._comparison_counter

    # Just to make sure lists of more than one filter are correctly handled
    pa = Preassembler(bio_ontology, stmts=[st1, st2, st3, st4, st5, st6])
    pa.combine_related(filters=[filter_all, filter_empty,
                                bio_ontology_refinement_filter])
    assert pa._comparison_counter == 0, pa._comparison_counter
