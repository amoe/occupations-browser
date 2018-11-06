import nltk
import occubrow

with open('/home/amoe/self/alice.txt', 'r') as f:
    sentences = nltk.sent_tokenize(f.read(), language='english')

backend = occubrow.OccubrowBackend()

for sentence in sentences:
    backend.add_sentence(sentence)
    
