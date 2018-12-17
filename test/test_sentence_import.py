import pytest
from occubrow.test_utility import make_backend
from occubrow.neo4j_repository import RealNeo4jRepository


EXPECTED_DATA = {
    'directed': True,
    'graph': {},
    'links': [{'index': 3,
               'lastIndex': True,
               'source': 3,
               'target': 8,
               'type': 'CONTAINS'},
              {'firstIndex': True,
               'index': 0,
               'source': 3,
               'target': 4,
               'type': 'CONTAINS'},
              {'index': 2, 'source': 3, 'target': 7, 'type': 'CONTAINS'}],
    'multigraph': False,
    'nodes': [{'content': 'Dinner', 'id': 8, 'label': 'Token'},
              {'content': ['Winner', 'Winner', 'Chicken', 'Dinner'],
               'id': 3,
               'label': 'Sentence',
               'uuid': '9cb34c17-da37-46fa-9e21-233f9eca01c4'},
              {'content': 'Winner', 'id': 4, 'label': 'Token'},
              {'content': 'Chicken', 'id': 7, 'label': 'Token'}]
}

sample_sentence = ["Winner", "Winner", "Chicken", "Dinner"]

# NB: Should factor the two parts (precedes+tezra) schema to the repository
# then backend add_sentence just combines these calls
# so this test should run against the repository
# directly using the repository is the only way that we can produce
# the graph above because the normal backend add-sentence procedure would create
# a more complicated graph including PRECEDES links

@pytest.mark.functional
def test_sentence_import(neo4j_driver):
    repository = RealNeo4jRepository(neo4j_driver)
    backend = make_backend(repository)
    repository.add_sentence_with_tokens(sample_sentence)
    assert backend.graph_matches(EXPECTED_DATA)
