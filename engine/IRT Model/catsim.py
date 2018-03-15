from catsim.cat import generate_item_bank
# simulation package contains the Simulator and all abstract classes
from catsim.simulation import *
# initialization package contains different initial proficiency estimation strategies
from catsim.initialization import *
# selection package contains different item selection strategies
from catsim.selection import *
# estimation package contains different proficiency estimation methods
from catsim.estimation import *
# stopping package contains different stopping criteria for the CAT
from catsim.stopping import *
import catsim.plot as catplot
import numpy as np
from engine.instructor.Quiz_Engine import Instructor as q
import csv
import os
import inspect
filepath = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../resources/")))

# generating an item bank
print('Generating item bank...')
bank_size = 5

data = numpy.loadtxt(filepath+'/difficulties.txt')


# creating dummy response patterns and selecting item indexes to pass as administered items
print('Creating dummy examinee data...')
responses = [True,True,True]
filename = filepath + '/item_list.txt'
administered_items = [int(line.strip()) for line in open(filename, 'r')]
print('Creating simulation components...')
# create a random proficiency initializer
initializer = RandomInitializer()
# create a maximum information item selector
selector = MaxInfoSelector()
# create a hill climbing proficiency estimator
estimator = HillClimbingEstimator()
 # create a stopping criterion that will make tests stop after 20 items
stopper = MaxItemStopper(20)
# manually initialize an examinee's proficiency as a float variable
est_theta = -1
print('Examinee initial proficiency:', est_theta)

# get an estimated theta, given the answers to the dummy items
new_theta = estimator.estimate(items=data, administered_items=administered_items, response_vector=responses, est_theta=est_theta)
print('Estimated proficiency, given answered items:', new_theta)
item_index = selector.select(items=data, administered_items=administered_items, est_theta=est_theta)
print('Next item to be administered:', item_index)
if __name__ == "__main__":
 print("catsim")