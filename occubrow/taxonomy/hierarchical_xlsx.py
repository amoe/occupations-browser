import networkx
import openpyxl
import pprint

# Booth-Armstrong file involves an excel sheet

class HierarchicalXlsxTaxonomyLoader(object):
    def __init__(self, path):
        wb = openpyxl.load_workbook(path)
        self.sheet = wb.active

    def get_useful_cell_info(self, row_values):
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


    def find_parent(self, indices, child_row, child_level):
        table = indices[child_level - 1]

        last_item = None

        for item in table:
            if item['row_index'] < child_row:
                last_item = item

        return last_item

    def run(self, reparent_node):
        """
        Taxonomy tree will be reparented under the node given by reparent_node,
        which will normally be a human-readable string.
        """
        g = networkx.DiGraph()
        current_row = 0
        should_continue = True

        all_indices = []

        while should_continue:
            should_continue = False

            level_indices = []
            for row in self.sheet:
                this_row_index = row[0].row
                print(this_row_index)
                row_values = [x.value for x in row]
                info = self.get_useful_cell_info(row_values)
                first_index = info['first_index']

                if first_index is None:
                    continue

                if  first_index > current_row:
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

        for level, table in enumerate(all_indices):
            for item in table:
                g.add_node(item['content'])

                if level > 0:
                    parent = self.find_parent(all_indices, item['row_index'], level)
                    g.add_edge(parent['content'], item['content'])

        g.add_node(reparent_node)

        # now reparent the graph
        for node, in_degree in g.in_degree():
            if in_degree == 0 and node != reparent_node:
                g.add_edge(reparent_node, node)

        return g
