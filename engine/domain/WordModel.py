from nltk.corpus import wordnet as wn
import nltk
nltk.data.path.append('nltk_data')
import random

class Word:
    id=0
    def __init__(self, word):
        from engine.domain.word_cefr_details import find_cefr
        self.id = Word.id
        self.word = word
        self.definitions = [Definition(sense) for sense in wn.synsets(self.word)]
        Word.id += 1
        self.cefr = find_cefr(word)
        self.senses = [Sense(sense, parent=self) for sense in wn.synsets(self.word)]
        self.sensesd = {Sense(sense, parent=self) for sense in wn.synsets(self.word)}
    def __str__(self):
        return "The Word is: {}".format(self.word)
    def __iter__(self):
        return self.senses.__iter__()


class Definition:
    def __init__(self, sense):
        self.definition = sense.definition()
        self.sense = sense
        self.pos = sense.pos() #pos : parts of speech
    def __repr__(self):
        return "{}".format(self.definition)

class Sense:

    def __init__(self, sense, parent):
        # Parse the name to get word
        splitted = sense.name().split('.')
        if len(splitted) == 3:
            self.sense_word = sense.name().split('.')[0]
        else:
            self.sense_word = ".".join(splitted[:-2])
        self.parent_word = parent
        self.sense = sense
        self.id = int(sense.name().split('.')[-1])
        self.pos = sense.pos()
        self.wordnet_name = sense.name()
        self.definition = sense.definition()

    def json(self):
        result = {
            'name': self.name,
            'pos': self.pos,
            'definition': self.definition,
        }
        return result
    def __repr__(self):
        return "<Sense {}>".format(self.wordnet_name)

    def __lt__(self, other):
        if self.parent_word_id == other.parent_word_id:
            self.id < other.id
        else:
            self.parent_word_id < other.parent_word_id

    def __hash__(self):
        return hash(self.wordnet_name)

    def __eq__(self, other):
        return self.wordnet_name == other.wordnet_name

if __name__ == "__main__":


    word = Word("weird").senses
    print(word)


