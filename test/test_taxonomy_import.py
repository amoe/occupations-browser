from occubrow.backend import OccubrowBackend
from unittest.mock import call, Mock
import occubrow.errors
from pytest import raises

EXPECTED_DATA = {
    'directed': True,
    'graph': {},
    'links': [],
    'multigraph': False,
    'nodes': []
}

INPUT_TAXONOMY = {}

def test_import_empty_taxonomy_throws():
    backend = OccubrowBackend(repository=Mock())

    # We don't know how to locate the taxonomy with no root, so there's not
    # much option other than to throw.  Remember there could be multiple
    # taxonomies in the database.
    with raises(occubrow.errors.EmptyTaxonomyError):
        backend.import_taxonomy(INPUT_TAXONOMY)


# def test_single_root_taxonomy_imports():
#     input_data = {
#         'id': 'A_Single_Root'
#     }

#     # For the isolated test, we check that the backend submits the correct
#     # Cypher query to the repository.  We can't really test on raw strings
#     # because we use NPD's feature of parameterized queries.  So we have to
#     # shim the driver's "run" interface and test against that instead.
#     # 
#     # The use of $properties here is a bit unfortunate because it's shared
#     # knowledge between the tests & code.

#     expected_cypher_params = {
#         'statement': "CREATE (t:Taxon $properties)",
#         'parameters': None,
#         'kwparameters': {
#             'properties': {
#                 'content': 'A_Single_Root'
#             }
#         }
#     }

#     mock_repository = Mock()
#     backend = OccubrowBackend(mock_repository)
#     backend.import_taxonomy(input_data)

#     mock_repository.run_statement.assert_called_once_with(
#         expected_cypher_params
#     )
    

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

