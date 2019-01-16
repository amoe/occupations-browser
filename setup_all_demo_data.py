import create_sample_taxonomy_graphs
import pprint
from occubrow.taxonomy.taxonomy_inserter import TaxonomyInserter
from occubrow.taxonomy.uri_generator import TaxonomySurrogateURIAssigner
import neo4j
from occubrow.corpus.import_sample_sentences import import_annotation_file
from occubrow.neo4j_schema_utilities \
  import reset_schema, create_constraints, create_indexes

driver = neo4j.GraphDatabase.driver("bolt://localhost:7688", auth=('neo4j', 'password'))

reset_schema(driver)
create_constraints(driver)
create_indexes(driver)

obj = TaxonomyInserter(driver)

taxonomy_graphs = {
    'occupation': create_sample_taxonomy_graphs.get_sample_occupation_graph(),
    'place': create_sample_taxonomy_graphs.get_sample_place_graph(),
    'object': create_sample_taxonomy_graphs.get_sample_object_graph()
}

print("Clearing existing database")

# clear database
with driver.session() as s:
    s.run("MATCH (n) DETACH DELETE n")

print("Importing taxonomy graphs")

surrogate = TaxonomySurrogateURIAssigner('2019-01-16')

# import all of the taxonomies
for key, g in taxonomy_graphs.items():
    g2 = surrogate.assign_to_entire_graph(g)
    obj.load_taxonomy(g2, key)

print("Importing annotated text")

# import the sample annotated tokens
import_annotation_file("sample_sentences.xml")
