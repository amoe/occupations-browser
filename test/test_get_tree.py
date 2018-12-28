from occubrow.backend import OccubrowBackend
from occubrow.test_utility import make_backend
from unittest.mock import Mock
from occubrow.types import Node, Relationship
import pytest
import pprint


WANTED_DATA = {
    'children': [{'children': [{'id': 'St.', 'taxon': None},
                               {'id': 'waggon', 'taxon': None}],
                  'id': 'the',
                  'taxon': None},
                 {'children': [{'id': 'shop', 'taxon': None}],
                  'id': 'a',
                  'taxon': None}],
    'id': 'keep',
    'taxon': None
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


        Node(7, 'Sentence', {'content': ['keep', 'a', 'shop']}),
        Node(8, 'Sentence', {'content': ['keep', 'a', 'bar']}),
        Node(9, 'Sentence', {'content': ['keep', 'the', 'peace']}),
        Node(10, 'Sentence', {'content': ['keep', 'the', 'books']})
    ],
    'rels': [
        Relationship(7, 0, {}, 'CONTAINS'),
        Relationship(7, 1, {}, 'CONTAINS'),
        Relationship(7, 2, {}, 'CONTAINS'),

        Relationship(8, 0, {}, 'CONTAINS'),
        Relationship(8, 1, {}, 'CONTAINS'),
        Relationship(8, 3, {}, 'CONTAINS'),

        Relationship(9, 0, {}, 'CONTAINS'),
        Relationship(9, 4, {}, 'CONTAINS'),
        Relationship(9, 5, {}, 'CONTAINS'),

        Relationship(10, 0, {}, 'CONTAINS'),
        Relationship(10, 4, {}, 'CONTAINS'),
        Relationship(10, 6, {}, 'CONTAINS')
    ]
}


def test_get_tree():
    repository = Mock()
    backend = make_backend(repository)
    repository.pull_graph.return_value = PRELOADED_SENTENCES
    pprint.pprint(backend.get_tree('keep'))
