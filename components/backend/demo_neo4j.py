#! /usr/bin/env python3

import neo4j
import neo4j.v1

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7687"

driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

READ_ENTIRE_GRAPH_QUERY = """
    MATCH (n) OPTIONAL MATCH (n)-[r]->() RETURN n, r
"""

node_index = {}


roots = [
]

roots_index = {
    
}


with driver.session() as session:
    with session.begin_transaction() as tx:
        results = tx.run(READ_ENTIRE_GRAPH_QUERY)
        for record in results:
            node['content'] = record['n']


# assert that 'ironmonger' is a root
# assert that 'hold' is a root
# assert that 'keep' is a root

# given the data set provided by the shuffled set, which is as such

["keep" "the" "Bell" "at" "Uxbridge"]
["keep" "the" "Half-moon"]
["hold" "a" "situation" "under" "the" "Honourable" "East" "India" "Company"]
["ironmonger" "and" "founder"]





# MATCH a WHERE NOT (a)-[:LOVES]->()


# MATCH (n) WHERE NOT (n)<-[:PRECEDES]-() RETURN n;            



