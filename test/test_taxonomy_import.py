from occubrow.backend import OccubrowBackend
from unittest.mock import Mock
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

