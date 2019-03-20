import json
import pprint
import util
import domain
import networkx
import sys

# Version of dfs_tree that copies node attributes (as the dfs_tree in networkx
# will strip them).  Source is actually root.
def dfs_tree_with_node_attributes(g, source, depth_limit=None):
    result = networkx.DiGraph()
    # in the special case where there's no edges, just return the root
    if g.number_of_edges() == 0:
        return g
    edges = networkx.dfs_edges(g, source=source, depth_limit=depth_limit)
    # coerce from generator to ease debugging
    edges_list = list(edges)
    for u, v in edges_list:
        result.add_node(u, **g.nodes[u])
        result.add_node(v, **g.nodes[v])
        result.add_edge(u, v)
    return result


def quickplot(g):
    import matplotlib.pyplot as plt
    import networkx as nx
    plt.clf()
    labels = networkx.get_node_attributes(g, 'content')
    networkx.draw_networkx(g, labels=labels, pos=nx.kamada_kawai_layout(g))
    plt.show()


with open('two-responses.json', 'r') as f:
    structure = json.load(f)

assert util.is_iterable(structure)

g = networkx.DiGraph()

# just accepting a callback here to allow deferring decision about whether to
# flatten spans or not
def process_spans(structure, handle_spans):
    for datum in structure:
        span_jsons = datum['text-token']['spans']
        spans = [
            domain.span_from_json(s) for s in span_jsons
        ]
        handle_spans(spans)

all_spans = []
process_spans(structure, lambda s: all_spans.extend(s))
pprint.pprint(all_spans)

last_idx = len(all_spans) - 1
for index in range(last_idx):
    antecedent = all_spans[index]
    postcedent = all_spans[index + 1]
    
    g.add_node(antecedent.with_value, content=antecedent.with_value)
    g.add_node(postcedent.with_value, content=postcedent.with_value)
    g.add_edge(antecedent.with_value, postcedent.with_value)

sources = [v for v, indegree in g.in_degree() if indegree == 0]
g2 = dfs_tree_with_node_attributes(g, sources[0], depth_limit=None)
data = networkx.tree_data(g2, root=sources[0])

json.dump(data, sys.stdout, indent=4)
print()


