import pytest
import occubrow.system
import unittest.mock
import occubrow.test_utility
import pprint
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

@pytest.mark.functional
def test_returns_results(neo4j_driver):
    repository = RealNeo4jRepository(neo4j_driver)
    b = occubrow.test_utility.make_backend(repository)
    result = b.query_micromacro(DEMO_QUERY)
    pprint.pprint(result)
    assert result
