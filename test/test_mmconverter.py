import pytest
import pprint
import unittest.mock
import occubrow.mmconverter.process
import occubrow.system
from  occubrow.utility import find_root_by_content
from occubrow.test_utility import tree_matches

MOCKED_QUERY_RESULT = [
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

EXPECTED_RESULT = {'children': [{'content': 'Broad', 'id': 2, 'strength': 1}],
                   'content': 'Mary',
                   'id': 1,
                   'strength': 1}

def test_graph_is_retrieved():
     mock = unittest.mock.Mock()
     mock.query.return_value = MOCKED_QUERY_RESULT
     backend = occubrow.system.get_backend({
          'micromacro_gateway': mock,
          'repository': unittest.mock.Mock()
     })
     graph = backend.query_micromacro({})
     assert graph.number_of_nodes() == 2

def test_tree_is_retrieved():
     mock = unittest.mock.Mock()
     mock.query.return_value = MOCKED_QUERY_RESULT
     backend = occubrow.system.get_backend(
          {'micromacro_gateway': mock, 
          'repository': unittest.mock.Mock()}
     )
     graph = backend.query_micromacro({})
     tree = backend.massage_for_depth(graph, find_root_by_content(graph, 'Mary'), 2, 0)
     assert tree_matches(tree, EXPECTED_RESULT)
    
