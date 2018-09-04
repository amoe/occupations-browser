import unittest.mock
import occubrow.neo4j_repository
import pytest
import logging
from logging import debug

STUB_TREE_DATA = [
   {
       'seq': [
           {
               'token': {'content': 'foo', '_type': 'Token'},
               'taxon': {'name': 'Ulmaridae', '_type': 'Taxon'}
           },
           {
               'token': {'content': 'bar', '_type': 'Token'},
               'taxon': {'name': 'Deepstaria', '_type': 'Taxon'}
           }
       ],
       's1': {'_type': 'Sentence', 'content': ['foo', 'bar']}
   }
]

@pytest.mark.unit
def test_get_tree():
    obj = occubrow.neo4j_repository.Neo4jRepository()
    obj.query = unittest.mock.Mock(return_value=STUB_TREE_DATA)
    result = obj.get_tree_by_root('foo', 1)
    debug("result is %s", result)
    assert result == {
        'id': 'foo',
        'foobar': 42,
        'children': [
            {'id': 'bar', 'foobar': 42}
        ]
    }
