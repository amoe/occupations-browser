import pytest
import unittest.mock
from occubrow.backend import OccubrowBackend


# Because we have a specialized isomorphic test, the actual (numeric) identity
# of the nodes doesn't matter, as long as they are in the correct arrangement.

EXPECTED_DATA = {
    'directed': True,
    'graph': {},
    'links': [{'source': 1, 'target': 2, 'type': 'KNOWS'}],
    'multigraph': False,
    'nodes': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
}


def test_can_retrieve_entire_graph(neo4j_driver):
    backend = OccubrowBackend(neo4j_driver)

    with neo4j_driver.session() as session:
        session.run("MATCH (a) DETACH DELETE a")
        session.run("CREATE (a:Person {name:'Alice'})-[:KNOWS]->({name:'Bob'})")
        assert backend.graph_matches(EXPECTED_DATA)
    

 # def can_retrieve_entire_graph_mocked():
 #    # mock_neo4j_driver = unittest.mock.Mock()
 #    # mock_neo4j_driver.
    

 #    backend = OccubrowBackend(mock_neo4j_driver)
    
 #    with neo4j_driver.session() as session:
 #        session.run("MATCH (a) DETACH DELETE a")
 #        session.run("CREATE (a:Person {name:'Alice'})-[:KNOWS]->({name:'Bob'})")
 #        assert backend.graph_matches(EXPECTED_DATA)
