import unittest.mock
import neo4j
import pprint
import json

# this is going to return domain specific stuff

class Neo4jService(object):
    def run_query(self, query, parameters):
        credentials = ('neo4j', 'password')
        uri = "bolt://localhost:7687"
        driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

        with driver.session() as session:
            with session.begin_transaction() as tx:
                results = tx.run(query, parameters)
                return results


# totree demo, we need the WHERE clause otherwise it's going to fuck us
RETURN_TAXONOMY_TREE = """
    MATCH p = (t1:Taxon)-[r:SUPERCATEGORY_OF*]->(t2:Taxon)
    WHERE NOT (t2)-[:SUPERCATEGORY_OF]->(t1) AND t1.name = 'Ulmaridae'
    WITH COLLECT(p) AS ps
    CALL apoc.convert.toTree(ps) YIELD value RETURN value;
"""

STUB_DATA = [
    {'_id': 19975,
     '_type': 'Taxon',
     'name': 'Ulmaridae',
     'supercategory_of': [{'_id': 19976,
                           '_type': 'Taxon',
                           'name': 'Deepstaria',
                           'supercategory_of': [{'_id': 19978,
                                                 '_type': 'Taxon',
                                                 'name': 'Deepstaria enigmatica'},
                                                {'_id': 19979,
                                                 '_type': 'Taxon',
                                                 'name': 'Deepstaria reticulum'}]},
                          {'_id': 19977,
                           '_type': 'Taxon',
                           'name': 'Aurelia',
                           'supercategory_of': [{'_id': 19980,
                                                 '_type': 'Taxon',
                                                 'name': 'Aurelia aurita'},
                                                {'_id': 19981,
                                                 '_type': 'Taxon',
                                                 'name': 'Aurelia labiata'}]}]}
]

db = Neo4jService()
db.run_query = unittest.mock.MagicMock(return_value=STUB_DATA)

def get_taxonomy_as_json(neo4j_service):
    result = neo4j_service.run_query(RETURN_TAXONOMY_TREE, {})
    return json.dumps(result)

def test_taxonomy_endpoint():
    result = get_taxonomy_as_json(db)
    print(result)
    assert result

    


