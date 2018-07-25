import pytest
import logging
import demo_taxonomy
import misc

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)8s - %(name)s - %(message)s"
)

@pytest.fixture(scope='function')
def load_demo_taxonomy():
    logging.debug("hi there")
    yield None
    print("unloading demo taxonomy")
    misc.close_connection()

def test_integration(load_demo_taxonomy):
    assert 2 + 2 == 4
