import neo4j
import neo4j.v1
import matplotlib
import networkx

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7687"
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
