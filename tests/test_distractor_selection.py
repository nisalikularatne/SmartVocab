import unittest
from hamcrest import *
from engine.domain.distractor_selection import read_file_ordered_by_frequency,read_file_ordered_by_alphabet
class TestDistractorSelection(unittest.TestCase):

    def test_read_file_by_frequency(self):
        expected_res=('6187267', 'the', 'det')
        res=next(read_file_ordered_by_frequency())
        self.assertEqual(expected_res,res)

    def test_read_file_by_alphabet(self):
        expected_res=('2186369', 'a', 'det')
        res=next(read_file_ordered_by_alphabet())
        self.assertEqual(expected_res,res)



