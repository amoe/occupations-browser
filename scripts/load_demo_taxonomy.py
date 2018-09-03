import occubrow.neo4j_repository

n4j = occubrow.neo4j_repository.Neo4jRepository(port=7688)
n4j.add_taxonomy()
