import occubrow.system
import json


def load_stop_words():
    print("Loading stop words...")
    backend = occubrow.system.get_backend()

    with open('stopwords.json', 'r') as f:
        words = json.load(f)

    for word in words:
        backend.register_stop_word(word)

    backend.register_stop_word('I')

    print("Loaded stop words.")


if __name__ == '__main__':
    load_stop_words()
