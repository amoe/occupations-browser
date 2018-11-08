from occubrow.backend import OccubrowBackend
from occubrow.neo4j_repository import RealNeo4jRepository
from unittest.mock import call, Mock
import occubrow.errors
from pytest import raises
import pytest
import pprint

INPUT_TAXONOMY = {}

def test_import_empty_taxonomy_throws():
    backend = OccubrowBackend(repository=Mock())

    # We don't know how to locate the taxonomy with no root, so there's not
    # much option other than to throw.  Remember there could be multiple
    # taxonomies in the database.
    with raises(occubrow.errors.EmptyTaxonomyError):
        backend.import_taxonomy(INPUT_TAXONOMY)


def test_single_root_taxonomy_imports():
    input_data = {
        'id': 'A_Single_Root'
    }

    mock_repository = Mock()
    runmock = mock_repository.run_statement
    backend = OccubrowBackend(mock_repository)
    backend.import_taxonomy(input_data)

    runmock.assert_called_once_with(
        'CREATE (t:Taxon {content: $content})', content='A_Single_Root'
    )

def test_small_taxonomy_imports():
    input_data = {
        'id': 'Music',
        'children': [
            {
                'id': 'Rock',
                'children': []
            },
            {
                'id': 'Classical',
                'children': []
            }
        ]
    }

    # For the isolated test, we check that the backend submits the correct
    # Cypher query to the repository.  We can't really test on raw strings
    # because we use NPD's feature of parameterized queries.  So we have to
    # shim the driver's "run" interface and test against that instead.
    # 
    # The use of $properties here is a bit unfortunate because it's shared
    # knowledge between the tests & code.

    mock_repository = Mock()
    runmock = mock_repository.run_statement
    backend = OccubrowBackend(mock_repository)
    backend.import_taxonomy(input_data)

    calls = [
        call('CREATE (t:Taxon {content: $content})', content='Music'),
        call('CREATE (t:Taxon {content: $content})', content='Rock'),
        call('CREATE (t:Taxon {content: $content})', content='Classical'),

        call('MATCH (t1:Taxon {content: $start_node}), (t2:Taxon {content: $end_node})\n                CREATE (t1)-[:SUPERCATEGORY_OF]->(t2)', end_node='Rock', start_node='Music'),
        call('MATCH (t1:Taxon {content: $start_node}), (t2:Taxon {content: $end_node})\n                CREATE (t1)-[:SUPERCATEGORY_OF]->(t2)', end_node='Classical', start_node='Music')
    ]

    runmock.assert_has_calls(calls, any_order=True)



@pytest.mark.functional
def test_import_worked(neo4j_driver):
    input_data = {
        'id': 'Music',
        'children': [
            {
                'id': 'Rock',
                'children': []
            },
            {
                'id': 'Classical',
                'children': []
            }
        ]
    }

    expected_graph = {'directed': True,
                      'graph': {},
                      'links': [{'source': 0, 'target': 1, 'type': 'SUPERCATEGORY_OF'},
                                {'source': 0, 'target': 2, 'type': 'SUPERCATEGORY_OF'}],
                      'multigraph': False,
                      'nodes': [{'content': 'Music', 'id': 0},
                                {'content': 'Rock', 'id': 1},
                                {'content': 'Classical', 'id': 2}]}


    backend = OccubrowBackend(RealNeo4jRepository(neo4j_driver))
    backend.import_taxonomy(input_data)
    assert backend.graph_matches(expected_graph)
