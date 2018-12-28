import networkx

def get_sample_occupation_graph():
    g = networkx.DiGraph()

    g.add_node('Occupation')
    g.add_node('Manage')
    g.add_node('Serve'),
    g.add_node('Drive'),
    g.add_node('Transport')

    g.add_edge('Occupation', 'Manage')
    g.add_edge('Occupation', 'Serve')
    g.add_edge('Occupation', 'Drive')
    g.add_edge('Occupation', 'Transport')
    return g
