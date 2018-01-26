import unittest
from hamcrest import *
from engine.domain.WordModel import Word
class TestWordModel(unittest.TestCase):
    def test_definitions(self):
        oldword=Word("actor").definition
        newword=str(oldword)
        print(newword)
        assert_that(newword,any_of('a person who acts and gets things done', 'a theatrical performer'))

