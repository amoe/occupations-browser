import pytest
import unittest.mock
from occubrow.backend import OccubrowBackend
from occubrow.types import Node, Relationship

PRELOADED_TAXONOMY = {
    'nodes': [
        Node(0, 'Taxon', {'name': 'Music'}),
        Node(1, 'Taxon', {'name': 'Rock'}),
        Node(2, 'Taxon', {'name': 'Classical'})
    ],
    'rels': [
        Relationship(0, 1, {}, 'SUPERCATEGORY_OF'),
        Relationship(0, 2, {}, 'SUPERCATEGORY_OF')
    ]
}

EXPECTED_EXPORT_DATA = {
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

def get_mocked_repository():
    mock_neo4j_repository = unittest.mock.Mock()
    mock_neo4j_repository.pull_graph.return_value = PRELOADED_TAXONOMY
    return mock_neo4j_repository


def test_taxonomy_export():
    repository = get_mocked_repository()
    b = OccubrowBackend(repository)
    root = 'Music'
    tree_data = b.export_taxonomy_tree(root)
    assert tree_data == EXPECTED_EXPORT_DATA
    
    
