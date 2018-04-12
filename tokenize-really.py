#! /usr/bin/env python3

import nltk
import sys
import json

all_input = sys.stdin.read()
tokens = nltk.word_tokenize(all_input)
json.dump(tokens, sys.stdout)
print()

