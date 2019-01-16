import occubrow.system
import occubrow.taxonomy.taxonomy_inserter
from occubrow.formats.thematic_categories_xlsx import SamuelsLoader
from occubrow.corpus.ob_samuels_csv import OBSamuelsCSVLoader
from occubrow.corpus.import_sample_sentences import import_annotation_file
from create_indexes import create_indexes
from load_stop_words import load_stop_words
import sys
import neo4j

SAMPLING_PROBABILITY = 0.001

driver = neo4j.GraphDatabase.driver("bolt://localhost:7688", auth=('neo4j', 'password'))
ti = occubrow.taxonomy.taxonomy_inserter.TaxonomyInserter(driver)

backend = occubrow.system.get_backend()
backend.clear_all_data()


loader = SamuelsLoader()
g = loader.load("/home/amoe/download/media_405073_en.xlsx")
ti.load_taxonomy(g, 'theme')

loader2 = OBSamuelsCSVLoader(SAMPLING_PROBABILITY)
loader2.run("/home/amoe/dev/samdist/intermediate_data/m_nonl_combined.csv", 'samuels-annotated.xml')

import_annotation_file('samuels-annotated.xml')

load_stop_words()
create_indexes()
