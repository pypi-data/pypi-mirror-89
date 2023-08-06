import random
import unittest
from datetime import datetime
from unittest import SkipTest

from nose.plugins.attrib import attr
from indra.sources import indra_db_rest as dbr
from indra.sources.indra_db_rest.api import get_statement_queries
from indra.statements import Agent, Phosphorylation


EXPECTED_BATCH_SIZE = 500


def __check_request(seconds, *args, **kwargs):
    check_stmts = kwargs.pop('check_stmts', True)
    simple_response = kwargs.pop('simple_response', True)
    kwargs['simple_response'] = simple_response
    now = datetime.now()
    resp = dbr.get_statements(*args, **kwargs)
    time_taken = datetime.now() - now
    if check_stmts:
        if kwargs.get('simple_response', True):
            stmts = resp
        else:
            stmts = resp.statements
        assert stmts, "Got no statements."
    return resp


@attr('nonpublic')
def test_simple_request():
    __check_request(6, 'MAP2K1', 'MAPK1', stmt_type='Phosphorylation')


@attr('nonpublic')
def test_request_for_complex():
    __check_request(30, agents=['MEK@FPLX', 'ERK@FPLX'], stmt_type='Complex')


@attr('nonpublic')
def test_null_request():
    try:
        dbr.get_statements()
    except ValueError:
        return
    except BaseException as e:
        assert False, "Raised wrong exception: " + str(e)
    assert False, "Null request did not raise any exception."


@attr('nonpublic', 'slow')
def test_large_request():
    __check_request(40, agents=['AKT1'])


@attr('nonpublic', 'slow')
def test_bigger_request():
    __check_request(60, agents=['MAPK1'])


@attr('nonpublic')
def test_timeout_no_persist_agent():
    candidates = ['TP53', 'NFkappaB@FPLX', 'AKT@FPLX']
    agent = random.choice(candidates)
    print(agent)
    resp = dbr.get_statements(agents=[agent], persist=False, timeout=0)
    assert resp.is_working(), "Lookup resolved too fast."
    resp.wait_until_done(70)
    assert len(resp.statements) > 0.9*EXPECTED_BATCH_SIZE, len(resp.statements)


@attr('nonpublic')
def test_timeout_no_persist_type_object():
    candidates = ['TP53', 'NFkappaB@FPLX', 'AKT@FPLX']
    agent = random.choice(candidates)
    print(agent)
    resp = dbr.get_statements(stmt_type='phosphorylation', object=agent,
                              persist=False, timeout=0)
    assert resp.is_working(), "Lookup resolved too fast."
    resp.wait_until_done(70)
    assert len(resp.statements) > 0.9*EXPECTED_BATCH_SIZE, len(resp.statements)


@attr('nonpublic', 'slow')
def test_too_big_request_no_persist():
    resp_some = __check_request(60, agents=['TP53'], persist=False,
                                simple_response=False)
    assert sum(resp_some.get_ev_count(s) is not None
               for s in resp_some.statements) == len(resp_some.statements), \
        "Counts dict was improperly handled."
    return resp_some


@attr('nonpublic', 'slow', 'notravis')
@unittest.skip('skippping')
def test_too_big_request_persist_and_block():
    resp_all1 = __check_request(200, agents=['TP53'], persist=True, timeout=None,
                                simple_response=False)
    assert sum(resp_all1.get_ev_count(s) is not None
               for s in resp_all1.statements) > 0.9*len(resp_all1.statements), \
        "Counts dict was improperly handled."
    return resp_all1


@attr('nonpublic', 'slow', 'notravis')
def test_too_big_request_persist_no_block():
    resp_some = test_too_big_request_no_persist()
    resp_all1 = test_too_big_request_persist_and_block()
    resp_all2 = __check_request(60, agents=['TP53'], persist=True,
                                timeout=10, check_stmts=False,
                                simple_response=False)
    num_counts = sum(resp_all2.get_ev_count(s) is not None
                     for s in resp_all2.statements)
    num_stmts = len(resp_all2.statements)
    assert num_counts == num_stmts, \
        ("Counts dict was improperly handled before completing: %d counts "
         "for %d statements." % (num_counts, num_stmts))
    assert resp_all2.is_working(), "Background complete resolved too fast."
    assert len(resp_all2.statements_sample) == len(resp_some.statements), \
        "Sample size: %s, Small resp size: %s" \
        % (len(resp_all2.statements_sample), len(resp_some.statements))
    resp_all2.wait_until_done(500)
    assert not resp_all2.is_working(), \
        "Response is still working. Took too long."
    assert resp_all2.statements
    num_counts = sum(resp_all2.get_ev_count(s) is not None
                     for s in resp_all2.statements)
    num_stmts = len(resp_all2.statements)
    assert num_counts > 0.9*num_stmts, \
        "Counts dict was improperly handled after completing."
    assert len(resp_all2.statements) == len(resp_all1.statements), \
        'Expected: %d, actual: %d' % (len(resp_all1.statements),
                                      len(resp_all2.statements))
    return


