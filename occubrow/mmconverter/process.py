import networkx
import pprint
import pdb
import random

import occubrow.errors
from occubrow.mmconverter.domain import span_from_json
from occubrow.utility \
  import dfs_tree_with_node_attributes, is_iterable, remove_cycles, \
         diagnose_nontree


# just accepting a callback here to allow deferring decision about whether to
# flatten spans or not
def process_spans(structure, handle_spans):
    for datum in structure:
        span_jsons = datum['text-token']['spans']
        spans = [span_from_json(s) for s in span_jsons]
        handle_spans(spans)

class MicromacroConverter(object):
    token_sequence = 0
    token_index = {}

    def assign_or_fetch_id(self, token):
        if token in self.token_index:
            return self.token_index[token]
        else:
            self.token_sequence += 1
            self.token_index[token] = self.token_sequence
            return self.token_sequence

    def get_graph(self, structure):
        assert is_iterable(structure)

        g = networkx.DiGraph()
        all_spans = []
        process_spans(structure, lambda s: all_spans.extend(s))

        last_idx = len(all_spans) - 1
        for index in range(last_idx):
            antecedent = all_spans[index]
            postcedent = all_spans[index + 1]

            aid = self.assign_or_fetch_id(antecedent.with_value)
            pid = self.assign_or_fetch_id(postcedent.with_value)

            print("aid is", aid, "pid is", pid)
            
            g.add_node(aid, content=antecedent.with_value, strength=1)
            g.add_node(pid, content=postcedent.with_value, strength=1)
            g.add_edge(aid, pid)

        return g
    
    def get_tree_from_micromacro_result(self, structure):
        """
        Convert JSON data received from the Micromacro /query/select endpoint
        to a JSON-serialized tree structure suitable for visualization.
        """
        g = self.get_graph(structure)
        return self.narrow_graph_to_tree(g, random.choice(list(g)), 2)

    def narrow_graph_to_tree(
        self, graph, chosen_source, depth_limit, coocurrence_threshold
    ):
        chosen_source = random.choice(list(graph))
        g2 = dfs_tree_with_node_attributes(graph, chosen_source, depth_limit=depth_limit)
        data = networkx.tree_data(g2, root=chosen_source)
        return data
