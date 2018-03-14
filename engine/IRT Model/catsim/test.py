import numpy as np
a = np.array([[1,2,3], [4,5,6]])
print(np.reshape(a, (3,-1)))

print(np.reshape(a, 6, order='F'))
print(a)
