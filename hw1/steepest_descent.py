#!/usr/bin/env python3

from util import spd
import numpy as np
from numpy.linalg import norm

def steepest_descent(A, b, x_init=None, M=10000, ε=10e-10, check_spd=True):        
    """
    finds a solution to the linear system Ax = b via steepest descent

    inputs:
        A is an nxn SPD matrix
        b is an n x 1 vector
        x0 is the initial estimate vector (nx1) (default is zero vector)
        M is max number of iterations (default 10000)
        ε is machine precision (default .0001)
        if check_spd, the program will fail in the event that the system is not
        spd

    note:
    -   uses size of || x_{k+1} - x_k ||_2^2 as stopping condition 
    -   please don't break this code with weird stuff (more testing needed)
    """

    if not spd(A):
        raise Exception("""
                A must be positive definite!
                pass check_spd=False to bypass""")

    # initialize x_0 as zero vector if one wasn't provided
    if x_init is None:
        x = np.zeros_like(b, np.float)
    else:
        x = x_init

    for k in range(M):
        v = b - A.dot(x)
        u = A.dot(v)
        t = v.T.dot(v) / u.T.dot(v)
        x, x_old = ( x + t*v , x)
        
        x_change = norm(x-x_old) 
        
        if x_change < ε:
            break
        #print(locals())    
        #input('...')

    else:
        print('warning: exhausted max iterations (M={})'.format(M))
  
    summary = "terminated in {} iterations (out of M={}) with tolerance ε={}".format(k+1, M, ε)
    
    print(summary)
    return x
