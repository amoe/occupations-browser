# Don't want this to be in the occubrow source tree directly but this is the easiest place to put it
# XXX: We should probably use builder pattern here
import occubrow.backend
from occubrow.identifier_functions import random_uuid

# repository might be mocked, but the identifiers are generated as in production
# (randomly)
def make_backend(repository):
    """
    Construct a backend configured for the default non-isolated behaviour, with
    the exception of the repository which may be passed in.  This can be used
    by both unit and functional tests.
    """
    return occubrow.backend.OccubrowBackend(repository, identifier_function=random_uuid)


