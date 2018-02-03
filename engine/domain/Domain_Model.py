import random
from engine.domain.WordModel import Word
import os
import inspect
filepath = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../resources/")))
import json
from engine.domain import distractor_selection
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
    def dict_repr(self):
        result = {
            'word': self.word,
            'cefr': self.cefr,
            'senses': {
                k: v.dict_repr() for (k, v) in self.senses.items()
                }
        }
        return result


class Sense:
    def __init__(self, name, pos, definition):
        self.name = name
        self.pos = pos
        self.definition = definition


    def dict_repr(self):
        result = {
            'name': self.name,
            'pos': self.pos,
            'definition': self.definition,
        }
        return result

    def __repr__(self):
        return "<Sense {}>".format((self.name, self.pos,
                                    self.definition))

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

    def __init__(self):
        self.word_list = {}
        filename = filepath + '/data.json'
        if filename:
            with open(filename, 'r') as f:
                datastore = json.load(f)
        for key, value in datastore.items():  # from this we get the sub dictionary of word,cefr and senses
            word = key
            cefr = value['cefr']
            senses = value['senses']
            senses_print = []
            for i in senses:
                id = i['id']
                name = i['name']
                definition = i['definition']
                pos = i['pos']
                s = Sense(name, pos, definition)
                senses_print.append(s)
            w = Word(word, cefr, senses_print)
            self.word_list[word] = w

if __name__ == "__main__":
    d=DomainModel()
    print (d)



