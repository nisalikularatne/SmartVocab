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
import csv
# generating an item bank
print('Generating item bank...')
bank_size = 5
g=generate_item_bank(5,'1PL')
print(g)
items=a = np.array([[ 1.        , -0.7 , 0.   ,       1.        ], #EASY
 [ 1.      ,   -0.3 ,  0.    ,      1.        ],#EASY
 [ 1.       ,  -1.30694568 , 0.,          1.        ],#EASY
 [ 1.         , 2.53300676 , 0.   ,       1.        ],#HARD
 [ 1.          ,1  ,0. ,         1.        ]])#HARD
print(items)
data = numpy.loadtxt('nisali.txt')
print("data in file as numpy array is ",data)

# creating dummy response patterns and selecting item indexes to pass as administered items
print('Creating dummy examinee data...')
responses = [True,True,False,False]
administered_items = [0,1,2,3]

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
est_theta = initializer.initialize()
print('Examinee initial proficiency:', 1)

# get an estimated theta, given the answers to the dummy items
new_theta = estimator.estimate(items=data, administered_items=administered_items, response_vector=responses, est_theta=est_theta)
print('Estimated proficiency, given answered items:', new_theta)
# get the index of the next item to be administered to the current examinee, given the answers they have already given to the previous dummy items
item_index = selector.select(items=items, administered_items=administered_items, est_theta=est_theta)
print('Next item to be administered:', item_index)
# get a boolean value pointing out whether the test should stop
_stop = stopper.stop(administered_items=items[administered_items], theta=est_theta)
print('Should the test be stopped:', _stop)