import numpy as np
import scipy as spy
from scipy.sparse import csc_matrix
import matplotlib.pyplot as plt
import time


m = 512
n = 1024


u= spy.sparse.rand(n,1,density=0.1,format='csc',dtype=None)
u1 = u.nonzero()
row = u1[0]
col = u1[1]
data = np.random.randn(int(0.1*n))
u = csc_matrix((data, (row, col)), shape=(n,1)).toarray() 

a = np.random.randn(512,1024)
b = np.dot(a,u)
v = 1e-3

def f(x0): 
    return 1/2*np.dot((np.dot(a,x0)-b).T,np.dot(a,x0)-b)+v*sum(abs(x0))

y = []
time1 = []
start = time.process_time()

x0 = np.zeros((n,1))


t = 1/np.max(np.linalg.eigvals(np.dot(a.T,a))).real

for i in range(1000):
    
    y.append(f(x0))
    
    x1 = x0-t*np.dot(a.T,np.dot(a,x0)-b)
    
    x1[x1 >= t*v] = x1[x1 >= t*v] - t*v
    x1[np.abs(x1) < t*v] = 0
    x1[x1 <= -t*v] = x1[x1 <= -t*v] + t*v
    
    x0 = x1
    end = time.process_time()
    time1.append(end)

y = np.array(y).reshape((1000,1))    

plt.plot(y)
plt.show()

time1 = np.array(time1)
time1 = time1 - start
time2 = time1[np.where(y - y[999] < 10e-4)[0][0]]

print(time2)