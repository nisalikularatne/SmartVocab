import unittest
from engine.student.StudentModel import Student
s=Student(username='jaslin3',password='1234')
class TestStudentModel(unittest.TestCase):
    def test_student_vocabulary_profile(self):
        word=s.vocabulary_profile['thanks']
        self.assertNotIsInstance(word, str)
        self.assertIsInstance(word, object)

    def test_update_sense(self):
        updation=s.vocabulary_profile['thanks'].updateSense('thanks.n.01', correct=True)
        self.assertIsNone(updation)