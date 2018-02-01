import os
import inspect
import pickle
filepath = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../resources/")))
from engine.domain.WordModel import Word


def retrieve_cefr_information():
    word_cefr_file = pickle.load(open(filepath+"/word_cefr_file.p", "rb"))
    print(len(word_cefr_file.items()))
    word_cefr_file = [(k, v) for k, v in word_cefr_file.items()]
    return word_cefr_file

def retrieve_word_list_with_wordnet_info():
    word_cefr_file = pickle.load(open(filepath+"/word_cefr_file.p", "rb"))
    word_cefr_file = [Word(k, v) for k, v in word_cefr_file.items()]
    return word_cefr_file

def load_word_list():
    # Redundant
    word_list = [k for k,v in retrieve_cefr_information()]

    return word_list


def load_domain_model():
    vocab_list = []
    for word, cefr in retrieve_cefr_information().items():
        vocab_list.append(Word(word))
    return vocab_list

def load_word_list_by_cefr_key():
    return pickle.load(open(filepath+"/word_list_by_cefr_key.p", 'rb'))

def find_cefr(word):
    for cefr, wordset in load_word_list_by_cefr_key().items():
        if word in wordset:
            return cefr
    return "U0"


word_list_by_cefr_key = load_word_list_by_cefr_key()
word_list = load_word_list()

if __name__ == "__main__":
    print(find_cefr("the"))
    print(retrieve_cefr_information())
    print(load_word_list_by_cefr_key())