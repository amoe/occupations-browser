import networkx
import matplotlib
import matplotlib.pyplot

def quickplot(g):
    matplotlib.pyplot.clf()
    networkx.draw_networkx(g)
    matplotlib.pyplot.show()
