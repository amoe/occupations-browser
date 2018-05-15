# Old school

READ_ENTIRE_GRAPH_QUERY = """
    MATCH (n) OPTIONAL MATCH (n)-[r]->() RETURN n, r
"""

