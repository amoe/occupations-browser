import neo4j
import neo4j.v1

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7687"

driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

READ_ENTIRE_GRAPH_QUERY = """
    MATCH (n) OPTIONAL MATCH (n)-[r]->() RETURN n, r
"""

def get_roots():
    roots = [
        {
            'content': 'foo'
        }
    ]

    with driver.session() as session:
        with session.begin_transaction() as tx:
            results = tx.run(READ_ENTIRE_GRAPH_QUERY)
            return roots
