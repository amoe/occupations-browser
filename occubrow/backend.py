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
        merged_node_properties = {'label': node.get_label()}
        merged_node_properties.update(node.get_properties())

        g.add_node(
            node.get_id(), **node.get_properties()
        )

    for rel in results['rels']:
        g.add_edge(
            rel.get_start_node(),
            rel.get_end_node(),
            **rel.get_properties(),
            type=rel.get_type()
        )

    return g

# Not actually tested but this property should definitely hold true.
def check_round_trip():
    g1 = rebuild_graph(pull_graph())
    data = networkx.readwrite.json_graph.node_link_data(g1)
    g2 = networkx.readwrite.json_graph.node_link_graph(data)
    return strict_eq(g1, g2)

def strict_eq(g1, g2):
    return networkx.is_isomorphic(g1, g2, node_match=operator.eq, edge_match=operator.eq)


class OccubrowBackend(object):
    def __init__(self, repository):
        self.repository = repository

    def export_graph(self):
        return networkx.readwrite.json_graph.node_link_data(
            rebuild_graph(self.repository.pull_graph())
        )

    def graph_matches(self, data):
        return strict_eq(
            rebuild_graph(self.repository.pull_graph()), 
            networkx.readwrite.json_graph.node_link_graph(data)
        )

    def import_taxonomy(self, taxonomy_data):
        """
        Import taxonomy data.  Data should be a JSON tree (in the sense defined
        by networkx).
        """
        pass

