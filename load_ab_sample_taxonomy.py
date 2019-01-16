import occubrow.taxonomy.hierarchical_xlsx
from occubrow.drawing import quickplot
import sys
import networkx
import occubrow.utility


def do_load(path, artificial_root_content):
    loader = occubrow.taxonomy.hierarchical_xlsx.HierarchicalXlsxTaxonomyLoader(
        path, '2019-01-16'
    )
    g, root_uri = loader.run(reparent_node=artificial_root_content)
    print(networkx.is_tree(g))
    print(g.number_of_nodes())
    print(g.number_of_edges())
    ok = occubrow.utility.diagnose_nontree(g, root_uri)
    if not ok: raise Exception('pod bay doors')
