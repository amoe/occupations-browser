from occubrow.backend import OccubrowBackend
from occubrow.constants import MOCKED_UUID
from occubrow.identifier_functions import random_uuid, get_predictable_uuid_generator
from occubrow.test_utility import make_backend, ncreated, rcreated
from occubrow.neo4j_repository import RealNeo4jRepository
from unittest.mock import Mock, call
from occubrow.canned_statements import CreateGroupNodeQuery, CreateGroupLink
import pytest
import pprint

def test_create_group():
    repository = Mock()
    backend = OccubrowBackend(repository, identifier_function=lambda: MOCKED_UUID)

    # Make sure assertions pass
    repository.run_canned_statement.side_effect = [
        ncreated(1), rcreated(1), rcreated(1), rcreated(1)
    ]
    compound_id = backend.create_group(['Oil', 'Oyl'])
    assert compound_id == MOCKED_UUID


def test_correct_neo4j_calls_happened():
    repository = Mock()
    backend = OccubrowBackend(repository, identifier_function=lambda: MOCKED_UUID)
    repository.run_canned_statement.side_effect = [
        ncreated(1), rcreated(1), rcreated(1)
    ]
    compound_id = backend.create_group(['Oil', 'Oyl'])

    # We can make more detailed assertions about the query structure
    # when we use statement objects instaed of raw strings
    repository.run_canned_statement.assert_has_calls([
        call(CreateGroupNodeQuery(MOCKED_UUID)),
        call(CreateGroupLink(MOCKED_UUID, 'Oil')),
        call(CreateGroupLink(MOCKED_UUID, 'Oyl'))
    ])
