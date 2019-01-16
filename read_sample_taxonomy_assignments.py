import openpyxl
import sys
import occubrow.system

def cell_to_record(row):
    return {
        'sentence': row[1].value.rstrip(),
        'assignments': {
            'object': row[5].value,
            'place': row[6].value,
            'activity': row[2].value,
            'status': row[8].value
        }
    }

class TaxonomyAssignmentReader(object):
    def run(self, path):
        wb = openpyxl.load_workbook(path)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2):
            record = cell_to_record(row)

            for k, v in record['assignments'].items():
                if v is not None:
                    print(k, v)

if __name__ == '__main__':
    obj = TaxonomyAssignmentReader()
    obj.run(sys.argv[1])
