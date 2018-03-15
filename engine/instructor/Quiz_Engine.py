import random
from nltk.corpus import wordnet as wn
from engine.domain.Domain_Model import DomainModel
from engine.student.StudentModel import Student
import os
import inspect
filepath = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../resources/")))

from engine.domain.distractor_selection import get_similar_frequency_words
ITEM_LIST = []
class Instructor:
    def __init__(self,domain_model,student_model,n=10):
        self.domain_model = domain_model
        self.student_model=student_model
        self.n = n
    def load_words(self):
    # Loads words according to the user's proficiency
    # First gets words the user has activated

        words = list(set(self.student_model.wordsNotMastered()))
    # Filter
        while len(words) < 50:
            diff_list = [-2.0,-1.200000000000000,-0.40000000000000013,0.3999999999999999 , 1.2, 2.0]
            ind = diff_list.index(self.student_model.cefr)
            words = [w for w in self.domain_model if self.domain_model[w].cefr in diff_list[:ind+1]]
        return words

    def quiz(self):
        words = self.load_words()
        for word in random.sample(words, self.n):
            ITEM_LIST.append(d[word].item_no)
            q = self.automatic_quiz_generator(word)
            correct=q.request()
            sense=q.sense.name
            self.student_model[word].updateSense(sense, correct)
            self.student_model[word].update()
        self.student_model.save()
    def get_item_list(self):
        filename = filepath + '/item_list.txt'
        if filename:
                thefile = open(filename, 'w')
                for item in ITEM_LIST:
                    thefile.write("%s\n" % item)



    def automatic_quiz_generator(self,word, prompt="What's the definition of {}"):
        senses = self.domain_model[word] #sense object list
        candidates = [sense for sense in senses if word not in sense.definition] #list of the sense
        if candidates:
            global sense
            sense = random.choice(candidates) #gets random sense
        # Generate Question
        # First randomly select a definition
        global definition
        definition=sense.definition
        pos = sense.pos
        try:
            # Get words in the same part of speech that have similar frequency
            # First returns a list of similar frequency words
            # Then chooses 3 candidates

            distractor_candidates = random.sample(get_similar_frequency_words(word, pos), 3)

            # For each distractor, find the definition
            # Make sure the part of speech matches
            distractors = []
            for candidate in distractor_candidates:
                distractor = random.choice([s.definition for s in self.domain_model[candidate]  if s.pos == pos])
                distractors.append(distractor)

        except (KeyError, IndexError) as e:
            print("Couldn't find the frequency for this word")
            print(e)
            distractor = random.choice([s.definition for s in self.domain_model[candidate]])
            distractors.append(distractor)

        return Question(sense, prompt, correct=definition, incorrect=distractors)


class Question:
    def __init__(self, sense, prompt, correct, incorrect,response=''):
        self.sense=sense
        self.word = "".join(sense.name.split('.')[0:-2])
        self.prompt = prompt
        self.correct = correct
        self.incorrect = incorrect
        self.response = response

    def request(self):
        print(self.prompt.format(self.word))
        choices = self.incorrect + [self.correct]
        random.shuffle(choices)
        for i, choice in enumerate(choices):
            print("[{}]: {}".format(i, choice))
        try:
         answer = int(input())
         if choices[answer] == self.correct:
             print("That is correct")
             return True
         else:
             if self.response == "":
                 self.response = "The correct answer is {}".format(self.correct)

             print("Incorrect\n"
                   "{}".format(self.response))
             return False
        except IndexError :
            print("You entered a wrong input for the question")


if __name__ == "__main__":

    d = DomainModel()
    s=Student('jaslin3','123')
    q = Instructor(d,s,3)
    q.quiz()
    q.get_item_list()


