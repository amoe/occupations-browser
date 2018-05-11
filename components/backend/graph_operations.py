#! /usr/bin/env python3

import functools
import matplotlib
import matplotlib.pyplot
import networkx
import pprint
import neo4j
import neo4j.v1

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7687"

driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

APOC_TREE_GENERATOR_QUERY = """
    MATCH p = (:Token {content: {root}})-[:PRECEDES*]->(end:Token) 
    WHERE NOT (end)-[:PRECEDES]->()
    CALL apoc.convert.toTree([p]) YIELD value
    RETURN value
"""

def run_some_query(query, parameters):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            results = tx.run(query, parameters)
            return results

def tree_to_graph(tree):
    # defined by apoc, precedes is based on the relationship label
    object_format = dict(id='_id', children='precedes')
    return networkx.tree_graph(tree, object_format)

def get_subgraph(root):
    result = run_some_query(APOC_TREE_GENERATOR_QUERY, {'root': root})
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
