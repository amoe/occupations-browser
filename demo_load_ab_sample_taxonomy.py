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


do_load("/home/amoe/download/Dave/Activities.xlsx", 'Activities')
do_load("/home/amoe/download/Dave/Place.xlsx", 'Place')
do_load("/home/amoe/download/Dave/Object.xlsx", 'Object')
do_load("/home/amoe/download/Dave/Instiutions.xlsx", None)
do_load("/home/amoe/dev/occubrow/backend/scripts/modified_sample_occupation_taxonomy.xlsx", 'Occupation')

