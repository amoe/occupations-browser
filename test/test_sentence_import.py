import pytest
from occubrow.backend import OccubrowBackend
from occubrow.neo4j_repository import RealNeo4jRepository

EXPECTED_DATA = {
    'directed': True,
    'graph': {},
    'links': [{'index': 2, 'source': 7, 'target': 0, 'type': 'CONTAINS'},
              {'firstIndex': True,
               'index': 0,
               'source': 7,
               'target': 8,
               'type': 'CONTAINS'},
              {'index': 3,
               'lastIndex': True,
               'source': 7,
               'target': 3,
               'type': 'CONTAINS'}],
    'multigraph': False,
    'nodes': [{'content': 'Chicken', 'id': 0},
              {'content': 'Winner', 'id': 8},
              {'content': 'Dinner', 'id': 3},
              {'content': 'Winner Winner, Chicken Dinner',
               'id': 7,
               'uuid': '545b07d6-6903-4549-847e-044c61326b0c'}]
}


sample_sentence = """
Winner Winner, Chicken Dinner
"""


# NB: Should factor the two parts (precedes+tezra) schema to the repository
# then backend add_sentence just combines these calls
# so this test should run against the repository
# directly using the repository is the only way that we can produce
# the graph above because the normal backend add-sentence procedure would create
# a more complicated graph including PRECEDES links

@pytest.mark.functional
def test_sentence_import(neo4j_driver):
    repository = RealNeo4jRepository(neo4j_driver)
    backend = OccubrowBackend(repository)
    repository.add_sentence(sample_sentence)
    assert backend.graph_matches(EXPECTED_DATA)
