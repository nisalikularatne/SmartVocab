import unittest
from hamcrest import *
from engine.domain.distractor_selection import read_file_ordered_by_frequency,read_file_ordered_by_alphabet
from engine.domain.distractor_selection import get_word_frequency
class TestDistractorSelection(unittest.TestCase):

    def test_read_file_by_frequency(self):
        expected_res=('6187267', 'the', 'det')
        res=next(read_file_ordered_by_frequency())
        self.assertEqual(expected_res,res)

    def test_read_file_by_alphabet(self):
        expected_res=('2186369', 'a', 'det')
        res=next(read_file_ordered_by_alphabet())
        self.assertEqual(expected_res,res)

    def test_get_word_frequency(self):
        expected_res = 30454
        res=get_word_frequency('able','a')
        self.assertEqual(expected_res, res)
        expected_res1 = 0
        res1 = get_word_frequency('vishwas', 'a')
        self.assertEqual(expected_res1, res1)

    def test_getwordfrequency2(self):
        # Works with part of speech info
        self.assertIsInstance(get_word_frequency("rage", "n"), int)
        self.assertIsInstance(get_word_frequency("rage", "v"), int)





