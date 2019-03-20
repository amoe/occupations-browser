from occubrow.backend import OccubrowBackend
from occubrow.constants import MOCKED_UUID
from occubrow.identifier_functions import random_uuid, get_predictable_uuid_generator
from occubrow.test_utility import make_backend, ncreated, rcreated
from occubrow.neo4j_repository import RealNeo4jRepository
from unittest.mock import Mock, call
from occubrow.canned_statements import CreateGroupNodeQuery, CreateGroupLink
import occubrow.system
import pytest
import pprint

def get_mocked_uuid_backend(repository, the_uuid):
    return occubrow.system.get_backend({
        'repository': repository,
        'identifier_function': lambda: the_uuid
    })

def test_create_group():
    repository = Mock()
    backend = get_mocked_uuid_backend(repository, MOCKED_UUID)

    # Make sure assertions pass
    repository.run_canned_statement.side_effect = [
        ncreated(1), rcreated(1), rcreated(1), rcreated(1)
    ]
    compound_id = backend.create_group(['Oil', 'Oyl'])
    assert compound_id == MOCKED_UUID


def test_correct_neo4j_calls_happened():
    repository = Mock()
    backend = get_mocked_uuid_backend(repository, MOCKED_UUID)

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


EXPECTED_DATA_AFTER_GROUP_CREATION = {
    'directed': True,
    'graph': {},
    'links': [{'firstIndex': True,
               'index': 0,
               'source': 0,
               'target': 32,
               'type': 'CONTAINS'},
              {'index': 1, 'source': 0, 'target': 33, 'type': 'CONTAINS'},
              {'index': 2, 'source': 0, 'target': 34, 'type': 'CONTAINS'},
              {'index': 3, 'source': 0, 'target': 3, 'type': 'CONTAINS'},
              {'index': 4, 'source': 0, 'target': 26, 'type': 'CONTAINS'},
              {'index': 5,
               'lastIndex': True,
               'source': 0,
               'target': 27,
               'type': 'CONTAINS'},
              {'source': 29, 'target': 33, 'type': 'GROUP_CONTAINS'},
              {'source': 29, 'target': 27, 'type': 'GROUP_CONTAINS'}],
    'multigraph': False,
    'nodes': [{'content': ['The', 'oyl', 'man', 'brought', 'the', 'oil'],
               'id': 0,
               'label': 'Sentence',
               'uuid': '00000000-0000-0000-0000-000000000000'},
              {'content': 'The', 'id': 32, 'label': 'Token'},
              {'content': 'man', 'id': 34, 'label': 'Token'},
              {'content': 'brought', 'id': 3, 'label': 'Token'},
              {'content': 'oyl', 'id': 33, 'label': 'Token'},
              {'content': 'the', 'id': 26, 'label': 'Token'},
              {'content': 'oil', 'id': 27, 'label': 'Token'},
              {'id': 29,
               'label': 'Group',
               'uuid': '00000000-0000-0000-0000-000000000001'}]
}

@pytest.mark.functional
def test_groups_are_inserted_to_db(neo4j_driver):
    repository = RealNeo4jRepository(neo4j_driver)
    backend = occubrow.system.get_backend({
        'identifier_function': get_predictable_uuid_generator
    })


    backend.add_sentence_with_tokens(['The', 'oyl', 'man', 'brought', 'the', 'oil'])
    backend.create_group(['oyl', 'oil'])
    backend.dump_internal_graph()
    assert backend.graph_matches(EXPECTED_DATA_AFTER_GROUP_CREATION)
