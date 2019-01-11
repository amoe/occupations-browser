import occubrow.system
from occubrow.drawing import quickplot
import networkx
import pprint

b = occubrow.system.get_backend()
r = b.search_with_taxon('keep', ['tag:solasistim.net,2018-12-28:occubrow/Vehicle/1'])

pprint.pprint(r)

# for rel in r['rels']:
#     print(rel.start_node)
#     print(rel.end_node)

# print(repr(r))
# pprint.pprint(networkx.node_link_data(r))
# quickplot(r)
