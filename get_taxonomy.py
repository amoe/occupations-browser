import occubrow.system
import pprint

b = occubrow.system.get_backend()
result = b.export_taxonomy_tree('Occupation')

pprint.pprint(result)
