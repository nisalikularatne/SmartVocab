"""
import os
import inspect
filepath = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../resources/")))
filename = filepath + '/data.json'
from engine.domain.Domain_Model import DomainModel
if __name__ == "__main__":
    d=DomainModel()
    words=['actor','on','slender','container']
    for word in words:
      if(d[word].item_no==5628):
          print(word)
"""
 # this function generates an item bank, in case the user cannot provide one
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
 # generating an item bank
print('Generating item bank...')
bank_size = 5000
items = items = numpy.loadtxt('nisali.txt')

# creating dummy response patterns and selecting item indexes to pass as administered items
print('Creating dummy examinee data...')
responses = [True, True, True, False, True, True, True, True, True, True]
administered_items = [3, 12, 7, 16, 2, 11, 6, 15, 1, 10]

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
new_theta = estimator.estimate(items=items, administered_items=administered_items, response_vector=responses, est_theta=est_theta)
print('Estimated proficiency, given answered items:', new_theta)

# get the index of the next item to be administered to the current examinee, given the answers they have already given to the previous dummy items
item_index = selector.select(items=items, administered_items=administered_items, est_theta=est_theta)
print('Next item to be administered:', item_index)

# get a boolean value pointing out whether the test should stop
_stop = stopper.stop(administered_items=items[administered_items], theta=est_theta)
print('Should the test be stopped:', _stop)