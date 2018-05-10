import neo4j
import neo4j.v1
import networkx
import matplotlib
import matplotlib.pyplot
import functools

def quickplot(g):
    matplotlib.pyplot.clf()
    networkx.draw_networkx(g)
    matplotlib.pyplot.show()

APOC_TREE_GENERATOR_QUERY = """
    MATCH p = (:Token {content: "the"})-[:PRECEDES*]->(end:Token) 
    WHERE NOT (end)-[:PRECEDES]->()
    CALL apoc.convert.toTree([p]) YIELD value
    RETURN value
"""

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7687"

driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

def run_some_query(query, parameters):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            results = tx.run(query, parameters)
            return results

def tree_to_graph(tree):
    # defined by apoc, precedes is based on the relationship label
    object_format = dict(id='_id', children='precedes')
    return networkx.tree_graph(tree, object_format)

def getgraphs():
    result = run_some_query(APOC_TREE_GENERATOR_QUERY, {})
    paths = result.value()

    return functools.reduce(networkx.compose, map(tree_to_graph, paths))
