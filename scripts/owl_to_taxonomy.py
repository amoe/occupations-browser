# convert owl to taxonomy

import bs4
import sys
import networkx
import matplotlib
import networkx.drawing
import matplotlib.pyplot
import networkx.readwrite.gexf


def quickplot(g):
    matplotlib.pyplot.clf()
    layout = networkx.drawing.kamada_kawai_layout(g)
    networkx.draw_networkx(g, pos=layout)
    matplotlib.pyplot.show()


input_path = sys.argv[1]

with open(input_path, 'r') as f:
    parser = bs4.BeautifulSoup(f, 'lxml')

classes = parser.find_all('owl:class')

# BeautifulSoup is automatically lowercasing tag names for some reason that I
# can't fathom.



print("Found %d classes" % len(classes))


g = networkx.DiGraph()


for class_ in classes:
    # label_element = class_.find('rdfs:label', {'xml:lang': 'en'})
    # label_text = label_element.text
    # g.add_node(label_text)

    uri = class_['rdf:about']
    print(uri)

    g.add_node(uri)
    
    parent_classes_list = class_.find_all('rdfs:subclassof')

    for parent_class in parent_classes_list:
        parent_uri = parent_class['rdf:resource']
        g.add_edge(parent_uri, uri)


#networkx.readwrite.gexf.write_gexf(g, 'foo.gexf')
