from occubrow.backend import OccubrowBackend
from occubrow.test_utility import make_backend
from unittest.mock import Mock

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

def test_get_tree():
    repository = Mock()
    backend = make_backend(repository)
    assert backend.get_tree() == WANTED_DATA
