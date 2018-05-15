import neo4j
import neo4j.v1
import networkx
import matplotlib
import matplotlib.pyplot
import functools
import misc

APOC_TREE_GENERATOR_QUERY = """
    MATCH p = (:Token {content: "the"})-[:PRECEDES*]->(end:Token) 
    WHERE NOT (end)-[:PRECEDES]->()
    CALL apoc.convert.toTree([p]) YIELD value
    RETURN value
"""

def tree_to_graph(tree):
    # defined by apoc, precedes is based on the relationship label
    object_format = dict(id='_id', children='precedes')
    return networkx.tree_graph(tree, object_format)

def getgraphs():
    result = misc.run_some_query(APOC_TREE_GENERATOR_QUERY, {})
    paths = result.value()

    return functools.reduce(networkx.compose, map(tree_to_graph, paths))
