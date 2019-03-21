import json
import occubrow.mmconverter.process
import pprint
import networkx
import pdb
import random
from occubrow.utility \
  import dfs_tree_with_node_attributes, diagnose_nontree

with open('test_data/large_mm_response.json', 'r') as f:
    structure = json.load(f)


mmconverter = occubrow.mmconverter.process.MicromacroConverter()
g = mmconverter.get_graph(structure)

chosen_source = random.choice(list(g))

g2 = dfs_tree_with_node_attributes(g, chosen_source, depth_limit=3)
data = networkx.tree_data(g2, root=chosen_source)
pprint.pprint(data)

#pdb.set_trace()

# sources = [v for v, indegree in g.in_degree() if indegree == 0]
# if not sources:
#     raise Exception('no roots')

# chosen_source = sources[0]

# print("Chosen source was '%s'" % chosen_source)

# diagnose_nontree(g2, chosen_source)

# print("Converting to tree")
# data = networkx.tree_data(g2, root=chosen_source)
