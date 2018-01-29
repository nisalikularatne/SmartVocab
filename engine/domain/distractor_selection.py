import pickle
from collections import OrderedDict
import os
import sys
import pkg_resources
import inspect
from nltk.corpus import wordnet as wn
from engine.domain.WordModel import Word
script_path = os.path.dirname(os.path.realpath(__file__))
frequency_list = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../resources/wordlist_byfrequency")))
alphabet_list = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../resources/wordlist_byalphabets")))

def read_file_ordered_by_frequency():
    with open(frequency_list,'r') as f:
        for line in f.readlines():
            l = line.strip().split()
            freq = l[1]
            word = l[2]
            pos = l[3]
            yield freq, word, pos

def read_file_ordered_by_alphabet():
     with open(alphabet_list, 'r') as f:
        for line in f.readlines():
            l = line.strip().split()
            freq = l[1]
            word = l[2]
            pos = l[3]
            yield freq, word, pos

#method where a dictionary is created with frequency as the key
def word_frequency_mapping():
    filename = "word_frequency_mapping.p"
    word_frequency_mapping = os.path.realpath(os.path.abspath(
        os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../resources/" + filename)))
    try:
        word_frequency_mapping = pickle.load(open(word_frequency_mapping, "rb"))
    except IOError as e:
        word_frequency_mapping = OrderedDict()
        for i, (frequency, word, pos) in enumerate(read_file_ordered_by_frequency()):
            # Convert text frequency data into an int
            frequency = int(frequency)
            if word_frequency_mapping.get(frequency):
                word_frequency_mapping[frequency].append((word, pos))
            else:
                word_frequency_mapping[frequency] = [(word, pos)]
    return word_frequency_mapping
if __name__ == "__main__":
    print(read_file_ordered_by_frequency())
    print(next(read_file_ordered_by_frequency()))
    print(next(read_file_ordered_by_alphabet()))
    print(word_frequency_mapping())
    print('hi')