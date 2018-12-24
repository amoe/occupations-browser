import occubrow.system
import sys
import pprint
import pdb

backend = occubrow.system.get_backend()


sentences = [
    'keep a bar',
    'keep a shop',
    'keep the peace',
    'keep the books'
]

backend.clear_all_data()

for sentence in sentences:
    backend.add_sentence(sentence)

result = backend.get_tree()
pprint.pprint(result)
