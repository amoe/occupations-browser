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


def get_sample_place_graph():
    g = networkx.DiGraph()

    g.add_node('Place')
    g.add_node('Pub')
    g.add_node('Shop'),
    g.add_node('Clothes shop'),

    g.add_edge('Place', 'Pub')
    g.add_edge('Place', 'Shop')
    g.add_edge('Shop', 'Clothes shop')

    return g


def get_sample_object_graph():
    g = networkx.DiGraph()

    g.add_node('Object')
    g.add_node('Alcoholic drink')
    g.add_node('Vehicle'),
    g.add_node('Clothes'),
    g.add_node('Bricks'),

    g.add_edge('Object', 'Alcoholic drink')
    g.add_edge('Object', 'Vehicle')
    g.add_edge('Object', 'Clothes')
    g.add_edge('Object', 'Bricks')

    return g
