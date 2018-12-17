from occubrow.backend import OccubrowBackend
from occubrow.constants import MOCKED_UUID

def test_create_compound():
    repository = None
    backend = OccubrowBackend(repository)
    compound_id = backend.create_compound(['Dog', 'and', 'Duck'])
    assert compound_id == MOCKED_UUID
