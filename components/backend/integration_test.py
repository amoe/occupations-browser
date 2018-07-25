import pytest
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)8s - %(name)s - %(message)s"
)


@pytest.fixture(scope='function')
def load_demo_taxonomy():
    logging.debug("hi there")
    yield None
    print("unloading demo taxonomy")

def test_integration(load_demo_taxonomy):
    assert 2 + 2 == 4
