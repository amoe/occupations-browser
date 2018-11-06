import neo4j
import networkx
import networkx.readwrite.json_graph
from occubrow.drawing import quickplot
import operator

ENTIRE_GRAPH_QUERY = """
    MATCH ()-[r]->()
    WITH COLLECT(r) AS rels
    MATCH (n)
    RETURN rels, COLLECT(n) AS nodes
"""

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7687"
driver = neo4j.GraphDatabase.driver(uri, auth=credentials)

def pull_graph():
    with driver.session() as session:
        with session.begin_transaction() as tx:
            results = tx.run(ENTIRE_GRAPH_QUERY)
            row = results.single()
            return {
                'rels': row.value('rels'),
                'nodes': row.value('nodes')
            }

# Rebuild the graph in memory, converting from the NPD wrapper structures
# to Networkx structures
def rebuild_graph(results):
    g = networkx.DiGraph()
    
    for node in results['nodes']:
        g.add_node(
            node.id, **dict(node.items())
        )

    for rel in results['rels']:
        g.add_edge(
            rel.start_node.id, 
            rel.end_node.id, 
            **dict(rel.items()), 
            type=rel.type
        )
        
    return g

def export_graph():
    return networkx.readwrite.json_graph.node_link_data(
        rebuild_graph(pull_graph())
    )

def strict_eq(g1, g2):
    return networkx.is_isomorphic(g1, g2, node_match=operator.eq, edge_match=operator.eq)

def check_round_trip():
    g1 = rebuild_graph(pull_graph())
    data = networkx.readwrite.json_graph.node_link_data(g1)
    g2 = networkx.readwrite.json_graph.node_link_graph(data)
    return strict_eq(g1, g2)

EXPECTED_DATA = {
    'directed': True,
    'graph': {},
    'links': [{'source': 57, 'target': 58, 'type': 'KNOWS'}],
    'multigraph': False,
    'nodes': [{'id': 57, 'name': 'Alice'}, {'id': 58, 'name': 'Bob'}]
}

def assert_graph(data):
    return strict_eq(
        rebuild_graph(pull_graph()), 
        networkx.readwrite.json_graph.node_link_graph(data)
    )
