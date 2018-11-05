import neo4j
from logging import warn

REQUIRED_NEO4J_VERSION = "1.7.1"

def ensure_versions():
    if neo4j.__version__ != REQUIRED_NEO4J_VERSION:
        warn("Neo4j Python driver version does not match")


if __name__ == '__main__':
    ensure_versions()
    
