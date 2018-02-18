import random


from engine.domain import distractor_selection
from engine.domain.word_cefr_details import word_list, find_cefr
from collections import namedtuple
from engine.domain.WordModel import Word
import ast
import os
import inspect
filepath = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../resources/")))
from nltk.corpus import wordnet as wn
import json
def read_cefr_file(filename):
    with open(filename) as f:
        for line in f.readlines():
            l = line.strip().split()
            word = l[0]
            cefr = l[-1]

            yield word, cefr

vocab_model={}
vocab_list = []
sense_list=[]
def get_domain_data():
    global final_dict
    final_dict = {}
    for filename in ["/a1", "/a2", "/b1", "/b2", "/c1", "/c2"]:
        for (word, cefr) in (read_cefr_file(filepath + filename + "-vocab.txt")):

            vocab_model[word] = {}
            vocab_model[word]['cefr'] = cefr
            vocab_model[word]['senses'] = []
            for sense in Word(word).senses:
                a = {'id': sense.id, 'name': sense.original, 'definition': sense.definition, 'pos': sense.pos}
                vocab_model[word]['senses'].append(a)
            final_dict = vocab_model.copy()


    with open('data.json', 'w') as f:
                  json.dump(final_dict, f)

def read_from_domain_json():
    filename = filepath + '/data.json'
    if filename:
        with open(filename, 'r') as f:
            datastore = json.load(f)
    return datastore

if __name__ == "__main__":

  get_domain_data()