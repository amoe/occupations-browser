import unittest.mock

class MyNeo4j(object):
    def query(self, string):
        return "hello"

thing = MyNeo4j()
thing.query = unittest.mock.MagicMock(return_value="goodbye")

def test_query():
    result = thing.query("MATCH (n) RETURN n")
    assert result == 'goodbye'   
