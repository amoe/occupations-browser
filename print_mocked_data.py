import occubrow.backend
from unittest.mock import Mock
import networkx
from occubrow.drawing import quickplot
import json
import pprint

sentences = [
    'keep a bar',
    'keep a shop',
    'keep the peace',
    'keep the books'
]


backend = occubrow.backend.OccubrowBackend(Mock(), Mock())

g = networkx.DiGraph()

def consecutive_pairs(sequence):
    for i in range(len(sequence) - 1):
        yield sequence[i], sequence[i + 1]

for sentence in sentences:
    tokens = backend.preprocess(sentence)

    for token1, token2 in consecutive_pairs(tokens):
        g.add_node(token1)
        g.add_node(token2)
        g.add_edge(token1, token2)

result = networkx.tree_data(g, 'keep')



pprint.pprint(result)
