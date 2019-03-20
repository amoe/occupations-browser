import networkx
from occubrow.mmconverter.domain import span_from_json
from occubrow.utility import dfs_tree_with_node_attributes, is_iterable
import pprint
import pdb


# just accepting a callback here to allow deferring decision about whether to
# flatten spans or not
def process_spans(structure, handle_spans):
    for datum in structure:
        span_jsons = datum['text-token']['spans']
        spans = [span_from_json(s) for s in span_jsons]
        handle_spans(spans)

class MicromacroConverter(object):
    def convert(self, structure):
        """
        Convert JSON data received from the Micromacro /query/select endpoint
        to a JSON-serialized tree structure suitable for visualization.
        """
        assert is_iterable(structure)

        g = networkx.DiGraph()
        all_spans = []
        process_spans(structure, lambda s: all_spans.extend(s))

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

        return data
