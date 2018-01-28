import pickle
from collections import OrderedDict
import os
import sys
import pkg_resources
from nltk.corpus import wordnet as wn
from engine.domain.WordModel import Word
script_path = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname())
DEFINITIONS_ROOT = os.path.join(PROJECT_ROOT, 'resources', 'wordlist_byalphabets')
CONFIG_PATH = pkg_resources.resource_filename('resources', 'wordlist_byalphabets')
path = '/home/travis/build/nisalikularatne/SmartVocab/resources/wordlist_byalphabets'
def read_file_ordered_by_frequency():
    with open(DEFINITIONS_ROOT,'r') as f:
        for line in f.readlines():
            l = line.strip().split()
            freq = l[1]
            word = l[2]
            pos = l[3]
            yield freq, word, pos
if __name__ == "__main__":
    print(read_file_ordered_by_frequency())
    print(next(read_file_ordered_by_frequency()))
    print('hi')