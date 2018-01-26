from nltk.corpus import wordnet as wn
import nltk
nltk.data.path.append('nltk_data')
import random
class Word:
    def __init__(self, word, difficulty=0):
        self.word = word
        self.difficulty = difficulty
        self.definitions = [Definition(sense) for sense in wn.synsets(self.word)]
        self.definition = random.choice(self.definitions)
    def __str__(self):
        return "The Word is: {}".format(self.word)



class Definition:
    def __init__(self, sense):
        self.definition = sense.definition()
        self.sense = sense
        self.pos = sense.pos() #pos : parts of speech



    def __repr__(self):
        return "{}".format(self.definition)



if __name__ == "__main__":

    w = Word("actor")
    print(w.definition)
    print(w)
