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

level_indices = []

current_index = 0
should_continue = True

myheap = []

while should_continue:
    should_continue = False

    for row in sheet:
        row_reference = row[0].row
        print(row_reference)

        row_values = list([cell.value for cell in row])
        useful_info = get_useful_cell_info(row_values)

        if useful_info['count'] == 0:
            raise Exception("found blank row, please check file" + row)

        first_index = useful_info['first_index']

        if useful_info['first_index'] > current_index:
            should_continue = True
        else:
            # Handle this level
            g.add_node(row_values[first_index])

    current_index += 1


# quickplot(g)
