"""This is the file which deals with selecting the distractors for the question being rendered
The file will provide the documentation for each method to enable future developers understand the code
better and to improve understandability and usability"""


import pickle
import os
import inspect
filepath = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../resources/")))
from collections import OrderedDict # An ordered dictionary that keeps words in a list indexable by frequency

"""This method reads the frequency, word and part of speech from the wordlist_byalphabet.txt file
ordered by alphabets"""
def read_file_ordered_by_alphabet():
    with open(filepath+"\wordlist_byalphabets.txt".replace("\\", os.sep)) as f:
        for line in f.readlines():
            l = line.strip().split()
            freq = l[1]
            word = l[2]
            pos = l[3]

            yield freq, word, pos

"""This method reads the frequency, word and part of speech from the wordlist_byfrequency.txt file
ordered by frequency"""
def read_file_ordered_by_frequency():
    with open(filepath+"\wordlist_byfrequency.txt".replace("\\", os.sep)) as f:
        for line in f.readlines():
            l = line.strip().split()
            freq = l[1]
            word = l[2]
            pos = l[3] #pos= part of speech

            yield freq, word, pos


def get_similar_frequency_words(word, pos=""):
    # Find frequency of the word passed into the function using get_word_frequency
    word_frequency = get_word_frequency((word, pos))

    if word_frequency == None:
        raise KeyError
    #make a frequency table with key as word and values as the distractor words
    words_by_frequency_table = build_words_by_frequency_table()
    #list to store the similar_frequency_words
    similar_frequency_words = []
    n = 1
    result = []
    while len(result) < 20:
        n *= 2
        for freq in range(word_frequency-n, word_frequency+n+1):
            if freq in words_by_frequency_table:
                similar_frequency_words += words_by_frequency_table[freq]
        # Filter out repetitions, parts of different speech, and same words as target
        if pos in ["a", "n", "v"]:
            result = set([w for (w, p) in similar_frequency_words if w != word and p == pos])
        else:
            result = set([w for (w, p) in similar_frequency_words if w != word])
    return result

    # Find words that have similar frequency
def build_words_by_frequency_table():
    filename = filepath+"/words_by_frequency_table.p".replace("\\", os.sep)
    try:
        words_by_frequency_table = pickle.load(open(filename, "rb"))
    except FileNotFoundError as e:
        words_by_frequency_table = OrderedDict()
        for i, (frequency, word, pos) in enumerate(read_file_ordered_by_frequency()):
            # Convert text frequency data into an int
            frequency = int(frequency)
            # Build the frequency dictionary using frequency as the key
            if words_by_frequency_table.get(frequency):
                words_by_frequency_table[frequency].append((word, pos))
            else:
                words_by_frequency_table[frequency] = [(word, pos)]
    return words_by_frequency_table

def build_word_frequency_table():
    filename = filepath+"/word_frequency_table.p".replace("\\", os.sep)
    try:
        word_frequency_table = pickle.load(open(filename, "rb"))
    except FileNotFoundError as e:
        word_frequency_table = {}
        for freq, word, pos in read_file_ordered_by_alphabet():
            freq = int(freq)
            word_frequency_table[word] = {pos:freq}
        pickle.dump(word_frequency_table, open(filename, "wb"))
    return word_frequency_table

# This is a data structure in the format
# { rage: {n: 12, v:130}}
_word_frequency_table = build_word_frequency_table()
_words_by_frequency_table = build_words_by_frequency_table()

def get_word_frequency(word, pos=""):
    """
    Returns the frequency of a word in a specific part of speech if
    info is provided, otherwise returns the average frequency.
    """
    if word in _word_frequency_table:
        word_frequencies = _word_frequency_table.get(word)
        if pos == "":
            nums = [int for int in word_frequencies.values()]
            return average(nums)
        if pos in ['a', 'n', 'v'] and pos in word_frequencies:
            return word_frequencies[pos]
        else:
            return 0
    else:

        return 0

def get_word_frequency_all(word):
    if word in _word_frequency_table:
        return _word_frequency_table[word]
    else:
        return 0

def average(list_of_num):
    return int(sum(list_of_num) / len(list_of_num))


if __name__ == "__main__":
    print(read_file_ordered_by_frequency())
    print(next(read_file_ordered_by_frequency()))
    print(next(read_file_ordered_by_alphabet()))
    print(build_word_frequency_table())
    print('hi')
    print(_word_frequency_table['sentiment'])
    print(get_word_frequency("sentiment", 'v'))
    print(get_similar_frequency_words('boy', 'n'))