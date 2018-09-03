import pytest
import logging
import demo_taxonomy
import misc

BOLT_DRIVER_LOGGER_NAME = 'neo4j.bolt'

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)8s - %(name)s - %(message)s"
)

logging.getLogger(BOLT_DRIVER_LOGGER_NAME).setLevel(logging.WARNING)

@pytest.fixture(scope='function')
def load_demo_taxonomy():
    logging.debug("loading demo taxonomy")
    demo_taxonomy.load_demo_taxonomy()
    yield None
    logging.debug("unloading demo taxonomy")
    misc.close_connection()

def test_integration(load_demo_taxonomy):
    assert 2 + 2 == 4
