#!/usr/bin/env python3

"""
This is an implementation of the (practical) conjugate gradient
algorithm for solving Ax=b presented in lecture, also used for
HW1, Problem 4

"""
import numpy as np
from scipy import linalg
from scipy.linalg import norm
from numpy import vdot
from util import spd, symmetric

def conjugate_gradient(A, b, M=10000, x=None, tol=10e-10, check_spd=True):
    """
    conjugate gradient solution of Ax = b

    INPUTS
    A:  a nxn array representing a symmetric positive definite matrix
    b:  a nx1 array 
    M:  max iterations to run (see below) 
    x:  a starting guess (default is zero vector)
    tol:    tolerance (used for stopping condition)
    check_spd:  pre-check that A is in fact symmetric positive definite

    OUTPUT
    x:      the approximate solution to the system Ax=b

    NOTES:

    -   M should be superfluous; theoretically this method with terminate
    successfuly in n == b.size iterations, provided A is s.p.d. No such
    guarantee is made if A is not s.p.d.
    -   Similarly, a starting guess of x=0 is typically desired, as it minimizes
    computational error.
    -   If A is not symmetric positive definite and check_spd==True, then a
        generic Exception will be thrown, terminating execution.
    """
   
    assert A.shape[1] == b.shape[0], "system doesn't match"
    
    if not spd(A):
        raise Exception("""
            A is not positive definite; aborting.
            pass check_false=False to bypass""")

    # set an initial guess or check inputted
    if x is None:
        x = np.zeros_like(b) # creates an nx1 zero vector
    else:
        assert x.shape == b.shape, "system doesn't match"

    r = b - A.dot(x)
    c = vdot(r,r)
    v = r

    for i in range(M):

        if np.sqrt(c) < tol:
            print("tolerance reached!")
            break

        u = A.dot(v)
        alpha = c / (u.T.dot(v))
        x = x + alpha*v
        r = r - alpha*u
        d = vdot(r,r)
        
        if np.sqrt(d) < tol:
            print("tolerance reached!")
            break
        else:
            v = r + (d/c)*v
            c = d

    else:
        print("max ({}) iterations exhausted".format(i+1))
    
    print("finished in {} iterations".format(i))

    return x

if __name__ == "__main__":
    from util import random_spd

    N = 100
    A = random_spd(N)
    b = np.random.random(N).reshape((-1,1))

    x = conjugate_gradient(A,b, tol=10e-10)

    # show x vector directly unless it's big
    if N <= 10:
        print(x.T)

    # show the size of the residue (well, show *something*) 
    print("|| b - Ax || = ", norm(b-A.dot(x)))

