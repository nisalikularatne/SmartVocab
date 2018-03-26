import unittest
from hamcrest import *
import random
from engine.domain.WordModel import Word
class TestWordModel(unittest.TestCase):
    def test_definitions(self):
        oldword=Word("actor").definitions
        definition=random.choice(oldword)
        newword=str(definition)
        print(newword)
        assert_that(newword,any_of('a person who acts and gets things done', 'a theatrical performer'))

