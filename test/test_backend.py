from occubrow.backend import OccubrowBackend
import pytest

sample_sentence = """
I wish I had never come here, and I don't want to see no more magic.
"""

# We define our expected node-based representation for the sentence.
# This will involve a single Sentence node and a bunch of Token nodes.
# The number of token nodes will be equal to the unique set of tokens derived
# from tokenizing this sentence.

EXPECTED_DATA = {}

@pytest.mark.skip
def test_add_sentence(neo4j_driver):
    backend = occubrow.OccubrowBackend(neo4j_driver)
    backend.add_sentence(sample_sentence)
    assert backend.graph_matches(EXPECTED_DATA)
