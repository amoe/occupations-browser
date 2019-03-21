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


def is_null_graph(g):
    return g.number_of_nodes() == 0 and g.number_of_edges() == 0


def remove_cycles(g):
    """
    Remove cycles from graph g.  Modifies g in-place.
    """
    cycles_left = True
    while cycles_left:
        try:
            cycles = networkx.find_cycle(g)
            #print(cycles)
            g.remove_edges_from(cycles)
        except networkx.exception.NetworkXNoCycle as e:
            cycles_left = False


def diagnose_nontree(g, purported_root):
    g2 = networkx.dfs_tree(g, purported_root)

    print("EDGE COUNT=", g.number_of_edges())
    print("EDGE COUNT=", g2.number_of_edges())
    edge_diff = g.edges() - g2.edges()
    print("Missing edges in tree:", edge_diff)

    print("NODE COUNT=", g.number_of_nodes())
    print("NODE COUNT=", g2.number_of_nodes())
    node_diff = g.nodes() - g2.nodes()
    print("Missing nodes in tree:", node_diff)

    if edge_diff or node_diff:
        return False
    return True


def is_iterable(value):
    try:
        iter(value)
        return True
    except TypeError:
        return False
    
    


def find_root_by_content(g, wanted):
   sources = [v for v, indegree in g.in_degree() if indegree == 0]
   valid_sources = [n for n, content in g.nodes(data='content') if content == wanted]

   if not valid_sources:
       raise errors.NoRootsFoundError()

   if len(valid_sources) != 1:
       raise errors.AmbiguousRootError()

   return valid_sources[0]

