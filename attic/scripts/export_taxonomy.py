import neo4j.v1

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7688"

driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

    MATCH p = (:Token {content: "the"})-[:PRECEDES*]->(end:Token) 
    WHERE NOT (end)-[:PRECEDES]->()
    CALL apoc.convert.toTree([p]) YIELD value


foo = """
    MATCH p = (ta1:Taxon)-[:SUPERCATEGORY_OF*]->(ta2:Taxon)
    WHERE NOT (ta2)-[:SUPERCATEGORY_OF]->()
    CALL apoc.convert.toTree([p]) YIELD value
    RETURN value;
"""


