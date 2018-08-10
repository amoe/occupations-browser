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

PULL_ALL_TOKEN_SEQUENCES = """
    MATCH (s1:Sentence)-[r:CONTAINS]->(t)
    WITH s1, t
    ORDER BY r.index
    RETURN s1, COLLECT(t) AS seq;
"""

GET_ALL_ROOTS_QUERY = """
    MATCH (t1:Token)<-[r:CONTAINS]-(s1:Sentence)
    WHERE r.index = 0
    RETURN DISTINCT t1 AS root
"""

GET_ROOTS_WITH_SUBSTRING_MATCH = """
    MATCH (t1:Token)<-[r:CONTAINS]-(s1:Sentence)
    WHERE r.index = 0 AND t1.content CONTAINS {substring}
    RETURN DISTINCT t1 AS root
"""   

def declare_group(synonym, master):
    results = misc.run_some_query(DECLARE_GROUP_QUERY, {'synonym': synonym, 'master': master})
    print(results)
    

def result_to_token(record):
    return record['t'].properties['content']

def add_linear_nodes(g, token_seq):
    for index, token in enumerate(token_seq):
        g.add_node(token)

        if index != 0:
            start_node = token_seq[index - 1]
            g.add_edge(start_node, token)

def gather_token_seq(result_seq):
    ret = []
    
    for node in result_seq:
        log.info(pprint.pformat(node))
        ret.append(node.properties['content'])

    return ret

# This is going to pull in the entire graph
# Because we are using DiGraph and not MultiDiGraph it's going to automatically
# remove duplicate edges for us.
def pull_graph():
    graph = networkx.DiGraph()
    results = misc.run_some_query(PULL_ALL_TOKEN_SEQUENCES, {})

    for result in results:
        token_seq = gather_token_seq(result['seq'])
        add_linear_nodes(graph, token_seq)

    return graph

# This is the endpoint that's currently used
def get_tree_by_root(root, depth_limit):
    g = pull_graph()
    tree = networkx.dfs_tree(g, root, depth_limit=depth_limit)
    return networkx.tree_data(tree, root)

def get_roots_with_substring_match(substring):
    return [
        record['root'].properties['content']
        for record in misc.run_some_query(GET_ROOTS_WITH_SUBSTRING_MATCH, {'substring': substring})
    ]
    
