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

def build_word_frequency_table():
    file = "word_frequency_table.p"
    filename = os.path.realpath(os.path.abspath(
        os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../resources/" + file)))
    try:
        word_frequency_table = pickle.load(open(filename, "rb"))
    except IOError as e:
        word_frequency_table = {}
        for freq, word, pos in read_file_ordered_by_alphabet():
            freq = int(freq)
            word_frequency_table[(word, pos)] = freq
        pickle.dump(word_frequency_table, open(filename, "wb"))
    return word_frequency_table

def get_word_frequency(word):
    word_frequency_table = build_word_frequency_table()
    if word[1] in ["a", "n", "v"]:
        return word_frequency_table.get(word)
    else:
        i = 0
        sum = 0
        for p in ["a", "n", "v"]:
            if (word[0], p) in word_frequency_table:
                sum += word_frequency_table[(word[0], p)]
                i += 1
        if i != 0:
            return int(sum / i)
        else:
            return 0;

def get_similar_path_words(word):
    l=return_similar_frequency_words_list(word)
    similar_words = []
    for i in l:
            target = i
            if wn.synsets(target):
             targetword=Word(target)
             wup_similarity=Word(word).definition.sense.wup_similarity(targetword.definition.sense)
             path_similarity=Word(word).definition.sense.path_similarity(targetword.definition.sense)
             if wup_similarity is None :
               wup_similarity=0.0
             if path_similarity is None:
                 path_similarity = 0.0
             if (wup_similarity<0.36) and wup_similarity!=0 and path_similarity<0.15 and path_similarity!=0:
                 similar_words.append(target)
    return similar_words

def return_similar_frequency_words_list(word):
    list_of_similar_words = []
    for i in get_similar_frequency_words(word):
        list_of_similar_words.append(i)
    return list_of_similar_words


def get_similar_frequency_words(word):
    # Find frequency of the word
    pos=Word(word).definition.partOfSpeech
    word_frequency = get_word_frequency((word, pos))
    words_by_frequency_table = word_frequency_mapping()
    similar_frequency_words = []
    n = 1
    result = []
    while len(result) < 20:
        n *= 2
        for freq in range(word_frequency - n, word_frequency+n+1):
            if freq in words_by_frequency_table:
                similar_frequency_words += words_by_frequency_table[freq]
        # Filter out repetitions, parts of different speech, and same words as target
        if pos in ["a", "n", "v"]:
            result = set([w for (w, p) in similar_frequency_words if w != word and p == pos])
        else:
            result = set([w for (w, p) in similar_frequency_words if w != word])
    return result
if __name__ == "__main__":
    print(read_file_ordered_by_frequency())
    print(next(read_file_ordered_by_frequency()))
    print(next(read_file_ordered_by_alphabet()))
    print(word_frequency_mapping())
    print('hi')