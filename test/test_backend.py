import occubrow
import pytest

sample_sentence = "I wish I had never come here, and I don't want to see no more magic"

#call apoc.export.graphml.all('yourPath/exportAll.graphml',null)

# Assert graph against a graphml representation
# The problem is, how to get APOC configured?
# And we also need to be able to compare two things.  We could take

@pytest.mark.skip
def test_add_sentence():
    backend = occubrow.OccubrowBackend()
    backend.add_sentence(sample_sentence)
    backend.assert_graph({})
