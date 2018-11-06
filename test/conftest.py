import pytest

@pytest.fixture
def meaning_of_life():
    print("Calculating")
    yield 42
    print("Calculated")
