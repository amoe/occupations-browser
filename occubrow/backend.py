import neo4j

ENTIRE_GRAPH_QUERY = """
    MATCH ()-[r]->()
    WITH COLLECT(r) AS rels
    MATCH (n)
    RETURN rels, COLLECT(n) AS nodes
"""

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7687"
driver = neo4j.GraphDatabase.driver(uri, auth=credentials)

def pull_graph():
    with driver.session() as session:
        with session.begin_transaction() as tx:
            results = tx.run(ENTIRE_GRAPH_QUERY)

            row = results.single()

            for rel in row.value('rels'):
                print("Relationship:", rel)

            for node in row.value('nodes'):
                print("Node:", node)
                
    
