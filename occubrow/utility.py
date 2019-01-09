import re
import networkx
import pdb

def collapse(qry):
    return re.sub(r'\s+', ' ', qry)

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


def get_node_by_attribute(g, attribute_name, attribute_value):
    result_set = [x for x, y in g.nodes(data=True) if y[attribute_name] == attribute_value]

    if not result_set:
        raise Exception("attribute value not found")

    if len(result_set) > 1:
        raise Exception("ambiguous result")

    return result_set[0]
