CREATE_TOKEN_QUERY = """
    MERGE (t:Token {content: $token})
"""

CREATE_SENTENCE_QUERY = """
    CREATE (s:Sentence {content: $sentence, uuid: $uuid})
"""

CREATE_CONTAINS_RELATIONSHIP = """
    MATCH (t:Token {content: $token}), (s:Sentence {uuid: $sentence_id})
    CREATE (s)-[:CONTAINS $relationship_properties]->(t)
"""

SLURP_TAXONOMIES = """
    MATCH (t1:Taxon)-[r]->(t2:Taxon)
    WITH COLLECT(r) AS rels
    MATCH (t:Taxon)
    RETURN rels, COLLECT(t) AS nodes
"""
