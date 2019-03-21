import pytest
import occubrow.mmconverter.process
import pprint

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

EXPECTED_RESULT = {'children': [{'content': 'Broad', 'id': 'Broad'}],
                   'content': 'Mary',
                   'id': 'Mary'}


def test_tree_is_constructed():
     converter = occubrow.mmconverter.process.MicromacroConverter()
     tree = converter.get_tree(MOCKED_RESULT)
     assert tree == EXPECTED_RESULT
     
    
