import neo4j

driver = neo4j.GraphDatabase.driver("bolt://localhost:7688", auth=('neo4j', 'password'))

def create_indexes():
    print("Creating indexes.")
    with driver.session() as session:
        session.run("CREATE INDEX ON :Token(content)")
        session.run("CREATE INDEX ON :Taxon(key)")
    print("Created indexes.")

