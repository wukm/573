#!/usr/bin/env python3

"""
Hw#1 PROBLEM 4b
Solving Ax=b via the conjugate gradient method where A
is the hilbert matrix
"""

from conjugate_gradient import conjugate_gradient
import numpy as np
from scipy.linalg import norm

def hilbert_matrix(n):
    """
    returns an nXn hilbert matrix. made from a generator for fun.
    """

    h = np.fromiter((i+j-1 for j in range(1,n+1) for i in range(1,n+1)), np.float,
            count=n*n)
    h = 1 / h
    return h.reshape((n,n))

if __name__ == "__main__":
    
    n = 150
    ε = 10e-12 
    # A, b given by problem spec 
    A = hilbert_matrix(n)
    b = A.sum(axis=1).reshape((-1,1)) / 3
    print("running CG on a {}-by-{} Hilbert matrix with tolerance {}".format(
                n, n, ε))
    x = conjugate_gradient(A,b, tol=ε)
    if x.size < 20:
        print("x =\n", x.T)
    else:
        print("x = (output suppressed)")
    
    x_real = (1/3)* np.ones_like(b)
    error = norm(x - x_real)
    print("|| x - x* || = ", error)

# vim: ts=8 et sw=4 sts=4
