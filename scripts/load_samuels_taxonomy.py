import networkx
import openpyxl
import sys
from logging import debug, info, warn

def quickplot(g):
    import matplotlib.pyplot as plt
    import networkx as nx
    plt.clf()
    labels = networkx.get_node_attributes(g, 'content')
    networkx.draw_networkx(g, labels=labels, pos=nx.kamada_kawai_layout(g))
    plt.show()


wb = openpyxl.load_workbook(sys.argv[1])
sheet = wb.active


def form_record(row):
    return {
        't1': row[1],
        't2': row[2],
        't3': row[3],
        't4': row[4],
        't5': row[5],
        't6': row[6],
        't7': row[7],
        'concat': row[9],
        'samuels_heading': row[17]
    }

def record_to_category_sequence(rec):
    wanted_keys = ['t1', 't2', 't3', 't4', 't5', 't6', 't7']
    return [rec[k] for k in wanted_keys]

def get_concat_id(seq, index):
    return ''.join(filter(None, seq[:index + 1]))

g = networkx.DiGraph()

for row in sheet.iter_rows(min_row=2):
    cell_values = [c.value for c in row]
    rec = form_record(cell_values)
    if not rec['t1']:
        warn("Strange record encountered, skipping: %s", rec)


    category_sequence = record_to_category_sequence(rec)

    last_index = len(category_sequence) - 1

    this_category_node_id = get_concat_id(category_sequence, last_index)
    g.add_node(this_category_node_id, content=rec['samuels_heading'])

    for index in range(last_index):
        u = get_concat_id(category_sequence, index)
        v = get_concat_id(category_sequence, index + 1)

        t_u = category_sequence[index]
        t_v = category_sequence[index + 1]

        # We reached the end of links for this row
        if t_u is None or t_v is None:
            break

        g.add_edge(u, v)


print("Nodes: %d, edges: %d" % (g.number_of_nodes(), g.number_of_edges()))

# if g.number_of_nodes() != g.number_of_edges() + 1:
#     raise TypeError("G is not a tree.")

g2 = networkx.dfs_tree(g, '01')

#leftovers = networkx.difference(g, g2)
#print(leftovers.nodes)

g1set = set()
for x in g.nodes:
    g1set.add(x)

g2set = set()
for x in g2.nodes:
    g2set.add(x)

diff = g1set - g2set

print("Size of g1set =", len(g1set))
print("Size of g2set =", len(g2set))


print("Size of g2 =", g2.number_of_nodes())


sources = [v for v, indegree in g.in_degree() if indegree == 0]

print("Possible roots:", sources)


emptystring = networkx.dfs_tree(g, '')
print("DFS from empty string:", emptystring.number_of_nodes())

# ... so, a large part of the graph is disconnected


#networkx.write_gexf(g, 'out.gexf')




