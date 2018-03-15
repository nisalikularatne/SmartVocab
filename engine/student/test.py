import numpy as np
import math
theta=0.3

difficulty=0.2
response_vector=[1,1,1,0,0]
e_to_the_power_calculations=-1.7*(theta-difficulty)
full_e_variable=math.exp(e_to_the_power_calculations)
probablity_of_thetha=1+full_e_variable
final_probability=1/probablity_of_thetha

'''Lets see if according to the given responses if theta increases or decreases'''
response_vector=np.array([1,1,1,0,0])
def calc_Summation1(response_vector):
    ans = 0.0
    for i in range(0, len(response_vector)):
        ans = ans -(response_vector[i]-final_probability)
    new_theta=theta+ans
    print(ans)
    return new_theta

print('new values',calc_Summation1(response_vector))
"""
w=4/5
print(w)
a=2-w
b=a-w
c=b-w
d=c-w
e=d-w
f=e-w

print(e,d,c,b,a,2)
"""
