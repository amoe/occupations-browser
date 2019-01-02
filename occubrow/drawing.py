import matplotlib
import networkx
import networkx.drawing
import matplotlib
import matplotlib.pyplot

def quickplot(g):
    matplotlib.pyplot.clf()
    layout = networkx.drawing.kamada_kawai_layout(g)
    networkx.draw_networkx(g, pos=layout)
    matplotlib.pyplot.show()
