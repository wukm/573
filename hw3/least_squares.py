#!/usr/bin/env python3

import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt

# set up least squares problem



def poly_lsq(data, n):
    """
    returns the coefficients of the degree n poly
    """
    # parse input 
    data = np.array(data)

    if 2 == data.shape[0]:
        data = data.T
    elif 2 == data.shape[1]:
        pass
    else:
        raise Exception("Sorry, can only deal with 2D data right now")

    # conveniences
    m = data.shape[0] # number of data points
    x = data[:,0].reshape((-1,1))
    y = data[:,1].reshape((-1,1))
    
    X = np.concatenate([x**i for i in range(n+1)], axis=1)
     
    print('normal\t', "_"*30)
    print('X=\n', X)

    M = X.T @ X
    b = X.T @ y

    print('y=',y)
    print('M=\n',M)
    print('b=\n',b)

    a = solve(M,b) # G.E. or whatever
    a = a.flatten() # i don't need the shape anymore, want easy iteration
    return a

def _alt_lsq(data, degree):
    """
    least squares interpolating of the 2D data
    with a polynomial of given degree

    returns the coefficients a_0 , ..., a_{n+1}
    """
    
    # make sure size is right first
    d = np.array(data).reshape((2,-1))

    # conveniences
    n, m = degree, d.shape[1]
    X, Y = d
    
    # initialize 
    M = np.empty((n+1,n+1))
    b = np.empty((n+1,1))

    # populate these in a boring way
    for i in range(n+1):
        M[i] = [sum(X**(i+j)) for j in range(n+1)]
        b[i] = sum(Y*X**i) 
    print("degree", degree, '\t'+'_'*30)  
    print('M=\n',M)
    print('b=\n',b)
    a = solve(M,b)
    
    return a

def exponential_lsq(data):
    """
    returns a,b corresponding to the form y = bx^a
    """

    data = np.array(data)
    data = np.log(data)

    a0, a1 = poly_lsq(data, 1)
    
    a = a1
    b = np.exp(a0) 

    return a, b

    


