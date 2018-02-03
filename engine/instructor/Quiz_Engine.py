import random
from nltk.corpus import wordnet as wn
from engine.domain.Domain_Model import read_from_domain_json
from engine.domain.WordModel import Word
from engine.domain.distractor_selection import get_similar_path_words
def automatic_quiz_generator(word, question="What's the definition of {}"):

    definitions = Word(word).definitions
    definition = [definition for definition in definitions if word not in definition.definition]
    definition = random.choice(definition)
    distractors = random.sample(get_similar_path_words((word,Word(word).pos)),3)
    distractors = [random.choice(wn.synsets(w)).definition() for w in distractors]
    return Question(word, question, correct=definition, incorrect=distractors)

class Question:
    def __init__(self, sense,word, prompt, correct, incorrect,response=''):
        self.sense=sense
        self.word = word
        self.prompt = prompt
        self.correct = correct
        self.incorrect = incorrect
        self.response = response

    def quiz(self):
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
        automatic_quiz_generator(word).quiz()

if __name__ == "__main__":
    for word in ["city","bitch","racism","actor","prince","reputation"]:

            automatic_quiz_generator(word).quiz()


