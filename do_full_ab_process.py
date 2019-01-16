import occubrow.backend
from load_stop_words import load_stop_words
from load_ab_sample_taxonomy import do_load
from read_sample_taxonomy_assignments import TaxonomyAssignmentReader
import occubrow.taxonomy.taxonomy_inserter
import neo4j
from occubrow.neo4j_schema_utilities \
  import reset_schema, create_constraints, create_indexes

driver = neo4j.GraphDatabase.driver("bolt://localhost:7688", auth=('neo4j', 'password'))

reset_schema(driver)
create_constraints(driver)
create_indexes(driver)

backend = occubrow.system.get_backend()
backend.clear_all_data()

# despicable hack these all now have dates that have to be different because the
# uri is no longer a key, 'key' attr is used so uris can duplicate :/

ti = occubrow.taxonomy.taxonomy_inserter.TaxonomyInserter(driver)

g = do_load("sample_data/activities_modified.xlsx", '2019-01-14', 'Activities')
ti.load_taxonomy(g, 'activity')

g = do_load("sample_data/Place.xlsx", '2019-01-15', 'Place')
ti.load_taxonomy(g, 'place')

g = do_load("sample_data/Object.xlsx", '2019-01-16', 'Object')
ti.load_taxonomy(g, 'object')

g = do_load("sample_data/modified_sample_occupation_taxonomy.xlsx", '2019-01-17', 'Occupation')
ti.load_taxonomy(g, 'occupation')

# It doesn't matter that this is totally broken as none of them are ever 
# actually used

g = do_load("sample_data/statuses_modified.xlsx", '2019-01-18', 'Status')
ti.load_taxonomy(g, 'status')

reader = TaxonomyAssignmentReader(backend)
reader.run("sample_data/modified_sample_taxonomy_assignments.xlsx")

load_stop_words()

