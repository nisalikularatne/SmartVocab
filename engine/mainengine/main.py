# import random
import click
# from quiz import Question
# from student.test_student_model import Student
# from domain.word_lists import word_list
# from instructor.quiz import generate_definition_question
from engine.domain.Domain_Model import DomainModel
from engine.instructor.Quiz_Engine import Instructor

@click.command()
def hello():
    click.echo("Hello. How are you?")

if __name__ == "__main__":

    d = DomainModel()
    I = Instructor(d, 3)

    I.quiz()

