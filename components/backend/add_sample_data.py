import data_service
import nltk

subset = [
    "keep a Plumber's Shop",
    "deal in cheese",
    "keep the Snow Shoes public-house, in Royal Hospital-row, Chelsea",
    "partnership",
    "Thread Throwster"
]

ds = data_service.DataService()

for x in subset:
    tokens = nltk.word_tokenize(x)
    ds.create_occupation_description_from_tokens(tokens)
