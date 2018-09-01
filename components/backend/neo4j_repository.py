import neo4j
import neo4j.v1
import networkx
import matplotlib
import matplotlib.pyplot
import functools
import pprint
import demo_taxonomy

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

def tree_to_graph(tree, relationship_name):
    # defined by apoc, precedes is based on the relationship label
    object_format = dict(id='_id', children=relationship_name)
    return networkx.tree_graph(tree, object_format)

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
        demo_taxonomy.load_demo_taxonomy(self)
        
