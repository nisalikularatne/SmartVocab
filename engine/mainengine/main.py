# import random
import click
# from quiz import Question
# from student.test_student_model import Student
# from domain.word_lists import word_list
# from instructor.quiz import generate_definition_question
from engine.domain.Domain_Model import DomainModel
from engine.instructor.Quiz_Engine import Instructor
from engine.student.StudentModel import Student
@click.command()
def hello():
    click.echo("Hello. How are you?")

if __name__ == "__main__":

    d = DomainModel()
    s=Student('jaslin3','123')
    I = Instructor(d,s, 10)

    I.quiz()

