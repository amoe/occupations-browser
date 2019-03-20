import pprint
import requests

endpoint = 'http://localhost:8090/api/query/select'
postdata = {
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

headers = {
}

r = requests.post(endpoint, json=postdata, headers=headers)
content = r.json()
pprint.pprint(content)
