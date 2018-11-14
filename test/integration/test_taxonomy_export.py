import pytest
import copy
from occubrow.backend import OccubrowBackend
from occubrow.neo4j_repository import RealNeo4jRepository

# functional test, note that this shows that we actually don't have a 1 to 1
# translation between these formats which is probably not the best, perhaps
# we should mandate the 'content' format for input as well?

EXPECTED_EXPORT_DATA = {
    'children': [{'content': 'Rock', 'id': 1, 'label': 'Taxon'},
                 {'content': 'Classical', 'id': 2, 'label': 'Taxon'}],
    'content': 'Music',
    'id': 0,
    'label': 'Taxon'
}

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

def remove_ids_from_tree(t):
    t.pop('id', None)
    for child in t.get('children', []):
        remove_ids_from_tree(child)
        
def tree_matches(t1, t2):
    t1_new = copy.deepcopy(t1)
    t2_new = copy.deepcopy(t2)
    remove_ids_from_tree(t1_new)
    remove_ids_from_tree(t2_new)
    return t1_new == t2_new

@pytest.mark.functional
def test_can_export_taxonomy_tree(neo4j_driver):
    backend = OccubrowBackend(RealNeo4jRepository(neo4j_driver))
    backend.import_taxonomy(input_data)
    root = 'Music'
    tree_data = backend.export_taxonomy_tree(root)
    assert tree_matches(tree_data, EXPECTED_EXPORT_DATA)
    
