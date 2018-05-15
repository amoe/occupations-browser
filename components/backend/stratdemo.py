#! /usr/bin/env python3

import nltk
import csv
import sys
import networkx
import matplotlib
import matplotlib.pyplot

token_seq_1 = ["the", "quick", "brown", "fox"]
token_seq_2 = ["the", "quick", "brown", "bear"]

graph = networkx.MultiDiGraph()

def quickplot(g):
    matplotlib.pyplot.clf()
    networkx.draw_networkx(g)
    matplotlib.pyplot.show()

def add_linear_nodes(g, token_seq):
    for index, token in enumerate(token_seq):
        g.add_node(token)

        if index != 0:
            start_node = token_seq[index - 1]
            g.add_edge(start_node, token)

def get_graph(path):
    graph = networkx.MultiDiGraph()

    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tokens = nltk.word_tokenize(row['occupation_status'])
            add_linear_nodes(graph, tokens)

    return graph

if __name__ == "__main__":
    g = get_graph(sys.argv[1])
    networkx.write_gexf(g, "out.gexf")
