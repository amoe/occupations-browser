import data_service
import nltk

subset = [
    {
        'content': "keep a Plumber's Shop",
        'category': 'Deepstaria enigmatica',
    },
    {
        'content':"deal in cheese",
        'category': "Deepstaria reticulum"
    },
    {
        'content': "keep the Snow Shoes public-house, in Royal Hospital-row, Chelsea",
        'category': "Deepstaria enigmatica"
    },
    {
        'content': "partnership",
        'category': "Deepstaria reticulum"
    },
    {
        'content': "Thread Throwster",
        'category': "Deepstaria enigmatica"
    }
]

ds = data_service.DataService()

for x in subset:
    tokens = nltk.word_tokenize(x['content'])
    ds.create_occupation_description_from_tokens(token_seq=tokens, category=x['category'])
