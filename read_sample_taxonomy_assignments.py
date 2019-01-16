import openpyxl
import sys

wb = openpyxl.load_workbook(sys.argv[1])
sheet = wb.active


def cell_to_record(row):
    return {
        'sentence': row[1].value.rstrip(),
        'assignments': [
            {'object': row[5].value,
             'place': row[6].value,
             'activity': row[2].value,
             'status': row[8].value}
        ]
    }

for row in sheet.iter_rows(min_row=2):
    record = cell_to_record(row)
    print(record)

    
