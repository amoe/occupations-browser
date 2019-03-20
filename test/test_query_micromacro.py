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

MOCKED_RESULT = [
    {
        "id": "17410828.xml",
        "123": 213.0,
        "text": " Mary  Broad  . On thursday last I was going to counsel for advice, and going through Bartholamew Fair I met the Prosecutrix. She told me she believed her child got a hurt on some timber in the new buildings; that she was very willing not to hurt the Prisoner, and that it was that curst stuff they gave the child at the workhouse was the occasion of its death. ",
        "persName": {
            "spans": [
                {
                    "to": 13.0,
                    "from": 0.0,
                    "with": "",
                    "target": "text",
                    "withType": "java.lang.String"
                }
            ],
            "target": "text"
        },
        "new/field": "BLAHBLAHBLH",
        "new/field2": "BLAHBLAHBLAH",
        "text-token": {
            "spans": [
                {
                    "to": 5.0,
                    "from": 1.0,
                    "with": "Mary",
                    "target": "text",
                    "withType": "java.lang.String"
                },
                {
                    "to": 12.0,
                    "from": 7.0,
                    "with": "Broad",
                    "target": "text",
                    "withType": "java.lang.String"
                }
            ],
            "target": "text"
        },
        "general/date": [
            1741.0,
            5.0,
            1.0
        ],
        "statement-id": "t17410828-63-11",
        "lookup/ob-date": False,
        "trialAccount-id": "t17410828-63",
        "general/postgresId": 15038.0,
        "general/session-date": [
            1741.0,
            8.0,
            28.0
        ],
        "general/trialAccount-id": "t17410828-63"
    }
]


def test_postprocesses_results():
    mock = unittest.mock.Mock()
    mock.query.return_value = MOCKED_RESULT

    b = occubrow.system.get_backend({
        'micromacro_gateway': mock
    })

    result = b.query_micromacro(DEMO_QUERY)
    assert result == MOCKED_RESULT

@pytest.mark.skip("""
We can't really test this at the moment, because it needs the infrastructure
of an entire micromacro server.
""")
@pytest.mark.functional
def test_returns_results(neo4j_driver):
    repository = RealNeo4jRepository(neo4j_driver)
    b = occubrow.test_utility.make_backend(repository)
    result = b.query_micromacro(DEMO_QUERY)
    pprint.pprint(result)
    assert result
