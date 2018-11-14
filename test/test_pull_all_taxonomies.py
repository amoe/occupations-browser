import pytest
import unittest.mock

def driveruser(driver):
    with driver.session() as session:
        r = session.run("FOO BAR")
        return r

def test_pull_all_taxonomies():
   mock_driver = unittest.mock.Mock()
   mock_session = unittest.mock.MagicMock()
   mock_driver.session.return_value = mock_session
   mock_session.__enter__ = lambda self: self
   mock_session.run.return_value = 42

   r = driveruser(mock_driver)
   assert r == 42
