import nltk
import occubrow

with open('/home/amoe/self/alice.txt', 'r') as f:
    sentences = nltk.sent_tokenize(f.read(), language='english')

for sentence in sentences:
    occubrow.add_sentence(sentence)
    
