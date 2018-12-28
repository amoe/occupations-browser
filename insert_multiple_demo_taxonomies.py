import create_sample_taxonomy_graphs
import pprint
from taxonomy_inserter import TaxonomyInserter
import neo4j

driver = neo4j.GraphDatabase.driver("bolt://localhost:7688", auth=('neo4j', 'password'))
g = create_sample_taxonomy_graphs.get_sample_occupation_graph()
obj = TaxonomyInserter(driver)
obj.load_taxonomy(g)

