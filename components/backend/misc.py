import neo4j
import neo4j.v1
import matplotlib
import networkx
import matplotlib
import matplotlib.pyplot

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7688"
driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

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
