import numpy as np
a = np.array([[1,2,7],[2,3,4]])
print(a)
print(a[[True,False]])
b = np.array([True, False])
print(a[~b])

c = np.array([1,2,3])
d = np.array([2,2,2])
print(c*d)
e = 0
print(e+0*np.log2(0))