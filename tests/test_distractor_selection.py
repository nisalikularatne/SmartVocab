import unittest
from hamcrest import *
from engine.domain.distractor_selection import read_file_ordered_by_frequency
path = 'C:\\Users\\Nisali Kularatne\\Documents\\final year project\\resources\\wordlist_byalphabets'
class TestDistractorSelection(unittest.TestCase):

    def test_read_file_by_frequency(self):
        expected_res=('2186369', 'a', 'det')
        res=next(read_file_ordered_by_frequency())
        self.assertEqual(expected_res,res)

