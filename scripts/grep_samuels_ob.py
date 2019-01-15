import pandas
import sys
import csv
import nltk
import re
import pprint

SEPARATOR = ' '

patterns = []

grep_csv_path = sys.argv[1]
with open(grep_csv_path, 'r') as f:
    r = csv.reader(f)
    for row in r:
        tokens = nltk.word_tokenize(row[0])
        pattern = re.compile(
            SEPARATOR.join(
                [re.escape(t) for t in tokens]
            )
        )
        patterns.append(pattern)

patterns_count = [0] * (len(patterns) + 1)

combined_csv_path = sys.argv[2]
df = pandas.read_csv(combined_csv_path)

result = df.groupby('chunk')

for name, group in result:
    sentence = []
    for index, row in group.iterrows():
        vard = row['vard']
        sentence.append(vard)

    sentence_string = SEPARATOR.join(sentence)

    found = False
    for index, p in enumerate(patterns):
        if p.search(sentence_string):
            #print(name)
            patterns_count[index] = patterns_count[index] + 1


for index, p in enumerate(patterns):
    print('%s,%d' % (p, patterns_count[index]))


