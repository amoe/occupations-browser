import neo4j
import occubrow.neo4j_repository
import occubrow.backend
import occubrow.identifier_functions
import occubrow.gateway.micromacro

def get_repository():
    bolt_uri = "bolt://localhost:7688"
    driver = neo4j.GraphDatabase.driver(bolt_uri)
    repository = occubrow.neo4j_repository.RealNeo4jRepository(driver)
    return repository

def get_identifier_function():
    return occubrow.identifier_functions.random_uuid

def get_micromacro_gateway():
    return occubrow.gateway.micromacro.MicromacroGateway()

def get_backend(overrides={}):
    """
    Construct a backend with optional overriding of certain dependencies to
    enable mocking, etc.  Non overridden parts of the system will be replaced by
    their production systems.  Overridden parts will be used as is; if overridden,
    production components for that dependency won't be initialized at all.
    """
    dependency_initializers = {
        'repository': get_repository,
        'identifier_function': get_identifier_function,
        'micromacro_gateway': get_micromacro_gateway
    }

    actual_dependencies = overrides.copy()
    
    for k, v in dependency_initializers.items():
        if k not in actual_dependencies:
            actual_dependencies[k] = v()
    
    return occubrow.backend.OccubrowBackend(**actual_dependencies)
