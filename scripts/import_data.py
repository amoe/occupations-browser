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

for path in sys.argv[1:]:
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tokens = nltk.word_tokenize(row['occupation_status'])
            print(tokens)


