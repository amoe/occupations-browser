import networkx
import openpyxl
import sys
import matplotlib
import networkx.drawing
import matplotlib.pyplot
import networkx.readwrite.json_graph
import networkx.readwrite.gexf
import pprint
import heapq
import pprint

def quickplot(g):
    matplotlib.pyplot.clf()
    layout = networkx.drawing.kamada_kawai_layout(g)
    networkx.draw_networkx(g, pos=layout)
    matplotlib.pyplot.show()


# Booth-Armstrong file involves an excel sheet

wb = openpyxl.load_workbook(sys.argv[1])
sheet = wb.active

g = networkx.DiGraph()

def get_useful_cell_info(row_values):
    count = 0
    first_index = None


    for index, value in enumerate(row_values):
        if value is not None:
            count += 1
            if first_index is None:
                first_index = index

    return {
        'count': count,
        'first_index': first_index
    }


current_row = 0
should_continue = True

all_indices = []

while should_continue:
    should_continue = False

    level_indices = []
    for row in sheet:
        this_row_index = row[0].row
        row_values = [x.value for x in row]
        info = get_useful_cell_info(row_values)
        first_index = info['first_index']
        if first_index > current_row:
            should_continue = True
            continue

        if first_index < current_row:
            # We already handled it so ignore
            continue

        if first_index == current_row:
            level_indices.append({
                'row_index': this_row_index,
                'content': row_values[first_index]
            })

    all_indices.append(level_indices)
    current_row += 1


def find_parent(indices, child_row, child_level):
    table = indices[child_level - 1]

    last_item = None
    
    for item in table:
        if item['row_index'] < child_row:
            last_item = item

    return last_item
    

for level, table in enumerate(all_indices):
    for item in table:
        g.add_node(item['content'])

        if level > 0:
            parent = find_parent(all_indices, item['row_index'], level)
            g.add_edge(parent['content'], item['content'])


print("nodes = %d", g.number_of_nodes())
print("edges = %d", g.number_of_edges())

for node, in_degree in g.in_degree():
    if in_degree == 0:
        print("node is", node)

g2 = networkx.dfs_tree(g, 'Occupation')
print("nodes = %d", g2.number_of_nodes())
print("edges = %d", g2.number_of_edges())

# This reveals that the problem is caused by duplication of names in the tree
# Answer question why is it not a tree?

edge_set_1 = g.edges
edge_set_2 = g2.edges
print(edge_set_1 - edge_set_2)


#json_data = networkx.readwrite.json_graph.tree_data(g2, 'Occupation')




