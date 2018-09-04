import neo4j
import neo4j.v1
import networkx
import functools
import pprint
import occubrow.demo_taxonomy
from occubrow.plotting import quickplot
import logging
from logging import debug, info

# relationship_name here is 'precedes'
APOC_TREE_GENERATOR_QUERY = """
    MATCH p = (:Token {content: "the"})-[:PRECEDES*]->(end:Token) 
    WHERE NOT (end)-[:PRECEDES]->()
    CALL apoc.convert.toTree([p]) YIELD value
    RETURN value
"""

# relationship_name here is 'supercategory_of'
TAXONOMY_TREE_QUERY = """
    MATCH p = (ta1:Taxon)-[:SUPERCATEGORY_OF*]->(ta2:Taxon)
    WHERE NOT (ta2)-[:SUPERCATEGORY_OF]->()
    CALL apoc.convert.toTree([p]) YIELD value
    RETURN value;
"""

GET_ROOTS_WITH_SUBSTRING_MATCH = """
    MATCH (t1:Token)<-[r:CONTAINS]-(s1:Sentence)
    WHERE r.index = 0 AND t1.content CONTAINS {substring}
    RETURN DISTINCT t1 AS root
"""

GET_ALL_ROOTS_QUERY = """
    MATCH (t1:Token)<-[r:CONTAINS]-(s1:Sentence)
    WHERE r.index = 0
    RETURN DISTINCT t1 AS root
"""

## XXX: REMOVE -- START
___PULL_ALL_TOKEN_SEQUENCES = """
    MATCH (s1:Sentence)-[r:CONTAINS]->(t)
    WITH s1, t
    ORDER BY r.index
    RETURN s1, COLLECT(t) AS seq;
"""
### XXX: REMOVE -- END 

PULL_ALL_TOKEN_SEQUENCES = """
    MATCH (s1:Sentence)-[r:CONTAINS]->(t)-[r2:MEMBER_OF]->(ta:Taxon)
    WITH s1, t, ta
    ORDER BY r.index
    RETURN s1, COLLECT({token: t, taxon: ta}) AS seq
"""

DECLARE_GROUP_QUERY = """
    MATCH (s:Token {content: {synonym}}), (m:Token {content: {master}})
    CREATE (s)-[:SYNONYMOUS]->(m)
"""

IDENTITY_FIELD_NAME = 'content'


def tree_to_graph(tree, relationship_name):
    # defined by apoc, precedes is based on the relationship label
    object_format = dict(id='_id', children=relationship_name)
    return networkx.tree_graph(tree, object_format)

def add_linear_nodes(g, token_seq):
    for index, token in enumerate(token_seq):
        node_identity = token[IDENTITY_FIELD_NAME]
        g.add_node(node_identity, taxon=token['taxon'])

        if index != 0:
            previous_node = token_seq[index - 1][IDENTITY_FIELD_NAME]
            g.add_edge(previous_node, node_identity)

# Version of dfs_tree that copies node attributes (as the dfs_tree in networkx
# will strip them).
def dfs_tree_with_node_attributes(g, source, depth_limit):
    edges = networkx.dfs_edges(g, source=source, depth_limit=depth_limit)
    result = networkx.DiGraph()

    for u, v in edges:
        result.add_node(u, **g.nodes[u])
        result.add_node(v, **g.nodes[v])
        result.add_edge(u, v)

    return result

# Flatten the nodes into a narrowed representation which is appropriate for the
# tree conversion
def gather_token_seq(result_seq):
    ret = []
    
    for datum in result_seq:
        # Each datum is a map with keys 'token' and 'taxon' containing
        # node-interface objects.
        
        token_node = datum['token']
        taxon_node = datum['taxon']

        # Destructure and flatten the list
        ret.append(
            {
                'content': token_node.get('content'),
                'taxon': taxon_node.get('name')
            }
        )

    return ret

class Neo4jRepository(object):
    port = None

    def __init__(self, port=7876):
        self.port = port

    def query(self, query, parameters):
        uri = "bolt://localhost:%d" % self.port

        with neo4j.v1.GraphDatabase.driver(uri) as driver:
            with driver.session() as session:
                with session.begin_transaction() as tx:
                    results = tx.run(query, parameters)
                    return results

    def get_tree(self, query, relationship_name):
        result = self.query(query, {})
        paths = result.value()
        get_graph = lambda p: tree_to_graph(p, relationship_name)
        return functools.reduce(networkx.compose, map(get_graph, paths), networkx.DiGraph())

    def clear_all(self):
        self.query("MATCH (n) DETACH DELETE n", {})

    def add_taxonomy(self):
        occubrow.demo_taxonomy.load_demo_taxonomy(self)

    def get_roots_with_substring_match(self, substring):
        return [
            record['root'].get('content')
            for record in self.query(GET_ROOTS_WITH_SUBSTRING_MATCH, {'substring': substring})
        ]

    # This is going to pull in the entire graph
    # Because we are using DiGraph and not MultiDiGraph it's going to automatically
    # remove duplicate edges for us.
    def pull_graph(self):
        graph = networkx.DiGraph()
        results = self.query(PULL_ALL_TOKEN_SEQUENCES, {})

        for result in results:
            token_seq = gather_token_seq(result.get('seq'))
            add_linear_nodes(graph, token_seq)

        return graph

    def get_tree_by_root(self, root, depth_limit):
        g = self.pull_graph()

        # Although the returned graph here is already tree-structured, it might
        # be too deep to return to the client.  So we use DFS to limit depth.

        tree = dfs_tree_with_node_attributes(g, root, depth_limit=depth_limit)
        return networkx.tree_data(tree, root)

    def declare_group(self, synonym, master):
        results = self.query(DECLARE_GROUP_QUERY, {'synonym': synonym, 'master': master})

    def get_taxonomy_as_json(self):
        dg = self.get_tree(TAXONOMY_TREE_QUERY, 'supercategory_of')

        # This essentially gets the (assumed to be single!) root of the tree.
        try:
            root = next(networkx.topological_sort(dg))
        except StopIteration as e:
            raise Exception("empty taxonomy?") from e

        # This is just the default tree-json format, but we prefer to be explicit 
        # about it
        attrs = {
            'children': 'children',
            'id': 'id'
        }
        dg_formatted_as_tree = networkx.tree_data(
            dg, root=root, attrs=attrs
        )

        return dg_formatted_as_tree
        
