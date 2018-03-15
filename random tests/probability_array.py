import numpy as np
import math
probability=[]
theta = 1
response_vector=np.array([0,1,1,1])
difficulty_vector=np.array([-1,0,1,1])
discrimation_vector=np.array([1,1,1,1])

def calculate_probability_for_item(theta,difficulty,discrimination):
    e_to_the_power_calculations = -discrimination*(theta - difficulty)
    full_e_variable = math.exp(e_to_the_power_calculations)
    probablity_of_thetha = 1 + full_e_variable
    final_probability = 1 / probablity_of_thetha
    print("probabilities",final_probability)
    return final_probability

def get_probability_vector():

    for i in range(0,len(difficulty_vector)):
      probability.append(calculate_probability_for_item(theta,difficulty_vector[i],discrimation_vector[i]))
    return probability


def get_new_theta_value(theta,probability_vector,response_vector):
    summation_equation=0.0
    summation_denominator=0.0
    for i in range(0, len(response_vector)):
      summation_equation= summation_equation+(discrimation_vector[i]*(response_vector[i]-probability_vector[i]))
      print('summation equation',summation_equation)
      summation_denominator=summation_denominator+((discrimation_vector[i]*discrimation_vector[i])*(probability_vector[i]*(1-probability_vector[i])))
      print('denominator', summation_denominator)
      division=summation_equation/summation_denominator
    new_theta=theta+ division
    print('division',division)
    return new_theta
def convertRange( value, r1, r2 ) :
    return ( value - r1[ 0 ] ) * ( r2[ 1 ] - r2[ 0 ] ) / ( r1[ 1 ] - r1[ 0 ] ) + r2[ 0 ]



if __name__ == "__main__":
    print("Probablity",calculate_probability_for_item(-1,-1,1))
    print('New theta value')
    w=get_probability_vector()
    print(w)
    q=get_new_theta_value(theta,w,response_vector)
    print('convert range',convertRange(3.5, [ -3.2, 2.5 ], [ -1, 1 ]))
    print(q)



