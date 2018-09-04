import sys
import neo4j.v1
import neo4j.v1.types
import neo4j.v1.types.graph
import json

QUERY_NODES_WITH_TAXA = """
    MATCH (se:Sentence {source: 1})-[r:CONTAINS]->(to:Token)-[:MEMBER_OF]->(ta:Taxon)
    RETURN to, ta
    ORDER BY r.index
"""

uri = "bolt://localhost:7688"
driver = neo4j.v1.GraphDatabase.driver(uri)

with driver.session() as session:
    with session.begin_transaction() as tx:
        results = tx.run(QUERY_NODES_WITH_TAXA, {})
            
# print(neo4j.v1.types.graph.Node(graph=None, n_id=None))
