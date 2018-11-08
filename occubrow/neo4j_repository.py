import neo4j
import occubrow.types

ENTIRE_GRAPH_QUERY = """
    MATCH ()-[r]->()
    WITH COLLECT(r) AS rels
    MATCH (n)
    RETURN rels, COLLECT(n) AS nodes
"""

def shim_node(node):
    return occubrow.types.Node(
        node.id, dict(node.items())
    )

def shim_relationship(relationship):
    return occubrow.types.Relationship(
        relationship.start_node.id,
        relationship.end_node.id,
        dict(relationship.items()),
        relationship.type
    )
 
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
                return {
                    'nodes': [shim_node(n) for n in row.value('nodes')],
                    'rels': [shim_relationship(r) for r in row.value('rels')]
                }

    def run_statement(self, execution_spec):
        pass


def demo():
    repo = RealNeo4jRepository()
    return repo.pull_graph()
