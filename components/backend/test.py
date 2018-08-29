import unittest.mock
import os
from logging import debug

class MyNeo4j(object):
    def query(self, string):
        return "hello"

thing = MyNeo4j()
thing.query = unittest.mock.MagicMock(return_value="goodbye")

def test_query():
    result = thing.query("MATCH (n) RETURN n")
    assert result == 'goodbye'   

def test_can_get_environment():
    debug("environment is %s", os.environ['OCCUBROW_ENVIRONMENT'])
