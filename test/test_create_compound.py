from occubrow.backend import OccubrowBackend
from occubrow.constants import MOCKED_UUID
from occubrow.identifier_functions import random_uuid, get_predictable_uuid_generator
from occubrow.test_utility import make_backend, ncreated, rcreated
from occubrow.neo4j_repository import RealNeo4jRepository
from occubrow.canned_statements import CreateCompoundNodeQuery
from unittest.mock import Mock
import pytest
import pprint

EXPECTED_DATA = {
    'directed': True,
    'graph': {},
    'links': [{'source': 9, 'target': 8, 'type': 'CONTAINS'},
              {'source': 9, 'target': 28, 'type': 'CONTAINS'},
              {'source': 9, 'target': 29, 'type': 'CONTAINS'},
              {'firstIndex': True,
               'index': 0,
               'source': 6,
               'target': 8,
               'type': 'CONTAINS'},
              {'index': 1, 'source': 6, 'target': 28, 'type': 'CONTAINS'},
              {'index': 2,
               'lastIndex': True,
               'source': 6,
               'target': 29,
               'type': 'CONTAINS'}],
    'multigraph': False,
    'nodes': [{'content': 'Dog', 'id': 8, 'label': 'Token'},
              {'id': 9, 'label': 'Compound', 'uuid': '00000000-0000-0000-0000-000000000001'},
              {'content': 'and', 'id': 28, 'label': 'Token'},
              {'content': 'Duck', 'id': 29, 'label': 'Token'},
              {'content': ['Dog', 'and', 'Duck'],
               'id': 6,
               'label': 'Sentence',
               'uuid': '00000000-0000-0000-0000-000000000000'}]
}

def test_create_compound():
    repository = Mock()
    backend = OccubrowBackend(repository, identifier_function=lambda: MOCKED_UUID)
    repository.run_canned_statement.side_effect = [ncreated(1)]
    repository.run_statement.side_effect = [
        rcreated(1), rcreated(1), rcreated(1)
    ]
    compound_id = backend.create_compound(['Dog', 'and', 'Duck'])
    assert compound_id == MOCKED_UUID


def test_correct_neo4j_calls_happened():
    repository = Mock()
    backend = OccubrowBackend(repository, identifier_function=lambda: MOCKED_UUID)
    repository.run_canned_statement.side_effect = [ncreated(1)]
    repository.run_statement.side_effect = [
        rcreated(1), rcreated(1), rcreated(1)
    ]

    compound_id = backend.create_compound(['Dog', 'and', 'Duck'])

    # We can make more detailed assertions about the query structure
    # when we use statement objects instaed of raw strings
    repository.run_canned_statement.assert_called_once_with(
        CreateCompoundNodeQuery(MOCKED_UUID)
    )
    assert repository.run_canned_statement.call_count == 1
    assert repository.run_statement.call_count == 3

# DISABLED -- Pending refactoring of the uuid-using code into the backend
# from repository -- Repository becomes a dumb layer
@pytest.mark.functional
def test_compounds_are_inserted_to_db(neo4j_driver):
    repository = RealNeo4jRepository(neo4j_driver)
    backend = OccubrowBackend(repository, get_predictable_uuid_generator())
    backend.add_sentence_with_tokens(['Dog', 'and', 'Duck'])
    backend.create_compound(['Dog', 'and', 'Duck'])
    backend.dump_internal_graph()
    assert backend.graph_matches(EXPECTED_DATA)
