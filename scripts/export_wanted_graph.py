# This is going to export a wanted graph

import pprint
import neo4j
import occubrow.backend
import occubrow.neo4j_repository

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7687"
driver = neo4j.GraphDatabase.driver(uri, auth=credentials)

repo = occubrow.neo4j_repository.RealNeo4jRepository(driver)
backend = occubrow.backend.OccubrowBackend(repo)
pprint.pprint(backend.export_graph())
