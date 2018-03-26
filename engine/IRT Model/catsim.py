from catsim.cat import generate_item_bank
from catsim.initialization import RandomInitializer
from catsim.selection import MaxInfoSelector,LinearSelector
from catsim.estimation import HillClimbingEstimator
from catsim.stopping import MaxItemStopper
from catsim.simulation import Simulator
from catsim.plot import *
bank_size = 5000
items = numpy.loadtxt('nisali.txt')
print('items',items[0][1])
responses = [True, True, False, False,True,True,False,True,True]
administered_items = [0, 1, 2, 3,4,5,6,7,8,9]
initializer = RandomInitializer()
selector = MaxInfoSelector()
estimator = HillClimbingEstimator()
stopper = MaxItemStopper(5)
est_theta = initializer.initialize()
item_index = selector.select(items=items,
administered_items=administered_items,
est_theta=est_theta)
new_theta = estimator.estimate(items=items,
administered_items=administered_items,
response_vector=responses, est_theta=est_theta)
_stop = stopper.stop(administered_items=items[administered_items],
theta=est_theta)
s = Simulator(items, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
s.simulate(RandomInitializer(), LinearSelector([1,2,3,4,5,6,7,8,9,10]),
HillClimbingEstimator(), MaxItemStopper(7))
print(s.response_vectors)
print(s.administered_items)

