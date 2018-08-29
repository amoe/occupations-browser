import networkx
import misc

g = networkx.DiGraph()

FAMILY = "Ulmaridae"
GENUS1 = "Aurelia"
GENUS2 = "Deepstaria"
SPECIES1 = "Aurelia aurita"
SPECIES2 = "Aurelia labiata"
SPECIES3 = "Deepstaria enigmatica"
SPECIES4 = "Deepstaria reticulum"

g.add_node(FAMILY)
g.add_node(GENUS1)
g.add_node(GENUS2)
g.add_node(SPECIES1)
g.add_node(SPECIES2)
g.add_node(SPECIES3)
g.add_node(SPECIES3)

# Top level relationships
g.add_edge(FAMILY, GENUS1)
g.add_edge(FAMILY, GENUS2)

# Aurelia jellys
g.add_edge(GENUS1, SPECIES1)
g.add_edge(GENUS1, SPECIES2)

# Deepstaria jellys
g.add_edge(GENUS2, SPECIES3)
g.add_edge(GENUS2, SPECIES4)


MERGE_TAXON_QUERY = """
    MERGE (t1:Taxon {name: {name}})
"""

LINK_TAXA_QUERY = """
    MATCH (t1:Taxon {name: {u_name}}), (t2:Taxon {name: {v_name}})
    CREATE (t1)-[:SUPERCATEGORY_OF]->(t2)
"""


def load_demo_taxonomy():
    for edge in networkx.bfs_edges(g, FAMILY):
        u, v = edge
        misc.run_some_query(MERGE_TAXON_QUERY, {'name': u})
        misc.run_some_query(MERGE_TAXON_QUERY, {'name': v})
        misc.run_some_query(LINK_TAXA_QUERY, {'u_name': u, 'v_name': v})

