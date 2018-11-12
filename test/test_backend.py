from occubrow.backend import OccubrowBackend
import pytest

sample_sentence = """
I wish I had never come here, and I don't want to see no more magic.
"""

# We define our expected node-based representation for the sentence.
# This will involve a single Sentence node and a bunch of Token nodes.
# The number of token nodes will be equal to the unique set of tokens derived
# from tokenizing this sentence.

EXPECTED_DATA = {
    'directed': True,
    'graph': {},
    'links': [],
    'multigraph': False,
    'nodes': [
        {'id': 1, 'token': "I"},
        {'id': 2, 'token': "wish"},
        {'id': 3, 'token': "had"},
        {'id': 3, 'token': "never"},
        {'id': 3, 'token': "come"},
        {'id': 3, 'token': "here"},
        {'id': 3, 'token': "and"},
        {'id': 3, 'token': "don't"},
        {'id': 3, 'token': "want"},
        {'id': 3, 'token': "to"},
        {'id': 3, 'token': "see"},
        {'id': 3, 'token': "no"},
        {'id': 3, 'token': "more"},
        {'id': 3, 'token': "magic"}
    ]
}

@pytest.mark.skip("not fleshed out yet")
def test_add_sentence(neo4j_driver):
    backend = OccubrowBackend(neo4j_driver)
    backend.add_sentence(sample_sentence)
    assert backend.graph_matches(EXPECTED_DATA)

