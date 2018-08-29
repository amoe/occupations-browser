import neo4j.v1

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7688"

driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

with driver.session() as session:
    with session.begin_transaction() as tx:
        tx.run("MATCH (n) DETACH DELETE n", {})

