import create_sample_taxonomy_graphs
import pprint
from taxonomy_inserter import TaxonomyInserter
import neo4j

driver = neo4j.GraphDatabase.driver("bolt://localhost:7688", auth=('neo4j', 'password'))
obj = TaxonomyInserter(driver)

taxonomy_graphs = [
    create_sample_taxonomy_graphs.get_sample_occupation_graph(),
    create_sample_taxonomy_graphs.get_sample_place_graph(),
    create_sample_taxonomy_graphs.get_sample_object_graph()
]


# clear database
with driver.session() as s:
    s.run("MATCH (n) DETACH DELETE n")

for g in taxonomy_graphs: obj.load_taxonomy(g)

