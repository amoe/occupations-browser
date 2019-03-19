from occubrow.backend import OccubrowBackend
from occubrow.test_utility import make_backend
from unittest.mock import Mock
from occubrow.types import Node, Relationship
import pytest
import pprint

# Note that the root data doesn't have a strength
WANTED_DATA = {
    'children': [{'children': [{'content': 'shop', 'id': 2, 'label': 'Token', 'strength': 1},
                               {'content': 'bar', 'id': 3, 'label': 'Token', 'strength': 1}],
                  'content': 'a',
                  'id': 1,
                  'label': 'Token',
                  'strength': 1},
                 {'children': [{'content': 'peace', 'id': 5, 'label': 'Token', 'strength': 1},
                               {'content': 'books', 'id': 6, 'label': 'Token', 'strength': 1}],
                  'content': 'the',
                  'id': 4,
                  'label': 'Token',
                  'strength': 1}],
    'strength': None,
    'content': 'keep',
    'id': 0,
    'label': 'Token'
}

PRELOADED_SENTENCES = {
    'nodes': [
        Node(0, 'Token', {'content': 'keep'}),
        Node(1, 'Token', {'content': 'a'}),
        Node(2, 'Token', {'content': 'shop'}),
        Node(3, 'Token', {'content': 'bar'}),
        Node(4, 'Token', {'content': 'the'}),
        Node(5, 'Token', {'content': 'peace'}),
        Node(6, 'Token', {'content': 'books'}),
    ],
    'rels': [
        # Only the PRECEDES links are actually used to form the tree.
        Relationship(0, 1, {'occurrences': 1}, 'PRECEDES'),
        Relationship(1, 2, {'occurrences': 1}, 'PRECEDES'),
        Relationship(1, 3, {'occurrences': 1}, 'PRECEDES'),
        Relationship(0, 4, {'occurrences': 1}, 'PRECEDES'),
        Relationship(4, 5, {'occurrences': 1}, 'PRECEDES'),
        Relationship(4, 6, {'occurrences': 1}, 'PRECEDES')
    ]
}


def test_get_tree():
    repository = Mock()
    backend = make_backend(repository)
    repository.pull_graph.return_value = PRELOADED_SENTENCES

    assert backend.get_token_tree('keep', 4, 0) == WANTED_DATA
