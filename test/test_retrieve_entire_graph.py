import pytest
import occubrow.backend

EXPECTED_DATA = {
    'directed': True,
    'graph': {},
    'links': [{'source': 57, 'target': 58, 'type': 'KNOWS'}],
    'multigraph': False,
    'nodes': [{'id': 57, 'name': 'Alice'}, {'id': 58, 'name': 'Bob'}]
}


def test_can_retrieve_entire_graph(neo4j_driver):
    with neo4j_driver.session() as session:
        session.run("MATCH (a) DETACH DELETE a")
        session.run("CREATE (a:Person {name:'Alice'})-[:KNOWS]->({name:'Bob'})")
        occubrow.backend.assert_graph(EXPECTED_DATA)
    
