#! /usr/bin/python3

import csv
import sys
import neo4j
import neo4j.v1
import nltk

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7687"

driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

def run_some_query(query, parameters):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            results = tx.run(query, parameters)
            return results

CREATE_PARENT_SENTENCE = """
    CREATE
      (s1:Sentence {tokens: {token_list}})
"""

MERGE_TOKEN_NODE = """
    MERGE (n:Token {content: {content}})
    RETURN n
"""

CREATE_CONTAINS_RELATIONSHIP = """
    MATCH (n:Token {content: {content}}), (s1:Sentence {tokens: {token_list}})   
    CREATE (s1)-[:CONTAINS {index: {index}}]->(n)
"""


for path in sys.argv[1:]:
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tokens = nltk.word_tokenize(row['occupation_status'])
            result = run_some_query(CREATE_PARENT_SENTENCE, {'token_list': tokens})

            for index, token in enumerate(tokens):
                run_some_query(MERGE_TOKEN_NODE, {'content': token})
                run_some_query(
                    CREATE_CONTAINS_RELATIONSHIP,
                    {'content': token, 'index': index, 'token_list': tokens}
                )
                
