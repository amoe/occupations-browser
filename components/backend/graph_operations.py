#! /usr/bin/env python3

import matplotlib
import matplotlib.pyplot
import networkx
import pprint
import neo4j
import neo4j.v1

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7687"

driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

# This is the one you need, it operates with v2 of the rs2graph code below 
# Note that the node with content 'the' is at the root here
# There's a bug here because it's not going to return absolute leaf nodes at all
# So that will fail with an empty result set causing strict_first to raise
# an exception.
INSANE_GRAPH_QUERY = """
    MATCH (a:Token {content: {root}})-[:PRECEDES*]->(t:Token)
    WITH COLLECT(a) + COLLECT(DISTINCT t) AS nodes_
    UNWIND nodes_ AS n
    OPTIONAL MATCH p = (n)-[r]-()
    WITH n AS n2, COLLECT(DISTINCT RELATIONSHIPS(p)) AS nestedrel
    RETURN n2, REDUCE(output = [], rel in nestedrel | output + rel) AS rels
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

def strict_first(seq):
    if not seq:
        raise Exception("seq is falsy")

    if len(seq) != 1:
        raise Exception("unexpected number of items in seq")

    return seq[0]

def get_tree_by_root(root):
    graph = rs2graph_v3(run_some_query(INSANE_GRAPH_QUERY, {'root': root}))
    root_id = strict_first(find_nodes_by_content_attribute(graph, root))
    return networkx.tree_data(graph, root_id)

def find_nodes_by_content_attribute(g, wanted):
    return [
        n for n, d in g.nodes(data=True) if d['content'] == wanted 
    ]


# this version expects a collection of rels in the variable 'rels'
# But, this version doesn't handle dangling references
def rs2graph_v2(rs):
    graph = networkx.MultiDiGraph()

    for record in rs:
        node = record['n2']
        if not node:
            raise Exception('every row should have a node')

        print("adding node")
        nx_properties = {}
        nx_properties.update(node.properties)
        nx_properties['labels'] = list(node.labels)
        graph.add_node(node.id, **nx_properties)

        relationship_list = record['rels']

        for relationship in relationship_list:
            print("adding edge")
            graph.add_edge(
                relationship.start, relationship.end, key=relationship.type,
                **relationship.properties
            )

    return graph


# This version has to materialize the entire node set up front in order
# to check for dangling references.  This may induce memory problems in large
# result sets
def rs2graph_v3(rs):
    graph = networkx.MultiDiGraph()

    materialized_result_set = list(rs)
    node_id_set = set([
        record['n2'].id for record in materialized_result_set
    ])

    for record in materialized_result_set:
        node = record['n2']
        if not node:
            raise Exception('every row should have a node')

        print("adding node")
        nx_properties = {}
        nx_properties.update(node.properties)
        nx_properties['labels'] = list(node.labels)
        graph.add_node(node.id, **nx_properties)

        relationship_list = record['rels']

        for relationship in relationship_list:
            print("adding edge")

            # Bear in mind that when we ask for all relationships on a node,
            # we may find a node that PRECEDES the current node -- i.e. a node
            # whose relationship starts outside the current subgraph returned
            # by this query.
            if relationship.start in node_id_set:
                graph.add_edge(
                    relationship.start, relationship.end, key=relationship.type,
                    **relationship.properties
                )
            else:
                print("ignoring dangling relationship [no need to worry]")

    return graph
