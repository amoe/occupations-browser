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

def strip_semtag(val):
    v1 = re.sub(r'^[^\[]*\[', '', val)
    v2 = re.sub(r'\]$', '', v1)
    return v2


driver = neo4j.GraphDatabase.driver("bolt://localhost:7688", auth=('neo4j', 'password'))

query = """
    MATCH (ta:Taxon {content: {wanted_content}}) RETURN ta.uri AS uri
"""

combined_csv_path = sys.argv[1]
df = pandas.read_csv(combined_csv_path)

result = df.groupby('chunk')

soup = bs4.BeautifulSoup(features='xml')

root = soup.new_tag("root")
soup.append(root)


class AmbiguousTagException(Exception):
    pass

@functools.lru_cache(maxsize=None)
def lookup_semtag_value_in_neo(semtag):
    stripped = strip_semtag(semtag)
    result = session.run(query, {'wanted_content': stripped})
    uri = result.value('uri')

    if len(uri) == 0:
        return None

    if len(uri) != 1:
        raise AmbiguousTagException(semtag)

    return uri[0]



def handle_token(containing_sentence, row):
    semtag = row['SEMTAG3']
    vard = row['vard']

    if pandas.isna(semtag):
        containing_sentence.append(vard)
    else:
        uri = lookup_semtag_value_in_neo(semtag)

        if uri:
            annotation_tag = soup.new_tag("annotation")
            annotation_tag['ref'] = uri
            annotation_tag.string = vard
            containing_sentence.append(annotation_tag)
        else:
            containing_sentence.append(vard)

    containing_sentence.append(" ")


success = 0
errors = []


with driver.session() as session:
    for name, group in result:
        sentence = soup.new_tag('sentence')

        for index, row in group.iterrows():
            print(index)
            try:
                handle_token(sentence, row)
                success = success + 1
            except AmbiguousTagException as e:
                errors.append(e)

        root.append(sentence)

        # Get back to the relatively pristine phrase with this.
#        print(group['vard'].str.cat(sep=' '))
        # From here we know the overall phrase (sentence)
        # and we also know the taxonomical class of each token
        # so all that remains is to produce an importable form

        # What importable form can we produce?
        # LOAD CSV format can be used.
        # It would really be worth freezing the documentation for n4j and
        # n4j pytohn driver.
        # We can easily write a testable taxonomy importer.



# So the problem with this is that once we have the data we need some way to
# link it into the existing taxonomy.

# So produce an XML-annotated set

#"18000528-0074"

with open('samuels-annotated.xml', 'w') as f:
    f.write(soup.prettify())

print("Successful lookup: ", success)
print("Errors: ", len(errors))
