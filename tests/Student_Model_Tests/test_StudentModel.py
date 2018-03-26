import unittest
from engine.student.StudentModel import Student
s=Student(username='jaslin3',password='1234')
class TestStudentModel(unittest.TestCase):
    def test_read_file_by_frequency(self):
        word=s.vocabulary_profile['thanks']
        self.assertNotIsInstance(word, str)
        self.assertIsInstance(word, object)