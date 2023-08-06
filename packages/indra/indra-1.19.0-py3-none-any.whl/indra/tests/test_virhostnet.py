import pandas
from nose.plugins.attrib import attr
from indra.statements import Complex
from indra.sources import virhostnet
from indra.sources.virhostnet.api import data_columns
from indra.sources.virhostnet.processor import parse_psi_mi, parse_source_ids, \
    parse_text_refs, get_agent_from_grounding, process_row


test_row_str = ('uniprotkb:Q6P5R6	uniprotkb:Q1K9H5	'
                'uniprotkb:RL22L_HUMAN	uniprotkb:Q1K9H5_I33A0	'
                'uniprotkb:RL22L_HUMAN	uniprotkb:Q1K9H5_I33A0	'
                'psi-mi:"MI:0004"(affinity chromatography technology)	'
                '-	pubmed:26651948	taxid:9606	taxid:381518	'
                'psi-mi:"MI:0915"(physical association)	'
                'psi-mi:"MI:1114"(virhostnet)	'
                'virhostnet-rid:19809|virhostnet-nrid:18603	'
                'virhostnet-miscore:0.32715574')
test_row = {k: v for k, v in zip(data_columns, test_row_str.split('\t'))}
test_df = pandas.DataFrame.from_dict({k: [v] for k, v in test_row.items()})


@attr('webservice', 'slow')
def test_process_from_web():
    vp = virhostnet.process_from_web(query='pubmed:8553588')
    assert len(vp.statements) == 5, len(vp.statements)
    assert all(isinstance(st, Complex) for st in vp.statements)
    assert all(stmt.members[1].db_refs['REFSEQ_PROT'] == 'NP_040311'
               for stmt in vp.statements)
    assert all(stmt.evidence[0].pmid == '8553588'
               for stmt in vp.statements)


def test_process_df():
    vp = virhostnet.process_df(test_df)
    assert len(vp.statements) == 1
    _assert_test_stmt(vp.statements[0])


def test_get_agent_from_grounding():
    ag = get_agent_from_grounding('uniprotkb:P15056')
    assert ag.name == 'BRAF'
    assert ag.db_refs['UP'] == 'P15056', ag.db_refs

    ag = get_agent_from_grounding('uniprotkb:P15056-PRO_0000085665')
    # This is the name of the chain in UniProt which takes precedence
    # if we have a feature ID
    assert ag.name == 'Serine/threonine-protein kinase B-raf'
    assert ag.db_refs['UP'] == 'P15056'
    assert ag.db_refs['UPPRO'] == 'PRO_0000085665'

    ag = get_agent_from_grounding('refseq:NP_828867')
    assert ag.db_refs['REFSEQ_PROT'] == 'NP_828867'


def test_parse_text_refs():
    tr = parse_text_refs('pubmed:22046132')
    assert tr['PMID'] == '22046132'

    tr = parse_text_refs('pubmed:https(//doi.org/10.1101/2020.03.22.002386)')
    assert tr['DOI'] == '10.1101/2020.03.22.002386'


def test_parse_source_ids():
    sd = parse_source_ids('virhostnet-rid:2564|virhostnet-nrid:2199')
    assert sd == {'virhostnet-rid': '2564',
                  'virhostnet-nrid': '2199'}


def test_parse_psi_mi():
    res = parse_psi_mi('psi-mi:"MI:0915"(physical association)')
    assert len(res) == 2, res
    assert res[0] == 'MI:0915', res
    assert res[1] == 'physical association'


def test_process_row():
    stmt = process_row(test_row)
    _assert_test_stmt(stmt)


def _assert_test_stmt(stmt):
    assert isinstance(stmt, Complex)
    host_ag = stmt.members[0]
    assert host_ag.name == 'RPL22L1'
    vir_ag = stmt.members[1]
    # This is unreviewed so we currently can't get its name
    assert vir_ag.name == 'Q1K9H5'
    assert len(stmt.evidence) == 1
    ev = stmt.evidence[0]
    assert ev.source_api == 'virhostnet'
    assert ev.source_id == '19809'
    assert ev.pmid == '26651948'
    assert ev.text_refs == {'PMID': '26651948'}
    assert ev.annotations['host_tax'] == '9606'
    assert ev.annotations['vir_tax'] == '381518'
    assert ev.annotations['score'] == 0.32715574
    assert ev.annotations['int_type'] == {'id': 'MI:0915',
                                          'name': 'physical association'}
    assert ev.annotations['virhostnet-rid'] == '19809'
    assert ev.annotations['virhostnet-nrid'] == '18603'
    assert ev.annotations['exp_method'] == {'id': 'MI:0004',
                                            'name': ('affinity chromatography '
                                                     'technology')}


def test_get_uppro_name():
    ag = get_agent_from_grounding('uniprotkb:Q32ZE1-PRO_0000435839')
    assert ag.db_refs['UP'] == 'Q32ZE1'
    assert ag.db_refs['UPPRO'] == 'PRO_0000435839'
    assert ag.name == 'Non-structural protein 4A'


def test_name_web_fallback():
    ag = get_agent_from_grounding('uniprotkb:Q174W8', up_web_fallback=False)
    assert ag.name == 'Q174W8'
    ag = get_agent_from_grounding('uniprotkb:Q174W8', up_web_fallback=True)
    assert ag.name == 'GPRFZ2'
