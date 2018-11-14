import networkx
import openpyxl
import sys

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
    print(rec)

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

#quickplot(g)

networkx.write_gexf(g, 'out.gexf')


