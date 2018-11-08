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


def test_single_root_taxonomy_imports():
    input_data = {
        'id': 'A_Single_Root'
    }

    # For the isolated test, we check that the backend submits the correct
    # Cypher query to the repository.  Really we want to be able to do
    # non-string-matching on this.  We will have to experiment to get this
    # value.

    expected_cypher = """
       
    """

    backend = OccubrowBackend(repository=Mock())
    backend.import_taxonomy(input_data)
    # TODO: Speak to the mock to verify that expected_cypher was asked
#    assert backend.graph_matches(expected_data)