@attr('nonpublic')
def test_famplex_namespace():
    stmts = dbr.get_statements('PDGF@FPLX', 'FOS', stmt_type='IncreaseAmount',
                               simple_response=True)
    print(len(stmts))
    print(stmts)
    assert all([s.agent_list()[0].db_refs.get('FPLX') == 'PDGF' for s in stmts]),\
        'Not all subjects match.'
    assert all([s.agent_list()[1].name == 'FOS' for s in stmts]),\
        'Not all objects match: ' \
        + ', '.join({s.agent_list()[1].name for s in stmts})


@attr('nonpublic')
def test_paper_query():
    stmts_1 = dbr.get_statements_for_paper([('pmcid', 'PMC5770457'),
                                            ('pmid', '27014235')],
                                           simple_response=True)
    assert len(stmts_1)

    p = dbr.get_statements_for_paper([('pmcid', 'PMC5770457'),
                                      ('pmid', '27014235')])
    assert len(p.statements)
    assert len(p.get_source_counts())
    assert len(p.get_ev_counts())


@attr('nonpublic')
def test_regulate_amount():
    idbp = dbr.get_statements('FOS', stmt_type='RegulateAmount',
                              simple_response=False)
    stmts = idbp.statements
    stmt_types = {type(s).__name__ for s in stmts}
    counts = idbp.get_source_counts()
    one_key = list(counts.keys())[0]
    assert counts[one_key] == idbp.get_source_count_by_hash(one_key)
    assert {'IncreaseAmount', 'DecreaseAmount'}.issubset(stmt_types), \
        stmt_types


@attr('nonpublic')
def test_get_statements_by_hash():
    hash_list = [30674674032092136, -22289282229858243, -25056605420392180]
    stmts = dbr.get_statements_by_hash(hash_list, simple_response=True)
    print({s.get_hash(shallow=True): s for s in stmts})
    assert len(stmts) >= 2, \
        "Wrong number of statements: %s vs. %s" % (len(stmts), len(hash_list))

    p = dbr.get_statements_by_hash(hash_list)
    assert len(p.statements)
    assert len(p.get_source_counts())
    assert len(p.get_ev_counts())
    return


@attr('nonpublic')
def test_get_statements_by_hash_no_hash():
    stmts = dbr.get_statements_by_hash([], simple_response=True)
    assert not stmts, "Got statements without giving a hash."


@attr('nonpublic')
def test_curation_submission():
    raise SkipTest("Curation currently not working.")
    dbr.submit_curation(32760831642168299, 'TEST', 'This is a test.',
                        'tester', is_test=True)


@attr('nonpublic')
def test_get_statement_queries():
    ag = Agent('MAP2K1', db_refs={})
    stmt = Phosphorylation(None, ag)
    urls = get_statement_queries([stmt])
    assert 'MAP2K1@NAME' in urls[0]
    urls = get_statement_queries([stmt], fallback_ns='TEXT')
    assert 'MAP2K1@TEXT' in urls[0]
    urls = get_statement_queries([stmt],
                                 pick_ns_fun=lambda x: '%s@%s' %
                                                       (x.name, 'XXX'))
    assert 'MAP2K1@XXX' in urls[0], urls[0]
    ag = Agent('MEK', db_refs={'FPLX': 'MEK'})
    stmt = Phosphorylation(None, ag)
    urls = get_statement_queries([stmt])
    assert 'MEK@FPLX' in urls[0]
    urls = get_statement_queries([stmt], fallback_ns='TEXT')
    assert 'MEK@FPLX' in urls[0]
    urls = get_statement_queries([stmt],
                                 pick_ns_fun=lambda x: '%s@%s' %
                                                       (x.name, 'XXX'))
