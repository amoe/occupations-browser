from occubrow.backend import OccubrowBackend
from occubrow.constants import MOCKED_UUID
from occubrow.identifier_functions import random_uuid

def test_create_compound():
    repository = None
    backend = OccubrowBackend(repository, identifier_function=lambda: MOCKED_UUID)
    compound_id = backend.create_compound(['Dog', 'and', 'Duck'])
    assert compound_id == MOCKED_UUID
