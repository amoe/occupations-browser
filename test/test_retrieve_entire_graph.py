import pytest

def test_can_retrieve_entire_graph(neo4j_driver):
    with neo4j_driver.session() as session:
        session.run("MATCH (a) DETACH DELETE a")
        session.run("CREATE (a:Person {name:'Alice'})-[:KNOWS]->({name:'Bob'})")

    
