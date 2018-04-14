import random
from nltk.corpus import wordnet as wn
from engine.domain.Domain_Model import DomainModel
from engine.utils.dump_to_json import read_from_domain_json
from engine.student.StudentModel import Student
import os
import inspect
filepath = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../resources/")))
filepath2 = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../users/used_items")))
from colorama import Fore, Back, Style
from engine.IRT_Model.catsim.initialization import RandomInitializer
from engine.IRT_Model.catsim.selection import MaxInfoSelector,LinearSelector
from engine.IRT_Model.catsim.estimation import HillClimbingEstimator,DifferentialEvolutionEstimator
from engine.IRT_Model.catsim.stopping import MaxItemStopper
from catsim.simulation import Simulator
from engine.IRT_Model.catsim.plot import *
from engine.domain.distractor_selection import get_similar_frequency_words

ITEM_LIST = []
responses = []
class Instructor:
    def __init__(self,domain_model,student_model,n=10):
        self.domain_model = domain_model
        self.student_model=student_model
        self.n = n
    def load_words(self):
    # Loads words according to the user's proficiency
    # First gets words the user has activated
     words = self.student_model.wordsSeen()
     words = list(set(words + self.student_model.wordsNotMastered()))
     while len(words) < 50:
        diff_list = ["-2.0", "-1.2", "-0.40000000000000013", "0.3999999999999999", "1.2", "2.0"]
        ind = diff_list.index(self.student_model.cefr)
        words = [w for w in self.domain_model if self.domain_model[w].cefr in diff_list[:ind + 1]]
     return words


    def testCandidate(self):
        words = list(set(self.student_model.wordsNotMastered()))
        word12=[]
        filepath = os.path.realpath(os.path.abspath(
            os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../instructor/")))

        items = numpy.loadtxt("C:\\Users\\Nisali Kularatne\\Documents\\final year project\\engine\\instructor\\nisali.txt")

        initializer = RandomInitializer()
        selector = MaxInfoSelector(self.student_model)
        estimator = DifferentialEvolutionEstimator([-1,1])
        stopper = MaxItemStopper(5)
        est_theta = "-0.40000000000000013"
        for word in self.domain_model:
            if (self.domain_model[word].cefr == est_theta):
                word12.append(word)

        wordinitial=random.choice(word12)
        words1=[wordinitial]

        i=0
        for word in words1:
            est_theta = -0.40000000000000013
            ITEM_LIST.append(self.domain_model[word].item_no)
            q = self.automatic_quiz_generator(word)
            correct=q.request()
            filename = filepath2 + "\\{}-{}-useditems.txt".format(self.student_model.username, self.student_model.password)
            if not os.path.exists(filename):
                with open(filename, 'w'): pass
            thefile=open(filename,'a')
            new_theta = estimator.estimate(items=items,
                                           administered_items=ITEM_LIST,
                                           response_vector=responses, est_theta=est_theta)
            item_index = selector.select(items=items,
                                         administered_items=ITEM_LIST,
                                         est_theta=new_theta)

            thefile.write("%s\n" % item_index)
            for word in self.domain_model:
                if (self.domain_model[word].item_no == item_index):
                    words1.append(word)

            sense = q.sense.name



            i=i+1
            if(i==10):
                break
        if(new_theta<=-2.0):
            print("The grade assigned is C2")
        elif(new_theta>-2.0 and new_theta<=-1.2):
            print("The grade assigned is C1")
        elif (new_theta > -1.2 and new_theta <= -0.40000000000000013):
            print("The grade assigned is B2")
        elif (new_theta > -0.40000000000000013 and new_theta <= 0.3999999999999999):
            print("The grade assigned is B1")
        elif (new_theta > 0.3999999999999999 and new_theta <=1.2):
            print("The grade assigned is A2")
        elif (new_theta >1.2 and new_theta <=2.0):
            print("The grade assigned is A1")
        return new_theta

    def testCandidateeval(self):
        words = list(set(self.student_model.wordsNotMastered()))
        word12 = []
        filepath = os.path.realpath(os.path.abspath(
            os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../instructor/")))

        items = numpy.loadtxt(
            "C:\\Users\\Nisali Kularatne\\Documents\\final year project\\engine\\instructor\\nisali.txt")

        initializer = RandomInitializer()
        selector = LinearSelector([3873,3887,4118,2754,2014,2010,1950,1912,1870])
        estimator = DifferentialEvolutionEstimator([-1, 1])
        stopper = MaxItemStopper(5)
        est_theta = "2.0"
        for word in self.domain_model:
            if (self.domain_model[word].cefr == est_theta):
                word12.append(word)


        wordinitial = random.choice(word12)
        words1 = ["completion"]

        i = 0
        for word in words1:
            est_theta = 2.0
            ITEM_LIST.append(self.domain_model[word].item_no)
            q = self.automatic_quiz_generator(word)
            correct = q.request()

            filename = filepath2 + "\\{}-{}-useditems.txt".format(self.student_model.username,
                                                                  self.student_model.password)
            if not os.path.exists(filename):
                with open(filename, 'w'): pass
            thefile = open(filename, 'a')
            new_theta = estimator.estimate(items=items,
                                           administered_items=ITEM_LIST,
                                           response_vector=responses, est_theta=est_theta)
            item_index = selector.select(items=items,
                                         administered_items=ITEM_LIST,
                                         est_theta=new_theta)

            thefile.write("%s\n" % item_index)
            for word in self.domain_model:
                if (self.domain_model[word].item_no == item_index):
                    words1.append(word)

            sense = q.sense.name

            print(new_theta)
            i = i + 1
            if (i == 10):
                break
        if (new_theta <= -2.0):
            print("The grade assigned is C2")
        elif (new_theta > -2.0 and new_theta <= -1.2):
            print("The grade assigned is C1")
        elif (new_theta > -1.2 and new_theta <= -0.40000000000000013):
            print("The grade assigned is B2")
        elif (new_theta > -0.40000000000000013 and new_theta <= 0.3999999999999999):
            print("The grade assigned is B1")
        elif (new_theta > 0.3999999999999999 and new_theta <= 1.2):
            print("The grade assigned is A2")
        elif (new_theta > 1.2 and new_theta <= 2.0):
            print("The grade assigned is A1")
        return new_theta

    def quiz(self):
        words=self.load_words()
        for word in random.sample(words,self.n):
            ITEM_LIST.append(self.domain_model[word].item_no)
            q = self.automatic_quiz_generator(word)
            correct=q.request(word)
            sense=q.sense.name
            self.student_model[word].updateSense(sense, correct)
            self.student_model[word].update()
        self.student_model.save()
    def review(self):
        words=self.student_model.wordsSeen()
        for word in random.sample(words,self.n):

            ITEM_LIST.append(self.domain_model[word].item_no)
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
                distractor = random.choice([s.definition for s in self.domain_model[candidate]  ])
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

    def request(self,word):
        d=DomainModel()
        print(self.prompt.format(self.word))
        choices = self.incorrect + [self.correct]
        random.shuffle(choices)
        for i, choice in enumerate(choices):
            print("[{}]: {}".format(i, choice))
        try:
         answer = int(input())
         if choices[answer] == self.correct:
             print(Fore.GREEN+ "That is correct")
             responses.append(True)
             return True
         else:
             if self.response == "":
                 self.response = "The correct answer is {}".format(self.correct)
             fas = read_from_domain_json()
             print("----------------------------------------------------------------------------------------------------")
             print("FEEDBACK SECTION\n")
             print(Fore.RED +"Incorrect\n"
                   "{}".format(self.response)+'\n')

             for x in fas[word]["senses"]:
                 if x['name'] == self.sense.name:
                     if x['examples'] != []:
                         print("Here are some example usages of the word "+word+" of which "+self.sense.name+" is a sense")
                         for i,w in enumerate(x['examples']):
                             print("{}): {}".format(i+1, w))
                         print('')
                     else:
                         print("Sorry the word has no examples currently")
                         print('')
                     if x['synoyms'] != []:
                         print("Here are some synonyms of the word "+word+" of which "+self.word+" is a sense")
                         for i,w in enumerate(x['synoyms']):
                             print("{}): {}".format(i + 1, w))

                     else:
                         print("Sorry the word has no synonyms currently")

             print('-----------------------------------------------------------------------------------------------------')

             responses.append(False)
             return False
        except(ValueError,IndexError) :
            print("You entered a wrong input for the question")
            print(self.prompt.format(self.word))
            choices = self.incorrect + [self.correct]

            for i, choice in enumerate(choices):
                print("[{}]: {}".format(i, choice))

            answer = int(input())
            if choices[answer] == self.correct:
                    print(Fore.GREEN + "That is correct")
                    responses.append(True)
                    return True
            else:
                    if self.response == "":
                        self.response = "The correct answer is {}".format(self.correct)

                    print(Fore.RED + "Incorrect\n"
                                     "{}".format(self.response))

                    print([x for x in fas[self.word]["senses"][self.sense.name]["examples"]])
                    responses.append(False)
                    return False



if __name__ == "__main__":

    d = DomainModel()
    s=Student('nethmie','nethmielime')
    q = Instructor(d,s,10)
    q.quiz()



