import pickle
from engine.domain.word_cefr_details import retrieve_cefr_information, word_list
from engine.domain.WordModel import Word

from engine.domain.Domain_Model import DomainModel
class WordProfile:
    # Word profile is made up of all the word senses
    # Each sense has an individual score associated with it
    # There's an overall word score as well
    def __init__(self, word):
        self.word = Word(word)
        self.total_score = 0.0
        self.sense_profiles = {sense.name: SenseProfile(self, sense) for sense in word}
        self.n = len(self.senses_profiles)

    def __iter__(self):
        return self.senses_profiles.__iter__()
    def __next__(self):
        return self.senses_profiles.__next__()

    def __eq__(self, other):
        return self.word.word == self.other.word and self.word.cefr == self.other.cefr

    def __hash__(self):
        return self.word.__hash__()

    def __repr__(self):
        result = ""
        result += "The word profile for {} is {:.4f}: \n\t".format(self.word, self.total_score)
        for sense_profile in self.senses_profiles:
            result += str(sense_profile) + '\n\t'
        return result
    # Total Score is the average of all sense scores

    def update_score(self):
        self.total_score = (sum([x.score for x in self.senses_profiles])/self.n)




class VocabularyProfile:
    def __init__(self):

        self.profile = {}

        d = DomainModel()
        for word_name, word_model in d.items():
         self.profile[word_name] = WordProfile(word_model)
    pass

    def __getitem__(self, item):
        return self.profile[item]
    def items(self):
        return self.profile.items()
    def __iter__(self):
        return self.profile.__iter__()
    def __next__(self):
        return self.profile.__next__()
    def __repr__(self):
        result = ''
        for _, word_profile in self.items():
            result += '{}\n'.format(word_profile)
        return result



class SenseProfile:
    # Sense profile is an individual sense
    # A question is generated based on the word sense
    # A score is given based on the word sense
    # Each sense has an associated history of questions that have been asked
    def __init__(self, sense, parent):
        self.parent = parent
        self.sense = sense
        self.name=sense.name
        self.score = 0.0


    def __repr__(self):
        return "{}".format((self.sense.name, self.score))


    def update_score(self, correct):
        if correct:
            self.score += 0.2
        else:
            self.score -= 0.2
        self.parent.update_score()





class Student:
    def __init__(self, name, password,new=False):
        self.name = name
        self.password = password
        self.vocabulary_profile = {}
        for word in word_list:
            self.vocabulary_profile[word] = WordProfile(word)
        if new:
            self.save()
        else:
            self.load()



    def get_word_profile(self, word):
        return self.vocabulary_profile[word]

    def get_sense_profile(self, sense):
        return self.get_word_profile(sense.parent_word.word).senses_profiles

    def update_score(self, sense, correct):
        # Find the sense
        sense_profiles = self.get_sense_profile(sense)
        for s in sense_profiles:
            if s == sense:
                s.update_score(correct)


if __name__ == "__main__":
    d=VocabularyProfile()
    print(d)