import networkx
import openpyxl
import sys
from logging import debug, info, warn
import pprint
from occubrow.utility import dfs_tree_with_node_attributes
import pdb

# this is for dealing with the file 'media_405073_en.xlsx'

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
    raw = [rec[k] for k in wanted_keys]
    while raw[-1] is None:
        del raw[-1]

    return raw

def get_concat_id(seq, index):
    return ''.join(filter(None, seq[:index + 1]))

class SamuelsLoader(object):
    def load(self, path):
        wb = openpyxl.load_workbook(sys.argv[1])
        sheet = wb.active
        g = networkx.DiGraph()

        for row in sheet.iter_rows(min_row=2):
            cell_values = [c.value for c in row]
            rec = form_record(cell_values)

            if not rec['t1']:
                warn("Strange record encountered, skipping: %s", rec)
                continue

            category_sequence = record_to_category_sequence(rec)

            this_category_node_id = get_concat_id(category_sequence, len(category_sequence))

            g.add_node(this_category_node_id, content=rec['samuels_heading'])

            for i in range(len(category_sequence)):
                source = get_concat_id(category_sequence, i)
                
                # Skip to the next parent if it doesn't exist as a concrete row
                # This can happen and it's not an error
                if source not in g:
                    continue
                
                for j in range(i + 1, len(category_sequence)):
                    possible_target = get_concat_id(category_sequence, j)

                    if possible_target in g:
                        g.add_edge(source, possible_target)
                        break
                
        sources = [v for v, indegree in g.in_degree() if indegree == 0]
        print("Possible roots:", sources)

        # artificially reparent to form a rooted tree
        g.add_node('00', content='Theme')
        for source in sources:
            g.add_edge('00', source)

        tree = dfs_tree_with_node_attributes(g, '00')
        return tree

if __name__ == '__main__':
    obj = SamuelsLoader()
    print("Tree is", networkx.tree_data(obj.load(sys.argv[1]), '00'))
