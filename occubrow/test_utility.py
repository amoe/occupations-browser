# Don't want this to be in the occubrow source tree directly but this is the easiest place to put it
# XXX: We should probably use builder pattern here
import occubrow.backend
from occubrow.identifier_functions import random_uuid
import networkx
from occubrow.backend import strict_eq

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
    return occubrow.backend.OccubrowBackend(repository, identifier_function=random_uuid)


