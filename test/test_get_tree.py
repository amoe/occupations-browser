import unittest.mock
import occubrow.neo4j_repository
import pytest

STUB_TREE_DATA = [
   {
       'seq': [
           {
               'token': {'content': 'foo', '_type': 'Token'},
               'taxon': {'content': 'Ulmaridae', '_type': 'Taxon'}
           },
           {
               'token': {'content': 'bar', '_type': 'Token'},
               'taxon': {'content': 'Deepstaria', '_type': 'Taxon'}
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
    assert result == {
        'id': 'foo',
        'children': [
            {'id': 'bar'}
        ]
    }
