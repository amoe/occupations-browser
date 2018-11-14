import networkx
import openpyxl
import sys

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
        'concat': row[9]
    }

for row in sheet:
    cell_values = [c.value for c in row]
    rec = form_record(cell_values)
    print(rec)
    
