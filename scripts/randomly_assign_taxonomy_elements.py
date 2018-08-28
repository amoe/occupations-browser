import csv
import sys
import neo4j
import neo4j.v1
import nltk


credentials = ('neo4j', 'password')
uri = "bolt://localhost:7688"

driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

QUERY_FOR_ALL_NODES = """
   MATCH (to:Token) RETURN to;
"""

RANDOM_TAXON_QUERY = """
   MATCH (ta:Taxon)
   WITH collect(ta.name) AS l
   RETURN apoc.coll.randomItem(l) AS pick
"""

ASSIGN_TO_TAXON = """
    MATCH (to:Token {content: {token_content}}), (ta:Taxon {name: {taxon_name}})
    CREATE (to)-[:MEMBER_OF]->(ta);
"""


class TaxonomyAssigner(object):
    def pick_taxon(self, tx):
        rs2 = tx.run(RANDOM_TAXON_QUERY, {})
        g = rs2.records()
        rec = next(g)
        return rec.value('pick')

    def assign_token_to_taxon(self, tx, token, taxon):
        tx.run(ASSIGN_TO_TAXON, {'token_content': token, 'taxon_name': taxon})
        
    def run(self, tx):
        rs1 = tx.run(QUERY_FOR_ALL_NODES, {})
        for it in rs1:
            taxon = self.pick_taxon(tx)
            print(taxon)


obj = TaxonomyAssigner()
with driver.session() as session:
    with session.begin_transaction() as tx:
        obj.run(tx)

