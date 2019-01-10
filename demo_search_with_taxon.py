import occubrow.system
from occubrow.drawing import quickplot
import networkx
import pprint

b = occubrow.system.get_backend()
r = b.search_with_taxon('keep', 'tag:solasistim.net,2018-12-28:occubrow/Vehicle/1')

# print(networkx.node_link_data(g))
