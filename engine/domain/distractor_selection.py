import pickle
from collections import OrderedDict
import os
import sys
import pkg_resources
import inspect
from nltk.corpus import wordnet as wn
from engine.domain.WordModel import Word
script_path = os.path.dirname(os.path.realpath(__file__))
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../resources/wordlist_byalphabets")))
def read_file_ordered_by_frequency():
    with open(cmd_subfolder,'r') as f:
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