import unittest
from hamcrest import *
from engine.domain.word_cefr_details import find_cefr
class TestWordCefr(unittest.TestCase):

    def test_read_file_by_frequency(self):
        expected_res="C1"
        res=find_cefr("the")
        expected_res2 = "A2"
        res2 = find_cefr("snake")
        self.assertEqual(expected_res, res)
        self.assertEqual(expected_res2,res2)
        self.assertNotEqual(expected_res, res2)
