#!/usr/bin/env python3

import numpy as np
from numpy.linalg import solve

def poly_lsq(data, n):
    """
    returns the coefficients of the degree n poly
    """
    # parse input 
    data = np.array(data)
    
    # make sure data is 2D & get into desired shape
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
     
    #print('normal\t', "_"*30)
    #print('X=\n', X)

    M = X.T @ X
    b = X.T @ y

    #print('y=',y)
    #print('M=\n',M)
    #print('b=\n',b)

    a = solve(M,b) # G.E. or whatever
    a = a.flatten() # i don't need the shape anymore, want easy iteration
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

    


