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
import fileinput
def remove_extra_lines():
    with open(filepath + "/c2" + "-vocab.txt") as infile, open('output.txt', 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)
def add_difficulty():

    for line in fileinput.FileInput(filepath + "/c2" + "-vocab.txt", inplace=1):
        line = line.replace("C2", "2.0")
        print(line)
if __name__ == "__main__":
    print(-2.0, -1.2000000000000002 ,-0.40000000000000013 ,0.3999999999999999, 1.2 ,2)
    add_difficulty()
    remove_extra_lines()




