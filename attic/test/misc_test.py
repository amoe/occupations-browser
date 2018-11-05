import pytest
import unittest.mock
import os
from logging import debug
import yaml
import subprocess

class MyNeo4j(object):
    def query(self, string):
        return "hello"

thing = MyNeo4j()
thing.query = unittest.mock.MagicMock(return_value="goodbye")

def get_repo_toplevel():
    output = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])
    return output.rstrip().decode('utf-8')

@pytest.mark.unit
def test_query():
    result = thing.query("MATCH (n) RETURN n")
    assert result == 'goodbye'   

def test_can_get_environment():
    debug("environment is %s", os.environ['OCCUBROW_ENVIRONMENT'])
    env = os.environ['OCCUBROW_ENVIRONMENT']
    config_path = os.path.join(get_repo_toplevel(), 'environments', "%s.yml" % env)

    with open(config_path, 'r') as f:
        data = yaml.load(f, Loader=yaml.Loader)

    debug("data is %s", data)

