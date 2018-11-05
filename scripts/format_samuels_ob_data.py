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

combined_csv_path = sys.argv[1]
df = pandas.read_csv(combined_csv_path)

result = df.groupby('chunk')

for name, group in result:
    if name == 1000:
        print("Found chunk 1000")
        # Get back to the relatively pristine phrase with this.
        print(group['vard'].str.cat(sep=' '))
        # From here we know the overall phrase (sentence)
        # and we also know the taxonomical class of each token
        # so all that remains is to produce an importable form

        # What importable form can we produce?
        # LOAD CSV format can be used.
        # It would really be worth freezing the documentation for n4j and
        # n4j pytohn driver.
        # We can easily write a testable taxonomy importer.



#"18000528-0074"

