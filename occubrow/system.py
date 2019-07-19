import neo4j
import occubrow.neo4j_repository
import occubrow.backend
import occubrow.identifier_functions

def get_backend():
    bolt_uri = "bolt://localhost:7688"
    credentials = ('neo4j', 'password')
    driver = neo4j.GraphDatabase.driver(bolt_uri, auth=credentials)
    repository = occubrow.neo4j_repository.RealNeo4jRepository(driver)
    identifier_function = occubrow.identifier_functions.random_uuid
    return occubrow.backend.OccubrowBackend(
        repository, identifier_function
    )
