import networkx
import openpyxl
import sys
import matplotlib
import networkx.drawing
import matplotlib.pyplot
import networkx.readwrite.json_graph
import pprint
import heapq


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


pprint.pprint(all_indices)
