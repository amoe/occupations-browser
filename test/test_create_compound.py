from occubrow.backend import OccubrowBackend
from occubrow.constants import MOCKED_UUID
from occubrow.identifier_functions import random_uuid
from occubrow.test_utility import make_backend
from occubrow.neo4j_repository import RealNeo4jRepository
from unittest.mock import Mock
import pytest
import pprint

EXPECTED_DATA = {
    'directed': True,
    'graph': {},
    'links': [{'source': 1, 'target': 2, 'type': 'KNOWS'}],
    'multigraph': False,
    'nodes': [
        {'id': 1, 'name': 'Alice', 'label': 'Person'},
        {'id': 2, 'name': 'Bob', 'label': 'Person'}
    ]
}


def test_create_compound():
    repository = Mock()
    backend = OccubrowBackend(repository, identifier_function=lambda: MOCKED_UUID)
    compound_id = backend.create_compound(['Dog', 'and', 'Duck'])
    assert compound_id == MOCKED_UUID


def test_correct_neo4j_calls_happened():
    repository = Mock()
    backend = OccubrowBackend(repository, identifier_function=lambda: MOCKED_UUID)
    compound_id = backend.create_compound(['Dog', 'and', 'Duck'])
    assert repository.run_statement.call_count == 4

@pytest.mark.functional
def test_compounds_are_inserted_to_db(neo4j_driver):
    backend = make_backend(RealNeo4jRepository(neo4j_driver))
    backend.create_compound(['Dog', 'and', 'Duck'])
    pprint.pprint(backend.export_graph())
    assert backend.graph_matches(EXPECTED_DATA)
