#! /usr/bin/python3 

import misc
import networkx
import pprint
import logging

log = logging.getLogger('occubrow')

DECLARE_GROUP_QUERY = """
    MATCH (s:Token {content: {synonym}}), (m:Token {content: {master}})
    CREATE (s)-[:SYNONYMOUS]->(m)
"""


GET_ALL_ROOTS_QUERY = """
    MATCH (t1:Token)<-[r:CONTAINS]-(s1:Sentence)
    WHERE r.index = 0
    RETURN DISTINCT t1 AS root
"""

def declare_group(synonym, master):
    results = misc.run_some_query(DECLARE_GROUP_QUERY, {'synonym': synonym, 'master': master})
    print(results)
    

def result_to_token(record):
    return record['t'].get('content')

def add_linear_nodes(g, token_seq):
    for index, token in enumerate(token_seq):
        g.add_node(token)

        if index != 0:
            start_node = token_seq[index - 1]
            g.add_edge(start_node, token)

def gather_token_seq(result_seq):
    ret = []
    
    for node in result_seq:
        ret.append(node.get('content'))

    return ret
