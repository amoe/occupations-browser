import occubrow.taxonomy.hierarchical_xlsx
from occubrow.drawing import quickplot
import sys
import networkx
import occubrow.utility


loader = occubrow.taxonomy.hierarchical_xlsx.HierarchicalXlsxTaxonomyLoader(
    sys.argv[1], '2019-01-16'
)
g, root_uri = loader.run(reparent_node='Place')

print(networkx.is_tree(g))
print(g.number_of_nodes())
print(g.number_of_edges())
#print(networkx.tree_data(g, 'Place'))
print(occubrow.utility.diagnose_nontree(g, root_uri))
quickplot(g)

