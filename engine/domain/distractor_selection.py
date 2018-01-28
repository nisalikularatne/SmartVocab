import pickle
from collections import OrderedDict
import os
from nltk.corpus import wordnet as wn
from engine.domain.WordModel import Word
script_path = os.path.dirname(os.path.realpath(__file__))
path = 'home\\travis\\build\\nisalikularatne\\SmartVocab\\resources\\wordlist_byalphabets'
def read_file_ordered_by_frequency():
    with open(path,'r') as f:
        for line in f.readlines():
            l = line.strip().split()
            freq = l[1]
            word = l[2]
            pos = l[3]
            yield freq, word, pos
if __name__ == "__main__":
    print(read_file_ordered_by_frequency())
    print(next(read_file_ordered_by_frequency()))
