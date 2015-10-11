#!/usr/bin/env python3

"""

w is the intermediate matrix

1   x1  x1^2    ... x1^n
1   x2  x2^2    ... x2^n
... ... ...     ... ...
1   xm  xm^2    ... xm^n

"""
import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt

# set up least squares problem

# inputs

# Table 1: Data for Problem 1.
TABLE_1 = [[  1.0,    1.1,    1.3,    1.5],
           [ 1.84,   1.96,   2.21,   2.45]]

N = 2 # degree of least-squares polynomial to construct

# start of function

data = np.array(TABLE_1)
n = N

# parse input
try:
    data = data.reshape((2,-1))
except ValueError:
    raise Exception("Sorry, can only deal with 2D data")

# conveniences
m = data.shape[-1] # number of data points

# ugh, get each row as an mx1
x = data[0].reshape((-1,1))
y = data[1].reshape((-1,1))

# build xpowers matrix
w = np.empty((m,n+1), dtype=data.dtype)
for j in range(n+1):
    w[:,j] = (x**j).flatten() # ugh, x can't be nx1 here...

# broadcasting
b = y*w 

# b as described for problem!
b = b.T.sum(axis=1, keepdims=True) # or b.sum(axis=0).reshape(-1,1) 

# build A
A = np.empty((n+1,n+1), dtype=data.dtype)
for i in range(n+1):
    A[i] = (w*x**i).sum(axis=0) 

# approximating coefficients
a = solve(A,b)
a = a.flatten() # i don't need the shape anymore, want easy iteration
# make a function
p = lambda x: sum(ai*(x**i) for i, ai in enumerate(a))
# error
lsq_error = ((p(x) - y)**2).sum()

print("A=\n", A)
print("b=\n", b)
print("solution:\n", a)

print("least squared error:", lsq_error)

X = np.linspace(0,2,100) # fix bounds to match size of data

# actually do this iteratively because you don't want to create a huge matrix
#Y = [sum((ai*(x**i) for i, ai in enumerate(a))) for x in X]
#Y = [p(x) for x in X]
Y = p(X)    # this amazingly works!

plt.scatter(x, y)
plt.plot(X,Y)


