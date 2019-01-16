import openpyxl
import sys
import occubrow.system
import nltk
from fuzzywuzzy import process

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
    def __init__(self, backend):
        self.backend = backend

    def run(self, path):
        wb = openpyxl.load_workbook(path)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2):
            record = cell_to_record(row)
            tokens = nltk.word_tokenize(record['sentence'])
            sentence_id = self.backend.add_sentence_with_tokens(tokens)

            for k, v in record['assignments'].items():
                if v is not None:
                    found = self.backend.get_taxon_by_content(v, k)

                    if found is not None:
                        to_tag, ratio = process.extractOne(v, tokens)
                        self.backend.annotate(sentence_id, to_tag, found)
                    

if __name__ == '__main__':
    obj = TaxonomyAssignmentReader(occubrow.system.get_backend())
    obj.run(sys.argv[1])
