import pytest
import occubrow.system
import unittest.mock
import occubrow.test_utility
from occubrow.neo4j_repository import RealNeo4jRepository

DEMO_QUERY = {
    "table": "ob-all5",
    "filter": "a&b",
    "limit": 100,
    "orderBy": {
        "context": "",
        "clauses": []
    },
    "literals": {
        "a": {
            "type": "present",
            "args": "true",
            "key": {
                "name": "persName",
                "type": {
                    "nullable": False,
                    "type": "class",
                    "typeParameters": [
                        {
                            "nullable": False,
                            "type": "class",
                            "typeParameters": [],
                            "class": "java.lang.String"
                        },
                        {
                            "nullable": False,
                            "type": "class",
                            "typeParameters": [],
                            "class": "java.lang.String"
                        }
                    ],
                    "class": "uk.ac.susx.tag.method51.core.meta.span.Spans"
                }
            }
        },
        "b": {
            "type": "regex",
            "args": "death",
            "key": {
                "name": "text",
                "type": {
                    "nullable": False,
                    "type": "class",
                    "typeParameters": [],
                    "class": "java.lang.String"
                }
            }
        }
    },
    "_TYPE": "select",
    "isCached": False
}

def test_foo(neo4j_driver):
    repository = RealNeo4jRepository(neo4j_driver)
    b = occubrow.test_utility.make_backend(repository)
    mock = unittest.mock.Mock()
    assert True
