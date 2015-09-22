#!/usr/bin/env python3

import numpy as np
from scipy import linalg

def as_row(v):
    """
    recast a 1D array as a row vector
    """
    if v.ndim == 2 and v.shape[1] == 1:
        return v
    elif v.ndim == 1:
        return v.reshape((-1,1)).T
    else:
        raise

def symmetric(A):
    """
    test an nxn matrix for symmetry
    """
    return (A == A.T).all()

def spd(A):
    """
    spd(A) -> True if A is a symmetric positive definite matrix

    constructs an upper triangular matrix from A and then checks that each
    diagonal element is greater than zero (this comes from the test that a
    matrix is SPD iff all principal leading minors are nonzero, and that these
    determinants will carry through to the diagonalization.

    alternative test is testing eigs(A) > 0 but this is much faster as it
    doesn't involve root-finding
    """
    # test symmetric first, as it's easier
    if not symmetric(A):
        return False
    

    t = linalg.triu(A)
    return (np.diag(t) > 0).all()

def random_spd(n, check_spd=False):
    """
    generate a random symmetric positive definite matrix of size (n,n)

    INPUT:
    n   - dimension of (square) matrix to construct
    check_spd   -   check spd within this function (defaults to false)
    """
    
    # n by n matrix with elements unif. between 0 and 1
    a = np.random.random((n,n))
    
    # make it symmetric
    a = a + a.T

    if check_spd and not spd(a):
        # force it to be diagonally dominant if it's not spd
        a += diag([n-1]*2)
    
        if not spd(a):
            Exception("random spd matrix generation failed :(")
    
    return a
