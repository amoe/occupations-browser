import occubrow.backend
from load_stop_words import load_stop_words
from load_ab_sample_taxonomy import do_load

backend = occubrow.system.get_backend()
backend.clear_all_data()

load_stop_words()


do_load("/home/amoe/download/Dave/Place.xlsx", 'Place')
do_load("/home/amoe/download/Dave/Object.xlsx", 'Object')
do_load("/home/amoe/download/Dave/Instiutions.xlsx", None)
do_load("/home/amoe/dev/occubrow/backend/scripts/modified_sample_occupation_taxonomy.xlsx", 'Occupation')

