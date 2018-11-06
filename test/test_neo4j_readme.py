# This is adapted from test_readme.py in the neo4j-python-driver git repository.

def test_simple_2(neo4j_driver):
    names = set()
    print = names.add

    def print_friends(tx, name):
        for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) "
                             "WHERE a.name = {name} "
                             "RETURN friend.name", name=name):
            names.add(record["friend.name"])

    with neo4j_driver.session() as session:
        session.run("MATCH (a) DETACH DELETE a")
        session.run("CREATE (a:Person {name:'Alice'})-[:KNOWS]->({name:'Bob'})")
        session.read_transaction(print_friends, "Alice")

    assert len(names) == 1
    assert "Bob" in names
