#! /usr/bin/env python3

import functools
import matplotlib
import matplotlib.pyplot
import networkx
import pprint
import neo4j
import neo4j.v1
import misc

APOC_TREE_GENERATOR_QUERY = """
    MATCH p = (:Token {content: {root}})-[:PRECEDES*]->(end:Token) 
    WHERE NOT (end)-[:PRECEDES]->()
    CALL apoc.convert.toTree([p]) YIELD value
    RETURN value
"""

DELETE_NODE_QUERY = """
    MATCH (n:Token {content: {wanted}}) DETACH DELETE n
"""

CLEAR_GRAPH_QUERY = """
    MATCH (n) DETACH DELETE n
"""

GET_ALL_ROOTS_QUERY = """
    MATCH (n) WHERE NOT (n)<-[:PRECEDES]-() RETURN n
"""


def tree_to_graph(tree):
    # defined by apoc, precedes is based on the relationship label
    object_format = dict(id='_id', children='precedes')
    return networkx.tree_graph(tree, object_format)

def get_subgraph(root):
    result = misc.run_some_query(APOC_TREE_GENERATOR_QUERY, {'root': root})
    paths = result.value()

    if not paths:
        raise Exception("no results. this can happen on attempt to query nonexistent node OR a leaf node")

    return functools.reduce(networkx.compose, map(tree_to_graph, paths))

def quickplot(g):
    matplotlib.pyplot.clf()
    networkx.draw_networkx(g)
    matplotlib.pyplot.show()

def strict_first(seq):
    if not seq:
        raise Exception("seq is falsy")

    if len(seq) != 1:
        raise Exception("unexpected number of items in seq")

    return seq[0]

def get_tree_by_root(root):
    graph = get_subgraph(root)
    root_id = strict_first(find_nodes_by_content_attribute(graph, root))
    return networkx.tree_data(graph, root_id)

def find_nodes_by_content_attribute(g, wanted):
    return [
        n for n, d in g.nodes(data=True) if d['content'] == wanted 
    ]

def delete_node(wanted_content):
    misc.run_some_query(DELETE_NODE_QUERY, {'wanted': wanted_content})   

def clear_entire_graph():
    misc.run_some_query(CLEAR_GRAPH_QUERY, {})

def get_all_roots():
    return [
        r.value()['content']
        for r in run_some_query(GET_ALL_ROOTS_QUERY, {})
    ]
