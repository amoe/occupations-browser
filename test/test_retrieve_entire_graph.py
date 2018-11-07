import pytest
import unittest.mock
from occubrow.backend import OccubrowBackend
from occubrow.neo4j_repository import RealNeo4jRepository
from occubrow.types import Node, Relationship


# Because we have a specialized isomorphic test, the actual (numeric) identity
# of the nodes doesn't matter, as long as they are in the correct arrangement.

EXPECTED_DATA = {
    'directed': True,
    'graph': {},
    'links': [{'source': 1, 'target': 2, 'type': 'KNOWS'}],
    'multigraph': False,
    'nodes': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
}


# Integration version
def test_can_retrieve_entire_graph(neo4j_driver):
    backend = OccubrowBackend(RealNeo4jRepository(neo4j_driver))

    with neo4j_driver.session() as session:
        session.run("MATCH (a) DETACH DELETE a")
        session.run("CREATE (a:Person {name:'Alice'})-[:KNOWS]->({name:'Bob'})")
        assert backend.graph_matches(EXPECTED_DATA)

# Isolated version
def test_can_retrieve_entire_graph_mocked():
    mock_neo4j_repository = unittest.mock.Mock()

    mock_neo4j_repository.pull_graph.return_value = {
        'nodes': [
            Node(1, {'name': 'Alice'}), Node(2, {'name': 'Bob'})
        ],
        'rels': [
            Relationship(1, 2, {}, 'KNOWS')
        ]
    }

    backend = OccubrowBackend(mock_neo4j_repository)

    # This is just going to no-op
    mock_neo4j_repository.execute("MATCH (a) DETACH DELETE a")
    mock_neo4j_repository.execute("CREATE (a:Person {name:'Alice'})-[:KNOWS]->({name:'Bob'})")

    assert backend.graph_matches(EXPECTED_DATA)
