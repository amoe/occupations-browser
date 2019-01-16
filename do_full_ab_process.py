import occubrow.backend
from load_stop_words import load_stop_words
from load_ab_sample_taxonomy import do_load
from create_indexes import create_indexes
from read_sample_taxonomy_assignments import TaxonomyAssignmentReader
import occubrow.taxonomy.taxonomy_inserter
import neo4j

driver = neo4j.GraphDatabase.driver("bolt://localhost:7688", auth=('neo4j', 'password'))

backend = occubrow.system.get_backend()
backend.clear_all_data()

ti = occubrow.taxonomy.taxonomy_inserter.TaxonomyInserter(driver)


g = do_load("/home/amoe/dev/occubrow/backend/scripts/activities_modified.xlsx", 'Activities')
ti.load_taxonomy(g, 'activities')

g = do_load("/home/amoe/download/Dave/Place.xlsx", 'Place')
ti.load_taxonomy(g, 'place')

g = do_load("/home/amoe/download/Dave/Object.xlsx", 'Object')
ti.load_taxonomy(g, 'object')

g = do_load("/home/amoe/dev/occubrow/backend/scripts/modified_sample_occupation_taxonomy.xlsx", 'Occupation')
ti.load_taxonomy(g, 'occupation')

reader = TaxonomyAssignmentReader()
reader.run("/home/amoe/dev/occubrow/backend/scripts/modified_sample_taxonomy_assignments.xlsx")


load_stop_words()
create_indexes()

