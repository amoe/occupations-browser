import neo4j.v1
import occubrow.demo_taxonomy

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7688"

def clear_all():
    with neo4j.v1.GraphDatabase.driver(uri, auth=credentials) as driver:
        with driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run("MATCH (n) DETACH DELETE n", {})

def add_taxonomy():
    demo_taxonomy.load_demo_taxonomy()
