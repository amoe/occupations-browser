import occubrow.system
from occubrow.drawing import quickplot
import networkx
import pprint

query_filters = [
    "tag:solasistim.net,2018-12-28:occubrow/Place/1",
    "tag:solasistim.net,2018-12-28:occubrow/Vehicle/1"
]


b = occubrow.system.get_backend()
r = b.search_with_taxons('keep', query_filters)

pprint.pprint(r)

# for rel in r['rels']:
#     print(rel.start_node)
#     print(rel.end_node)

# print(repr(r))
# pprint.pprint(networkx.node_link_data(r))
# quickplot(r)
