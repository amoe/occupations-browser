import create_sample_taxonomy_graphs
import pprint
from taxonomy_inserter import TaxonomyInserter
from create_surrogate_uris_for_taxonomy import TaxonomySurrogateURIAssigner
import neo4j
from import_sample_sentences import import_annotation_file

driver = neo4j.GraphDatabase.driver("bolt://localhost:7688", auth=('neo4j', 'password'))
obj = TaxonomyInserter(driver)

taxonomy_graphs = [
    create_sample_taxonomy_graphs.get_sample_occupation_graph(),
    create_sample_taxonomy_graphs.get_sample_place_graph(),
    create_sample_taxonomy_graphs.get_sample_object_graph()
]


print("Clearing existing database")

# clear database
with driver.session() as s:
    s.run("MATCH (n) DETACH DELETE n")

print("Importing taxonomy graphs")

surrogate = TaxonomySurrogateURIAssigner()

# import all of the taxonomies
for g in taxonomy_graphs:
    g2 = surrogate.assign(g)
    obj.load_taxonomy(g2)

print("Importing annotated text")

# import the sample annotated tokens
import_annotation_file("sample_sentences.xml")
