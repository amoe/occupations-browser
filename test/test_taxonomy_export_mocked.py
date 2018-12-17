import pytest
import unittest.mock
from occubrow.test_utility import make_backend
from occubrow.types import Node, Relationship

PRELOADED_TAXONOMY = {
    'nodes': [
        Node(0, 'Taxon', {'content': 'Music'}),
        Node(1, 'Taxon', {'content': 'Rock'}),
        Node(2, 'Taxon', {'content': 'Classical'})
    ],
    'rels': [
        Relationship(0, 1, {}, 'SUPERCATEGORY_OF'),
        Relationship(0, 2, {}, 'SUPERCATEGORY_OF')
    ]
}

EXPECTED_EXPORT_DATA = {
    'children': [{'content': 'Rock', 'id': 1, 'label': 'Taxon'},
                 {'content': 'Classical', 'id': 2, 'label': 'Taxon'}],
    'content': 'Music',
    'id': 0,
    'label': 'Taxon'
}


def get_mocked_repository():
    mock_neo4j_repository = unittest.mock.Mock()
    mock_neo4j_repository.get_all_taxonomies.return_value = PRELOADED_TAXONOMY
    return mock_neo4j_repository

def test_taxonomy_export():
    repository = get_mocked_repository()
    b = make_backend(repository)
    root = 'Music'
    tree_data = b.export_taxonomy_tree(root)
    assert tree_data == EXPECTED_EXPORT_DATA
    
    
