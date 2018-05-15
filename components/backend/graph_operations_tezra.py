#! /usr/bin/python3 

import misc
import networkx

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

# This is going to pull in the entire graph
# Because we are using DiGraph and not MultiDiGraph it's going to automatically
# remove duplicate edges for us.
def pull_graph():
    graph = networkx.DiGraph()
    results = misc.run_some_query(PULL_ALL_TOKEN_SEQUENCES, {})

    for result in results:
        add_linear_nodes(graph, [node.properties['content'] for node in result['seq']])

    return graph

def getblah():
    g = pull_graph()
    tree = networkx.dfs_tree(g, 'Oyl', depth_limit=2)
    return networkx.tree_data(tree, 'Oyl')
    
