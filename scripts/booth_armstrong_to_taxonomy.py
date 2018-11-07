import networkx
import openpyxl
import sys

# Booth-Armstrong file involves an excel sheet

wb = openpyxl.load_workbook(sys.argv[1])
sheet = wb.active

g = networkx.DiGraph()

def get_useful_cell_count(row_values):
    return sum(x is not None for x in row_values)

def handle_row(row):
    row_values = list([cell.value for cell in row])
    n_useful = get_useful_cell_count(row_values)
    print(row_values)
    if n_useful == 0:
        raise Exception("row " + row)

for row in sheet:
    handle_row(row)
