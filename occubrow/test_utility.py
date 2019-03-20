# Don't want this to be in the occubrow source tree directly but this is the easiest place to put it
# XXX: We should probably use builder pattern here
import collections
import networkx
import occubrow.backend
from occubrow.identifier_functions import random_uuid
from occubrow.backend import strict_eq
import occubrow.gateway.micromacro

def tree_matches(t1, t2):
    g1 = networkx.tree_graph(t1)
    g2 = networkx.tree_graph(t2)
    return strict_eq(g1, g2)

# repository might be mocked, but the identifiers are generated as in production
# (randomly)
def make_backend(repository):
    """
    Construct a backend configured for the default non-isolated behaviour, with
    the exception of the repository which may be passed in.  This can be used
    by both unit and functional tests.
    """
    return occubrow.backend.OccubrowBackend(
        repository, identifier_function=random_uuid,
        micromacro_gateway=occubrow.gateway.micromacro.MicromacroGateway()
    )


# Mocking out a crazy API from N-P-D whereby we have to satisfy the chained call:
#    result.summary().counters.nodes_created
# Once we have a better idea of what we need, it might be good to write a facade
# instead of this kludge

class MockStatementResultSummary(object):
    def __init__(self, counters):
        self.counters = counters

class MockSummaryCounters(object):
    def __init__(self, nodes_created, relationships_created):
        self.nodes_created = nodes_created
        self.relationships_created = relationships_created

class MockResult(object):
    def __init__(self, config):
        self.config = config
        
    def summary(self):
        return MockStatementResultSummary(
            MockSummaryCounters(self.config['nodes_created'], self.config['relationships_created'])
        )

# Top level function for use in tests
def ncreated(n):
    return MockResult({
        'nodes_created': n, 'relationships_created': 0
    })

def rcreated(n):
    return MockResult({
        'nodes_created': 0, 'relationships_created': n
    })
