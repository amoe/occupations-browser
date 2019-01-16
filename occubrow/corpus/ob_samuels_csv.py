#! /usr/bin/env python3

# The input for this is CSV files from Julie in the format 

# These are mechanically derived from the output of the Samuels tagger, whose
# input was sharonhoward's OBV corpus.

# The text is segmented into chunks

# We want to get from here to a series of labelled tokens that know how to refer
# back to their source.  The source should be represented as a Context object
# The full source can be depicted as a URL and an xpath?

import pandas
import sys
import bs4
import neo4j
import re
import functools
import random
import occubrow.system

def strip_semtag(val):
    v1 = re.sub(r'^[^\[]*\[', '', val)
    v2 = re.sub(r'\]$', '', v1)
    return v2

backend = occubrow.system.get_backend()

# blah = set([])
# with open('/home/amoe/dev/occubrow/backend/scripts/relevant_groups.lst', 'r') as f2:
#     blah = set([int(x.rstrip()) for x in f2])
#     print(blah)

# def filter_pred(group_index, group):
#     global blah
#     return group_index in blah


@functools.lru_cache(maxsize=None)
def lookup_semtag_value_in_neo(semtag):
    return backend.get_taxon_by_content(semtag, 'theme')

def unfiltered_pred(group_index, group):
    return True

class OBSamuelsCSVLoader(object):
    def __init__(self, sampling_probability):
        self.success = 0
        self.errors = []
        self.sampling_probability = sampling_probability

    def handle_token(self, containing_sentence, row):
        semtag = row['SEMTAG3']
        vard = row['vard']

        if pandas.isna(semtag):
            containing_sentence.append(vard)
        else:
            uri = lookup_semtag_value_in_neo(strip_semtag(semtag))

            if uri:
                annotation_tag = self.soup.new_tag("annotation")
                annotation_tag['ref'] = uri
                annotation_tag.string = vard
                containing_sentence.append(annotation_tag)
            else:
                containing_sentence.append(vard)

        containing_sentence.append(" ")


    def handle_sentence(self, group_index, group, predicate):
        if not predicate(group_index, group):
            return

        sentence = self.soup.new_tag('sentence')

        for index, row in group.iterrows():
            print(index)
            try:
                self.handle_token(sentence, row)
                self.success = self.success + 1
            except occubrow.errors.AmbiguousTaxonException as e:
                self.errors.append(e)

        return sentence

    def run(self, input_path, output_path, predicate=None):
        if predicate is None:
            predicate = unfiltered_pred

        df = pandas.read_csv(input_path)
        result = df.groupby('chunk')
        self.soup = bs4.BeautifulSoup(features='xml')
        root = self.soup.new_tag("root")
        self.soup.append(root)

        for group_index, group in result:
            if random.random() < self.sampling_probability:
                sentence = self.handle_sentence(group_index, group, predicate=unfiltered_pred)
                root.append(sentence)

        with open(output_path, 'w') as f:
            f.write(self.soup.prettify())

        print("Successful lookup: ", self.success)
        print("Errors: ", len(self.errors))

