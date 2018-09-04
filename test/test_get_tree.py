import unittest.mock
import occubrow.neo4j_repository
import pytest

STUB_TREE_DATA = [
   {
       'seq': [
           {'content': 'foo', '_type': 'Token'},
           {'content': 'bar', '_type': 'Token'}
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

