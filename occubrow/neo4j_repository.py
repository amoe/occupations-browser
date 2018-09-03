import neo4j
import neo4j.v1
import networkx
import matplotlib
import matplotlib.pyplot
import functools
import pprint
import occubrow.demo_taxonomy

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

PULL_ALL_TOKEN_SEQUENCES = """
    MATCH (s1:Sentence)-[r:CONTAINS]->(t)
    WITH s1, t
    ORDER BY r.index
    RETURN s1, COLLECT(t) AS seq;
"""

DECLARE_GROUP_QUERY = """
    MATCH (s:Token {content: {synonym}}), (m:Token {content: {master}})
    CREATE (s)-[:SYNONYMOUS]->(m)
"""

def tree_to_graph(tree, relationship_name):
    # defined by apoc, precedes is based on the relationship label
    object_format = dict(id='_id', children=relationship_name)
    return networkx.tree_graph(tree, object_format)

def add_linear_nodes(g, token_seq):
    for index, token in enumerate(token_seq):
        g.add_node(token)

        if index != 0:
            start_node = token_seq[index - 1]
            g.add_edge(start_node, token)

def gather_token_seq(result_seq):
    ret = []
    
    for node in result_seq:
        ret.append(node.get('content'))

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
            token_seq = gather_token_seq(result['seq'])
            add_linear_nodes(graph, token_seq)

        return graph

    def get_tree_by_root(self, root, depth_limit):
        g = self.pull_graph()
        tree = networkx.dfs_tree(g, root, depth_limit=depth_limit)
        return networkx.tree_data(tree, root)

    def declare_group(self, synonym, master):
        results = self.query(DECLARE_GROUP_QUERY, {'synonym': synonym, 'master': master})

