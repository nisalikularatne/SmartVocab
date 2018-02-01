import random


from engine.domain import distractor_selection
from engine.domain.word_cefr_details import word_list, find_cefr
from collections import namedtuple
from engine.domain import WordModel
import ast
import os
import inspect
filepath = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../resources/")))

from nltk.corpus import wordnet

class Word:
    def __init__(self, word, cefr, senses):
        self.word = word
        self.frequency = distractor_selection.get_word_frequency(word)
        self.cefr = cefr
        self.senses = {s.name:s for s in senses}

    def random_sense(self):
        r = random.randint(0, len(self.senses))
        for i, key in enumerate(self.senses):
            if i == r:
                return self.senses[key]

    # Iteration
    def __iter__(self):
        return self.senses.values().__iter__()
    def __next__(self):
        return self.__next__()

    def __len__(self):
        return self.senses.__len__()

    # Orderable
    def __lt__(self, other):
        if isinstance(other, type(self)):
            if self.word == other.word:
                return self.cefr < other.cefr
            else:
                return self.word < other.word
        raise TypeError

    # Hashing
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.word == other.word
        raise TypeError
    def __hash__(self):
        return hash(self.word)
    # Use senses' name to check
    def __getitem__(self, item):
        # Added int to be able to select a random sense
        if isinstance(item, int):
            l = list(self.senses.values())
            return l.__getitem__(item)
        return self.senses.__getitem__(item)
    def __contains__(self, item):
        return item in self.senses

    def json(self):
        return self.__repr__()

    # Representation
    def __repr__(self):
        result = {
            'word': self.word,
            'cefr': self.cefr,
            'senses': {
                k: v.dict_repr() for (k, v) in self.senses.items()
                }
        }
        return result


class Sense:
    def __init__(self, name, pos, definition, examples, synonyms, antonyms, frequency):
        self.name = name
        self.pos = pos
        self.definition = definition
        self.examples = examples
        self.synonyms = synonyms
        self.antonyms = antonyms
        self.frequency = frequency

    def json(self):
        result = {
            'name': self.name,
            'pos': self.pos,
            'definition': self.definition,
            'examples': self.examples,
            'synonyms': self.synonyms,
            'antonyms': self.antonyms,
            'frequency': self.frequency
        }
        return result

    def __repr__(self):
        return "<Sense {}>".format((self.name, self.pos,
                                    self.definition, self.examples,
                                    self.synonyms, self.antonyms,
                                    self.frequency))

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.name < other.name
        raise TypeError
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.name == other.name
        raise TypeError


class DomainModel:
    def __init__(self, filename=filepath+'\\data.in'):
        self.word_list = {}
        W = namedtuple('Word', 'word cefr senses')
        S = namedtuple('Sense', 'name, pos, definition, examples, synonyms, antonyms')
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if not line: break
                w = W._make(line.strip().split('||'))
                word = w.word
                frequency = distractor_selection.get_word_frequency(word)
                cefr = w.cefr
                senses = []
                for i in range(int(w.senses)):
                    line = f.readline()
                    s = (S._make(line.strip().split('||')))
                    name = s.name
                    pos = s.pos
                    definition = s.definition
                    examples = ast.literal_eval(s.examples)
                    synonyms = ast.literal_eval(s.synonyms)
                    antonyms = ast.literal_eval(s.antonyms)
                    frequency = distractor_selection.get_word_frequency(word)
                    s = Sense(name, pos, definition, examples, synonyms, antonyms, frequency)
                    senses.append(s)
                w = Word(word, cefr, senses)
                self.word_list[word] = w

    def filter(self, cefr=None):
        if cefr:
            return filter(lambda word: word.cefr == cefr, self)
        return []

    def items(self):
        return self.word_list.items()

    def random(self):
        return random.choice(self.word_list.keys())

    def sample(self, n):
        return random.sample(self.word_list.keys(), n)

    def save(self):
        result = ""
        for word in self:
            result += "{}||{}||{}\n".format(word, find_cefr(word), len(self[word]))
            for s in self[word]:
                result += "{}||{}||{}||{}||{}||{}\n".format(s.name, s.pos,
                                                          s.definition, s.examples,
                                                          s.synonyms, s.antonyms)
        with open(filepath+'\\data.in', 'w') as f:
            f.write(result)

    def __iter__(self):
        return self.word_list.__iter__()
    def __next__(self):
        return self.__next__()
    def __len__(self):
        return self.word_list.values().__len__()
    def __getitem__(self, item):
        if not self.word_list.__contains__(item):
            wd = WordModel.Word(item)
            word = wd.word
            cefr = wd.cefr
            senses = []
            for s in wd:
                frequency = distractor_selection.get_word_frequency(word, s.pos)
                sense = Sense(s.wordnet_name, s.pos, s.definition, s.examples,
                      s.synonyms, s.antonyms, frequency)
                senses.append(sense)
            self.word_list[item] = Word(word, cefr, senses)
            # self.save()
        return self.word_list.__getitem__(item)
    def __contains__(self, item):
        return item in self.word_list

def print_info():
    for word in word_list:
        # CSV format
        # Word -
        # Word,CEFR,Num_Senses
        # Senses -
        # name, pos, definition, examples, synonyms, antonyms
        # Followed by that many lines of senses
        w = WordModel.Word(word)
        print(word, find_cefr(word), len(w.senses), sep="||")
        for s in w:
            print(s.wordnet_name, s.pos, s.definition, s.examples,
                  s.synonyms, s.antonyms, sep='||')


if __name__ == "__main__":
    # print_info()
    d = DomainModel()
    d.save()
    for i, word in enumerate(d):
        if i > 10:
             break
        print(word)