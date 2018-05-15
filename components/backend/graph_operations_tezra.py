#! /usr/bin/python3 

import misc

DECLARE_GROUP_QUERY = """
    MATCH (s:Token {content: {synonym}}), (m:Token {content: {master}})
    CREATE (s)-[:SYNONYMOUS]->(m)
"""

def declare_group(synonym, master):
    results = misc.run_some_query(DECLARE_GROUP_QUERY, {'synonym': synonym, 'master': master})
    print(results)
    
