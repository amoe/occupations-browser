#! /usr/bin/env python3

import matplotlib
import matplotlib.pyplot
import networkx
import pprint

result_set = []

graph = networkx.MultiDiGraph()

for item in result_set:
    for node in item['nodes']:
        properties = copy.deepcopy(node['properties'])
        properties['labels'] = node['labels']
        graph.add_node(node['id'], **properties)
    for rel in item['relationships']:
        properties = copy.deepcopy(rel['properties'])
        properties.update(
            id=rel['id'],
            type=rel['type']
        )
        graph.add_edge(
            rel['start_node'], rel['end_node'],
            key=rel.get('type'), **properties
        )

import neo4j
import neo4j.v1

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7687"

driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

# This is the one you need, it operates with v2 of the rs2graph code below 
# Note that the node with content 'the' is at the root here
INSANE_GRAPH_QUERY = """
    MATCH (a:Token {content: "the"})-[:PRECEDES*]->(t:Token)
    WITH COLLECT(a) + COLLECT(DISTINCT t) AS nodes_
    UNWIND nodes_ AS n
    OPTIONAL MATCH p = (n)-[r]-()
    WITH n AS n2, COLLECT(DISTINCT RELATIONSHIPS(p)) AS nestedrel
    RETURN n2, REDUCE(output = [], rel in nestedrel | output + rel) AS rels
"""

SLURP_GRAPH_FROM_SPECIFIC_ROOT_INCLUDING_ROOT = """
    MATCH (a:Token {content: "the"})-[:PRECEDES*]->(t:Token)
    WITH COLLECT(a) + COLLECT(t) AS nodez, t AS t
    OPTIONAL MATCH (t)-[r:PRECEDES]->()
    UNWIND nodez AS c
    RETURN ID(c), c AS n, r;
"""

SLURP_GRAPH_FROM_SPECIFIC_ROOT = """
    MATCH (a:Token {content: "the"})-[:PRECEDES*]->(t:Token)
    OPTIONAL MATCH (t)-[r:PRECEDES]->()
    RETURN t AS n, r;
"""

READ_NODES_AND_RELATIONSHIPS = """
    MATCH (n) OPTIONAL MATCH (n)-[r]->() RETURN n, r
"""

READ_GRAPH_NODES = """
    MATCH (n) RETURN n
"""

def quickplot(g):
    matplotlib.pyplot.clf()
    networkx.draw_networkx(g)
    matplotlib.pyplot.show()

def run_some_query(query, parameters):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            results = tx.run(query, parameters)
            return results

def blah():
    return rs2graph(run_some_query(SLURP_GRAPH_FROM_SPECIFIC_ROOT_INCLUDING_ROOT, {}))

def rs2graph(rs):
    graph = networkx.MultiDiGraph()

    for record in rs:
        node = record['n']
        if node:
            print("adding node")
            nx_properties = {}
            nx_properties.update(node.properties)
            nx_properties['labels'] = node.labels
            graph.add_node(node.id, **nx_properties)

        relationship = record['r']
        if relationship is not None:   # essential because relationships use hash val
            print("adding edge")
            graph.add_edge(
                relationship.start, relationship.end, key=relationship.type,
                **relationship.properties
            )

    return graph


# this version expects a collection of rels
def rs2graph_v2(rs):
    graph = networkx.MultiDiGraph()

    for record in rs:
        node = record['n2']
        if not node:
            raise Exception('every row should have a node')

        print("adding node")
        nx_properties = {}
        nx_properties.update(node.properties)
        nx_properties['labels'] = node.labels
        graph.add_node(node.id, **nx_properties)

        relationship_list = record['rels']

        for relationship in relationship_list:
            print("adding edge")
            graph.add_edge(
                relationship.start, relationship.end, key=relationship.type,
                **relationship.properties
            )

    return graph

# now we can use networkx tree_data to do it

# now graph is contained in 'graph'

#     def get_graph(self, directed=True):
#         """Returns a NetworkX multi-graph instance built from the result set
#         :param directed: boolean, optional (default=`True`).
#             Whether to create a direted or an undirected graph.
#         """
#         if nx is None:
#             raise ImportError("Try installing NetworkX first.")
#         if directed:
#             graph = nx.MultiDiGraph()
#         else:
#             graph = nx.MultiGraph()
#         for item in self._results.graph:
#             for node in item['nodes']:
#                 properties = copy.deepcopy(node['properties'])
#                 properties['labels'] = node['labels']
#                 graph.add_node(node['id'], **properties)
#             for rel in item['relationships']:
#                 properties = copy.deepcopy(rel['properties'])
#                 properties.update(
#                     id=rel['id'],
#                     type=rel['type']
#                 )
#                 graph.add_edge(rel['startNode'], rel['endNode'],
#                                key=rel.get('type'), **properties)
# return graph
