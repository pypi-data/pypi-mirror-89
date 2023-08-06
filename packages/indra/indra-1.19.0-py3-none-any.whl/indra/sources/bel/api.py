# -*- coding: utf-8 -*-

"""High level API functions for the PyBEL processor."""

import zlib
import json
import pybel
import logging
import requests
from functools import lru_cache
from .processor import PybelProcessor


logger = logging.getLogger(__name__)

version = 'v1.0.0'
branch = 'https://github.com/cthoyt/selventa-knowledge/raw/' \
         '{}/selventa_knowledge/{}'
large_corpus_url = branch.format(version, 'large_corpus.bel.nodelink.json.gz')
small_corpus_url = branch.format(version, 'small_corpus.bel.nodelink.json.gz')


def process_small_corpus():
    """Return PybelProcessor with statements from Selventa Small Corpus.

    Returns
    -------
    bp : PybelProcessor
        A PybelProcessor object which contains INDRA Statements in
        its statements attribute.
    """
    return process_pybel_network(network_type='graph_jsongz_url',
                                 network_file=small_corpus_url)


def process_large_corpus():
    """Return PybelProcessor with statements from Selventa Large Corpus.

    Returns
    -------
    bp : PybelProcessor
        A PybelProcessor object which contains INDRA Statements in
        its statements attribute.
    """
    return process_pybel_network(network_type='graph_jsongz_url',
                                 network_file=large_corpus_url)


def process_pybel_network(network_type, network_file, **kwargs):
    """Return PybelProcessor by processing a given network file.

    Parameters
    ----------
    network_type : str
        The type of network that network_file is. The options are:
        belscript, json, cbn_jgif, graph_pickle, and graph_jsongz_url.
        Default: graph_jsongz_url
    network_file : str
        Path to the network file/URL to process.

    Returns
    -------
    bp : PybelProcessor
        A PybelProcessor object which contains INDRA Statements in
        bp.statements.
    """
    if network_type == 'belscript':
        return process_belscript(network_file, **kwargs)
    elif network_type == 'json':
        return process_json_file(network_file)
    elif network_type == 'cbn_jgif':
        return process_cbn_jgif_file(network_file)
    elif network_type == 'graph_jsongz_url':
        if not network_file:
            network_file = large_corpus_url
        logger.info('Loading %s' % network_file)
        res = requests.get(network_file)
        res.raise_for_status()
        contentb = zlib.decompress(res.content, zlib.MAX_WBITS | 32)
        content = contentb.decode('utf-8')
        graph = pybel.from_nodelink_jsons(content)
        return process_pybel_graph(graph)
    elif network_type == 'graph_pickle':
        graph = pybel.from_pickle(network_file)
        return process_pybel_graph(graph)
    else:
        raise ValueError('Unknown network type: %s' % network_type)


def process_pybel_neighborhood(entity_names, network_type='graph_jsongz_url',
                               network_file=None, **kwargs):
    """Return PybelProcessor around neighborhood of given genes in a network.

    This function processes the given network file and filters the returned
    Statements to ones that contain genes in the given list.

    Parameters
    ----------
    entity_names : list[str]
        A list of entity names (e.g., gene names) which will be used as the
        basis of filtering the result. If any of the Agents of an extracted
        INDRA Statement has a name appearing in this list, the Statement is
        retained in the result.
    network_type : Optional[str]
        The type of network that network_file is. The options are:
        belscript, json, cbn_jgif, graph_pickle, and graph_jsongz_url.
        Default: graph_jsongz_url
    network_file : Optional[str]
        Path to the network file/URL to process. If not given, by default, the
        Selventa Large Corpus is used via a URL pointing to a gzipped PyBEL
        Graph JSON file.

    Returns
    -------
    bp : PybelProcessor
        A PybelProcessor object which contains INDRA Statements in
        bp.statements.
    """
    bp = process_pybel_network(network_type, network_file, **kwargs)
    filtered_stmts = []
    filter_names = set(entity_names)
    for stmt in bp.statements:
        found = False
        for agent in stmt.agent_list():
            if agent is not None:
                if agent.name in filter_names:
                    found = True
        if found:
            filtered_stmts.append(stmt)

    bp.statements = filtered_stmts

    return bp


@lru_cache(maxsize=100)
def process_pybel_graph(graph):
    """Return a PybelProcessor by processing a PyBEL graph.

    Parameters
    ----------
    graph : pybel.struct.BELGraph
        A PyBEL graph to process

    Returns
    -------
    bp : PybelProcessor
        A PybelProcessor object which contains INDRA Statements in
        bp.statements.
    """
    bp = PybelProcessor(graph)
    bp.get_statements()
    if bp.annot_manager.failures:
        logger.warning('missing %d annotation pairs',
                       sum(len(v)
                           for v in bp.annot_manager.failures.values()))
    return bp


def process_belscript(file_name, **kwargs):
    """Return a PybelProcessor by processing a BEL script file.

    Key word arguments are passed directly to pybel.from_path,
    for further information, see
    pybel.readthedocs.io/en/latest/io.html#pybel.from_path
    Some keyword arguments we use here differ from the defaults
    of PyBEL, namely we set `citation_clearing` to False
    and `no_identifier_validation` to True.

    Parameters
    ----------
    file_name : str
        The path to a BEL script file.

    Returns
    -------
    bp : PybelProcessor
        A PybelProcessor object which contains INDRA Statements in
        bp.statements.
    """
    if 'citation_clearing' not in kwargs:
        kwargs['citation_clearing'] = False
    if 'no_identifier_validation' not in kwargs:
        kwargs['no_identifier_validation'] = True
    pybel_graph = pybel.from_bel_script(file_name, **kwargs)
    return process_pybel_graph(pybel_graph)


def process_json_file(file_name):
    """Return a PybelProcessor by processing a Node-Link JSON file.

    For more information on this format, see:
    http://pybel.readthedocs.io/en/latest/io.html#node-link-json

    Parameters
    ----------
    file_name : str
        The path to a Node-Link JSON file.

    Returns
    -------
    bp : PybelProcessor
        A PybelProcessor object which contains INDRA Statements in
        bp.statements.
    """
    pybel_graph = pybel.from_nodelink_file(file_name, check_version=False)
    return process_pybel_graph(pybel_graph)


def process_cbn_jgif_file(file_name):
    """Return a PybelProcessor by processing a CBN JGIF JSON file.

    Parameters
    ----------
    file_name : str
        The path to a CBN JGIF JSON file.

    Returns
    -------
    bp : PybelProcessor
        A PybelProcessor object which contains INDRA Statements in
        bp.statements.
    """
    with open(file_name, 'r') as jgf:
        return process_pybel_graph(pybel.from_cbn_jgif(json.load(jgf)))


