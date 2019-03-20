import pytest
import occubrow.system
import unittest.mock

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

def test_foo():
    b = occubrow.system.get_backend()
    mock = unittest.mock.Mock()
    assert True
