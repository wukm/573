#!/usr/bin/env python3

import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt

# set up least squares problem



def polynomial_lsq(data, n):

    # parse input 
    data = np.array(data)
    try:
        data = data.reshape((-1,2))
    except ValueError:
        raise Exception("Sorry, can only deal with 2D data right now")

    # conveniences
    m = data.shape[0] # number of data points
    y = data[:,1] 

    # add a ones column to data
    X = np.concatenate((np.ones((m,1)), data), axis=1)
    
    M t X.T @ X
    b = X.T @ y

    a = solve(M,b) # G.E. or whatever
    a = a.flatten() # i don't need the shape anymore, want easy iteration
    # make a function
    #p = lambda x: sum(ai*(x**i) for i, ai in enumerate(a))
    # error
    #lsq_error = ((p(x) - y)**2).sum()
    
    return a

def log_fit(data):
    """
    returns a,b corresponding to the form y = bx^a
    """

    data = np.array(data)
    data = np.log(data)

    a0, a1 = polynomial_lsq(data, 2)
    
    a = a1
    b = np.exp(a0) 

    return a, b

if __name__ == "__main__":
    
    # Table 1: Data for Problem 1.
    TABLE_1 = [[  1.0,    1.1,    1.3,    1.5],
               [ 1.84,   1.96,   2.21,   2.45]]

    N = 2 # degree of least-squares polynomial to construct
    #print("A=\n", A)
    #print("b=\n", b)
    #print("solution:\n", a)
       
    #print("least squared error:", lsq_error)
       
    X = np.linspace(0,2,100) # fix bounds to match size of data
       
    Y = p(X)    # this amazingly works!
       
    plt.scatter(x, y)
    plt.plot(X,Y)


