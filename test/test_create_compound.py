from occubrow.backend import OccubrowBackend
from occubrow.constants import MOCKED_UUID
from occubrow.identifier_functions import random_uuid
from unittest.mock import Mock
import pytest

EXPECTED_EXPORT_DATA = {
    'children': [{'content': 'Rock', 'id': 1, 'label': 'Taxon'},
                 {'content': 'Classical', 'id': 2, 'label': 'Taxon'}],
    'content': 'Music',
    'id': 0,
    'label': 'Taxon'
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

# @pytest.mark.functional
# def test_compounds_are_inserted_to_db(neo4j_driver):
#     backend = make_backend(RealNeo4jRepository(neo4j_driver))
#     backend.create_compound(['Dog', 'and', 'Duck')
#     assert tree_matches(tree_data, EXPECTED_EXPORT_DATA)
    


