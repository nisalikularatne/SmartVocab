import unittest
from engine.domain.Domain_Model import DomainModel


d=DomainModel()
class MyTest(unittest.TestCase):
   def test_itemno(self):
      about_itemno=d['about'].item_no
      self.assertNotEqual(about_itemno, 5678)
      self.assertEqual(about_itemno, 1)
      self.assertIsInstance(about_itemno,int)
   def test_sense(self):
       senses=d['eventual'].senses
       self.assertIsInstance(senses,object)
       self.assertNotIsInstance(senses,bytearray)

   def test_cefr(self):
       word=d['eventual'].cefr
       self.assertIsInstance(word, str)
       self.assertNotIsInstance(word, bytearray)
