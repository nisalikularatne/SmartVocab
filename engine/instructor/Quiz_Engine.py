import random
from nltk.corpus import wordnet as wn
from engine.domain.Domain_Model import DomainModel
from engine.domain.WordModel import Word
from engine.domain.word_cefr_details import word_list
from engine.domain.distractor_selection import get_similar_frequency_words
class Instructor:
    def __init__(self,domain_model,n=10):
        self.domain_model = domain_model
        self.n = n

    def quiz(self):
        words = [word for word in self.domain_model ]
        for word in random.sample(words, self.n):
            q = self.automatic_quiz_generator(word)
            q.request()

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
    q = Instructor(d,3)
    q.quiz()

