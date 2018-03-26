import pickle
from engine.domain.word_cefr_details import retrieve_cefr_information, word_list
from engine.domain.WordModel import Word,Sense
from engine.instructor.LogisticRegressionModel import LogisticRegressionModel
import os
import inspect
import json
from collections import namedtuple
filepath = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../users/")))
import time
class WordProfile:
    # Word profile is made up of all the word senses
    # Each sense has an individual score associated with it
    # There's an overall word score as well
    def __init__(self, word,sense_profiles,score,active,date_activated,new):
        if new == False:
            self.word = word
            self.score = score
            self.sense_profiles = {s: SenseProfile.load_json(word, sp) for s, sp in sense_profiles.items()}
            self.n = len(self.sense_profiles)
            self.active = active
            self.date_activated = date_activated
        else:
            self.word = word
            self.original=word
            self.score = 0.0
            self.sense_profiles = {sense.name: SenseProfile(self, sense,sense.name,self.score,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) for sense in Word(self.word)}
            self.n = len(self.sense_profiles)
            self.active=False
            self.date_activated=None


    @staticmethod
    def load_json(word_profile, new=False):
        word = word_profile['word']
        score = word_profile['score']
        sense_profiles_json = word_profile['sense_profile']
        active = word_profile['active']
        date_activated = word_profile['date_activated']
        return WordProfile(word, sense_profiles_json,score,active,date_activated,new=False)

    def __len__(self):
        return self.sense_profiles.__len__()

    def __iter__(self):
        return self.sense_profiles.__iter__()
    def __next__(self):
        return self.sense_profiles.__next__()

    def __getitem__(self, item):
        return self.sense_profiles.__getitem__(item)

    def __eq__(self, other):
        return self.word.word == self.other.word and self.word.cefr == self.other.cefr

    def __hash__(self):
        return self.word.__hash__()



    def __repr__(self):
            result = "The word {} which has {} senses has a score of {}\n".format(self.word,len(self), self.score)
            for sense_profile in self:
                result += "\t{}\n".format(self[sense_profile])
            return result.rstrip()

    def dict_repr(self):

        result = {
            "word": self.word,
            "score": self.score,
            "sense_profile": {
                name: sense_profile.dict_repr() for name, sense_profile in self.sense_profiles.items()
            },
            "active": self.active,
            "date_activated": self.date_activated

        }

        return result
    # Total Score is the average of all sense scores

    def update(self):
        if self.n == 0: return 0
        if self.active == False:
            self.active = True
            self.date_activated = time.strftime("%c")
        self.score = sum([v.score for x, v in self.sense_profiles.items()]) / self.n


    def updateSense(self, sense, correct):
        if isinstance(sense, str):
            return self[sense].update(correct)
        else:
            return self[sense.name].update(correct)
        self.update()


class SenseProfile:
    # Sense profile is an individual sense
    # A question is generated based on the word sense
    # A score is given based on the word sense
    # Each sense has an associated history of questions that have been asked
    def __init__(self, sense, parent,name,score,answer_history,new=False):
        if new==False:
            self.score=score
            self.word = parent
            self.name = name
            self.proficiency = LogisticRegressionModel(answer_history=answer_history)

        else   :
            self.parent = parent
            self.sense = sense
            self.name=name
            self.original=sense.original

            self.score = 0.0





    def dict_repr(self):
        result = {'name': self.name,
                       'score':self.score,
                  'answer_history': self.proficiency.__repr__()
                        }


        return result
    def __repr__(self):
        return "The sense {} got a score of {}".format(self.name,self.score)
    def __eq__(self, other):
        if isinstance(other, Sense):
            return self.sense == other
        else:
            return self.sense == other.sense

    def __hash__(self):
        return hash((self.sense))
    # Update Score for the sense

    def update(self, correct):
        self.score = self.proficiency.update(correct)


    @staticmethod
    def load_json(w, sp):
        word = w
        name = sp['name']
        score = sp['score']
        answer_history = eval(sp['answer_history'])
        sense=None
        return SenseProfile(sense,word, name, score,answer_history,new=False)


class VocabularyProfile:
    def __init__(self):

        self.profile = {}


        for word in word_list:
            self.profile[word] = WordProfile(word,sense_profiles=None,score=0.0,active=False,date_activated=None,new=True)
        pass

    def words(self, n=0, f=None):
        result = []
        i = 1
        if n == 0:
            for word in filter(f, self):
                result.append(word)
        else:
            for word in filter(f, self):
                if i > n: break
                result.append(word)
                i += 1
        return result

    def wordsSeen(self, n=0):
        return self.words(n, lambda x: self[x].active)

    def wordsNotSeen(self, n=0):
        return self.words(n, lambda x: not self[x].active)

    def wordsMastered(self):
        return self.words(f=lambda x: self[x].score > 0.7)

    def wordsNotMastered(self):
        return self.words(f=lambda x: self[x].score < 0.7 )

    def __getitem__(self, item):
        return self.profile[item]
    def items(self):
        return self.profile.items()
    def __iter__(self):
        return self.profile.__iter__()
    def json(self):
        return self.profile
    def __next__(self):
        return self.profile.__next__()
    def dict_repr(self):
        result = {}
        for _, word_profile in self.items():
            result[_] = word_profile.dict_repr()
        return result
    def __repr__(self):
        result = {}
        for _, word_profile in self.items():
            result[_] = word_profile
        return str(result)

    def load_json(self, f, new=False):
        if new == False:
            vocabulary_profile = f['vocabulary_profile']
        for word, word_profile in vocabulary_profile.items():
            self.profile[word] = WordProfile.load_json(word_profile, new)




class Student:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.vocabulary_profile = VocabularyProfile()
        self.filename = filepath + "/{}-{}-model.json".format(self.username, self.password)

        if os.path.isfile(self.filename):
            self.load(new=False)
        else:
            new = input("User does not exist. Create a new user? (Y) or (N): ")
            if new.lower() == "y" or new.upper()=="Y":
                self.save()
            else:

                raise Exception("User does not exist")

    def save(self):
                filename = filepath + "/{}-{}-model.json".format(self.username, self.password)
                with open(filename, 'w') as f:
                    f.write(json.dumps(self.dict_repr(), indent=4))

    def get_word_profile(self, word):
        return self.vocabulary_profile[word]

    def get_sense_profile(self, sense):
        return self.get_word_profile(sense.parent_word.word).senses_profiles

    def update(self, sense, correct):
        # Find the sense
        sense_profiles = self.get_sense_profile(sense)
        for s in sense_profiles:
            if s == sense:
                s.update_score(correct)
    def __getitem__(self, item):
        return self.vocabulary_profile[item]

    def __getattr__(self, item):
        return self.vocabulary_profile.__getattribute__(item)
    def dict_repr(self):
        result = {
            'username': self.username,
            'password': self.password,
            'vocabulary_profile': self.vocabulary_profile.dict_repr(),
        }
        return result
    def __repr__(self):
        result = '{}||{}\n'.format(self.username, self.password)
        result += self.vocabulary_profile.__repr__()
        return result

    def load(self, new=False):
        filename = filepath + "/{}-{}-model.json".format(self.username, self.password)

        with open(filename, 'r') as f:
            f = json.load(f)
            self.vocabulary_profile.load_json(f, new=new)


if __name__ == "__main__":

  s=Student('jaslin3','1234')
  s.vocabulary_profile['thanks'].updateSense('thanks.n.01', correct=True)

  s.save()













