# import random
import click
# from quiz import Question
# from student.test_student_model import Student
# from domain.word_lists import word_list
# from instructor.quiz import generate_definition_question
from engine.domain.Domain_Model import DomainModel
from engine.student.StudentModel import Student
from engine.instructor.Quiz_Engine import Instructor

if __name__ == "__main__":

    username = input("Hello. Welcome to the Vocabulary ITS\n"
          "To begin enter your username: ")
    password = input("Enter your password: ")

    s = Student(username, password)
    d = DomainModel()
    I = Instructor(d, s, 1)

    choice = 1
    while True:
        print("Hello . How are you {}?".format(username))
        print("\n""Welcome to SmartVocab. Gear up to learn some vocabulary""\n""\n"
        
              "[0] Check Vocabulary Profile\n"
              "[1] Take a Quick Test (10 questions)\n"
              "[2] Learn Vocabulary \n"
              "[3] Review Vocabulary \n"
              "[4] Display Words Seen \n"
              "[5] Display Words Mastered \n"
              "[6] Quit")
        choice = int(input())
        if choice == 0:
            while True:
                choice = input("Enter a word to search, or 'b' to go back, or 'x' to quit: ").lower()
                if choice == 'x':
                    break
                if choice == 'b':
                    break
                else:
                    print("You asked for {}".format(choice))
                    try:
                        print(s.vocabulary_profile[choice].dict_repr)
                    except KeyError:
                        print("Word not found. Try another one.")
            if choice == 'x': break
        elif choice == 1:
            I.testCandidate()

        elif choice==2:
            I.quiz()
        elif choice==3:
            I.review()
        elif choice==4:
           print(s.vocabulary_profile.wordsSeen())
        elif choice==5:
            print(s.vocabulary_profile.wordsMastered())

        elif choice == 6:
            break
        else:
            print("Enter valid option")


    pass
