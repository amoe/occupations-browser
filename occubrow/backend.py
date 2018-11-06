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

def check_round_trip():
    g1 = rebuild_graph(pull_graph())
    data = networkx.readwrite.json_graph.node_link_data(g1)
    g2 = networkx.readwrite.json_graph.node_link_graph(data)
    return strict_eq(g1, g2)

def strict_eq(g1, g2):
    return networkx.is_isomorphic(g1, g2, node_match=operator.eq, edge_match=operator.eq)


class OccubrowBackend(object):
    def __init__(self, driver):
        self.driver = driver

    def pull_graph(self):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                results = tx.run(ENTIRE_GRAPH_QUERY)
                row = results.single()
                return {
                    'rels': row.value('rels'),
                    'nodes': row.value('nodes')
                }

    def export_graph(self):
        return networkx.readwrite.json_graph.node_link_data(
            rebuild_graph(pull_graph())
        )

    def graph_matches(self, data):
        return strict_eq(
            rebuild_graph(self.pull_graph()), 
            networkx.readwrite.json_graph.node_link_graph(data)
        )
