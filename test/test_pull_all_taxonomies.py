import pytest
import unittest.mock
import occubrow.queries
from occubrow.neo4j_repository import RealNeo4jRepository

# Here we are just checking that the correct query is used.
def test_submits_correct_query():
   mock_driver = unittest.mock.Mock()
   mock_session = unittest.mock.MagicMock()
   mock_driver.session.return_value = mock_session
   mock_session.__enter__ = lambda self: self
   repository = RealNeo4jRepository(mock_driver)
   result = repository.get_all_taxonomies()
   expected_query = occubrow.queries.SLURP_TAXONOMIES
   mock_session.run.assert_called_once_with(expected_query)
