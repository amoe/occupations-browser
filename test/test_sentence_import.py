import pytest

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

@pytest.mark.functional
def test_sentence_import(neo4j_driver):
    backend = OccubrowBackend(RealNeo4jRepository(neo4j_driver))
    backend.add_single_sentence(sample_sentence)
    assert backend.graph_matches(EXPECTED_DATA)
