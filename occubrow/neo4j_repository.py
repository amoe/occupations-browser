import neo4j
import occubrow.types
import occubrow.queries
from logging import debug
import uuid


ENTIRE_GRAPH_QUERY = """
    MATCH ()-[r]->()
    WITH COLLECT(r) AS rels
    MATCH (n)
    RETURN rels, COLLECT(n) AS nodes
"""

UPDATE_QUERY = """
    MATCH (t1:Token {content: $content1})-[r:PRECEDES]-(t2:Token {content: $content2})
    SET r.occurrences = r.occurrences + 1;
"""

INSERT_QUERY = """
    MATCH (t1:Token {content: $content1}), (t2:Token {content: $content2})
    CREATE (t1)-[:PRECEDES {occurrences: 1}]->(t2)
"""

MERGE_NODE_QUERY = """
    MERGE (t:Token {content: $content})
"""


def shim_node(node):
    labels = node.labels

    # Nodes should always have one and only one label under our data model
    if len(labels) != 1:
        raise Exception("node should have one label, corruption likely")

    # can't index into a frozenset so just pick an arbitrary one
    label = next(iter(labels))

    return occubrow.types.Node(
        node.id, label, dict(node.items())
    )

def shim_relationship(relationship):
    return occubrow.types.Relationship(
        relationship.start_node.id,
        relationship.end_node.id,
        dict(relationship.items()),
        relationship.type
    )

def merge_node(session, content):
    session.run(MERGE_NODE_QUERY, content=content)

def create_or_increment_precedes_relationship(session, start_node, end_node):
    with session.begin_transaction() as tx:
        result = tx.run(UPDATE_QUERY, content1=start_node, content2=end_node)
        property_set_count = result.summary().counters.properties_set
        print("Property set count = %d" % property_set_count)
        
        if property_set_count == 0:
            tx.run(INSERT_QUERY, content1=start_node, content2=end_node)


def shim_subgraph_result(row):
    return {
        'nodes': [shim_node(n) for n in row.value('nodes')],
        'rels': [shim_relationship(r) for r in row.value('rels')]
    }

 
class RealNeo4jRepository(object):
    def __init__(self):
        self.driver = neo4j.GraphDatabase.driver(uri="bolt://localhost:7687")

    def __init__(self, driver):
        self.driver = driver

    def pull_graph(self):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                results = tx.run(ENTIRE_GRAPH_QUERY)
                row = results.single()
                return shim_subgraph_result(row)


    # wrapper to allow asserting calls on this type
    def run_statement(self, statement, parameters=None, **kwparameters):
        with self.driver.session() as session:
            result = session.run(statement, parameters, **kwparameters)

        return result


    def add_precedes_links(self, phrase):
        """
        Add only the precedes links for one sentence.  This will only add a part
        of the database structure for a given sentence.  Phrase should be
        a tokenized list.
        """
        first_idx = 0
        last_idx = len(phrase) - 1

        for index in range(last_idx):
            start_node = phrase[index]
            end_node = phrase[index + 1]

            self._merge_sentence_links(start_node, end_node)

    def _merge_sentence_links(self, start_node, end_node):
        debug("Relationship: %s -> %s", start_node, end_node)

        with self.driver.session() as session:
            merge_node(session, start_node)
            merge_node(session, end_node)
            create_or_increment_precedes_relationship(session, start_node, end_node)

    def get_all_taxonomies(self):
        with self.driver.session() as session:
            r = session.run(occubrow.queries.SLURP_TAXONOMIES)
            return shim_subgraph_result(r.single())
    
def demo():
    repo = RealNeo4jRepository()
    return repo.pull_graph()
