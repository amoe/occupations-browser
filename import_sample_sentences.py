import occubrow.system
import sys
import pprint
import pdb
import bs4

backend = occubrow.system.get_backend()

sentence_file_path = "sample_sentences.xml"



with open(sentence_file_path, 'r') as f:
    root = bs4.BeautifulSoup(f, 'lxml')

sentences = root.find_all('sentence')

for sentence in sentences:
    for x in sentence:
        # print s.x
        # if isinstance(x, bs4.NavigableString):
        #     handle_string(
        # else:
        #     print("tag: ", x)
