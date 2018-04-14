"This is the word model which models and stores all the data related to the words required for this system to function"
import nltk
nltk.data.path.append('nltk_data')
from nltk.corpus import wordnet as wn
"""Class for the Word Model defined with various function. OOP concept of programming 
is being utilised in this file"""
class Word:

    def __init__(self, word):
        from engine.domain.word_cefr_details import find_cefr
        self.word = word
        self.cefr = find_cefr(word)
        self.definitions = [sense.definition() for sense in wn.synsets(self.word)]
        self.senses = [Sense(sense, parent=self) for sense in wn.synsets(self.word)]


    # Iteration
    def __iter__(self):
        return self.senses.__iter__()
    #next word in object
    def __next__(self):
        return self.__next__()
    # Orderable
    def __lt__(self, other):
        if self.word == other.word:
            return self.cefr < other.cefr
        else:
            return self.word < other.word

    # Hashing
    def __eq__(self, other):
        return self.word == other.word
    def __hash__(self):
        return hash((self.word))

    #an object of this class will be representated in the format declared in the method below
    def __repr__(self):
      return "Word '{}'".format((self.word))

#this class defines the methods to handle senses of each word we have defined in the database
class Sense:
    #initiliase
    def __init__(self, sense, parent):
        # Parse the name to get word

        splitted = sense.name().split('.')
        if len(splitted) == 3:
            self.sense_word = sense.name().split('.')[0]
        else:
            self.sense_word = ".".join(splitted[:-2])

        self.parent_word = parent
        self.sense = sense
        self.name = sense.name()
        self.id = int(sense.name().split('.')[-1])
        self.pos = sense.pos()
        self.wordnet_name = sense.name()
        self.definition = sense.definition()
        self.examples = sense.examples()

        self.synonyms = self.get_synonyms()
        self.antonyms = self.get_antonyms()
        self.hypernyms = []

    def __repr__(self):
        return "Sense {}".format(self.wordnet_name)

    def __lt__(self, other):
        if self.parent_word == other.parent_word:
            if self.pos == other.pos:
                return self.id < other.id
            else:
                return self.pos < other.pos
        else:
            return self.parent_word < other.parent_word

    def __hash__(self):
        return hash(self.wordnet_name)

    def __eq__(self, other):
        if isinstance(other, Sense):
            return self.wordnet_name == other.wordnet_name
        else:
            return False

    def list_everything(self):
        print("Name: {}\n"
              "POS: {}\n"
              "Definition: {}\n"
              "Examples: {}\n"
              "Synonyms: {}\n"
              "Antonyms: {}\n"
              "Hypernym: {}\n"
              "Homonyms: {}"
            .format(
            self.wordnet_name,
            self.pos,
            self.definition,
            self.examples,
            self.synonyms,
            self.antonyms,
            self.hypernyms,
            self.homonyms,
        ))
        # print("Lemmas: {}\n".format([Sense(l) for l in self.sense.lemmas()]))

    def get_synonyms(self):
        """ Tried very hard to embed synset information
            However, the lemmas don't have an associated synset information to save
            One solution would be to calculate synsets based on similarity
        """
        result = []
        # Find the original synset from which this sense came
        # The Sense class initializes based on the information provided by a synset
        wordnet_sense = [x for x in wn.synsets(self.sense_word) if x.name() == self.wordnet_name]
        if len(wordnet_sense) == 0:
            return []
        else:
            wordnet_sense = wordnet_sense[0]

            for lemma in wordnet_sense.lemmas():
                result.append(lemma.name())
            if self.sense_word in result:
                result.remove(self.sense_word)
            return result

    def get_antonyms(self):
        result = []
        # Find the original synset from which this sense came
        wordnet_sense = [x for x in wn.synsets(self.sense_word) if x.name() == self.wordnet_name]
        if len(wordnet_sense) == 0:
            print(self.sense)
            return []
        else:
            wordnet_sense = wordnet_sense[0]
        for lemma in wordnet_sense.lemmas():
            result += (x.name() for x in lemma.antonyms())
        # result.remove(self.word)
        return result


def get_senses(word):
    return [sense for sense in wn.synsets(word)]



if __name__ == "__main__":

    word = Word("actor")
    print(word.cefr)
