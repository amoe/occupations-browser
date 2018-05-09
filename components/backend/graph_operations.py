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

    # Roots index is a dictionary that's mapping from a string to the array
    # index.  This is a little bit weird perhaps but it's just more clear to
    # me for some reason, given that the array of roots is the correct
    # end-representation.
    roots_index = {
        'foo': 0,
        
    }

    with driver.session() as session:
        with session.begin_transaction() as tx:
            results = tx.run(READ_ENTIRE_GRAPH_QUERY)
            # results is of type BoltStatementResult
            return results
