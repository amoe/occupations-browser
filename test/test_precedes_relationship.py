import pytest
from occubrow.test_utility import make_backend
from occubrow.neo4j_repository import RealNeo4jRepository

EXPECTED_DATA = {
    'directed': True,
    'graph': {},
    'links': [{'occurrences': 1, 'source': 0, 'target': 3, 'type': 'PRECEDES'},
              {'occurrences': 1, 'source': 0, 'target': 20, 'type': 'PRECEDES'},
              {'occurrences': 1, 'source': 1, 'target': 2, 'type': 'PRECEDES'},
              {'occurrences': 2, 'source': 2, 'target': 0, 'type': 'PRECEDES'},
              {'occurrences': 1, 'source': 20, 'target': 1, 'type': 'PRECEDES'}],
    'multigraph': False,
    'nodes': [{'content': 'foo', 'id': 0, 'label': 'Token'},
              {'content': 'baz', 'id': 1, 'label': 'Token'},
              {'content': 'quux', 'id': 2, 'label': 'Token'},
              {'content': 'fry', 'id': 3, 'label': 'Token'},
              {'content': 'bar', 'id': 20, 'label': 'Token'}]
}

phrases = [
    ["foo", "bar", "baz"],
    ["quux", "foo", "fry"],
    ["baz", "quux", "foo"]
]

# This functionality belongs in the repository, and shouldn't be directly in the
# backend, because it's only a smaller piece of the full transaction structure
# for adding a sentence.

@pytest.mark.functional
def test_precedes_relationship(neo4j_driver):
    repository = RealNeo4jRepository(neo4j_driver)
    backend = make_backend(repository)

    for phrase in phrases:
        repository.add_precedes_links(phrase)

    assert backend.graph_matches(EXPECTED_DATA)
