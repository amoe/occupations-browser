import neo4j
import neo4j.v1
import matplotlib
import networkx
import matplotlib
import matplotlib.pyplot


def quickplot(g):
    matplotlib.pyplot.clf()
    networkx.draw_networkx(g)
    matplotlib.pyplot.show()

def run_some_query(query, parameters):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            results = tx.run(query, parameters)
            return results

def close_connection():
    driver.close()
