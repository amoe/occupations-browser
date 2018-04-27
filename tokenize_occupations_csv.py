#! /usr/bin/env python3

import csv
import sys
import nltk
import json

class OccupationsCsvTokenizer(object):
    def run(self, args):
        input_path = args[0]

        structure = []

        with open(input_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tokens = nltk.word_tokenize(row['occupation_status'])
                datum = {
                    'original': row['occupation_status'],
                    'tokenized': tokens,
                    'count': row['count']
                }
                structure.append(datum)
                
        json.dump(structure, sys.stdout)
            

if __name__ == "__main__":
    obj = OccupationsCsvTokenizer()
    obj.run(sys.argv[1:])
