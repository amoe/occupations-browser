#! /usr/bin/python3

import itertools
import csv
import sys
import neo4j
import neo4j.v1
import nltk
import argparse
import logging
from logging import debug

parser = argparse.ArgumentParser()

parser.add_argument(
    '--log-level', metavar="LEVEL", type=str, help="Log level",
    default='INFO'
)

# None will be used as a slice argument, meaning no limit
parser.add_argument(
    '--limit', metavar="NUMBER", type=int, default=None,
    help="Limit number of loaded rows from csv file"
)

parser.add_argument('rest_args', metavar="ARGS", nargs='*')
ns = parser.parse_args(sys.argv[1:])
args = ns.rest_args

logging.basicConfig(
    level=getattr(logging, ns.log_level),            
    format="%(asctime)s - %(levelname)8s - %(name)s - %(message)s"
)

credentials = ('neo4j', 'password')
uri = "bolt://localhost:7688"

driver = neo4j.v1.GraphDatabase.driver(uri, auth=credentials)

def run_some_query(query, parameters):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            results = tx.run(query, parameters)
            return results

CREATE_PARENT_SENTENCE = """
    CREATE
      (s1:Sentence {tokens: {token_list}, source: {source}})
"""

MERGE_TOKEN_NODE = """
    MERGE (n:Token {content: {content}})
    RETURN n
"""

CREATE_CONTAINS_RELATIONSHIP = """
    MATCH (n:Token {content: {content}}), (s1:Sentence {tokens: {token_list}})   
    CREATE (s1)-[:CONTAINS {index: {index}}]->(n)
"""


for path in args:
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in itertools.islice(enumerate(reader), 0, ns.limit):
            debug("Loading row %d", index)
            tokens = nltk.word_tokenize(row['occupation_status'])
            result = run_some_query(
                CREATE_PARENT_SENTENCE, {'token_list': tokens, 'source': index}
            )

            for index, token in enumerate(tokens):
                run_some_query(MERGE_TOKEN_NODE, {'content': token})
                run_some_query(
                    CREATE_CONTAINS_RELATIONSHIP,
                    {'content': token, 'index': index, 'token_list': tokens,}
                )
                
