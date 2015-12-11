#!/usr/bin/env python3

import numpy as np

def simplex(f, A, b):
    """
    solves a linear programming problem via simplex method
    input is the system f, A, b in canonical form.
    """

    # assert is_canonical(A)
    
    # if all c_i nonnegative
    if (f >= 0).all():
        print("solution found!")
        # ...

    # test theorem 2
    for s, c in enumerate(f):
        # if there exists a negative c_s
        if c < 0:
            # where a_{is} negative for all i 
            if (A[:,s] < 0).all():
                # output tableau?
                raise Exception("objective function is unbounded below by theorem 2")
    else:
        # step two complete, continue
        print("boundedness check complete, continuing")
    

    # blah

def is_canonical(A):
    """
    tests if a system of equations Ax = b is in canonical form

    INPUT
    -----
    A:  an np.array with shape (M,N) with M >= N

    OUTPUT
    ------
    boolean

    Notes:
        
        a matrix A is in canonical form if there are exactly M column that are
        all zero entries except for one place where it's 1.
        furthermore, each 1 entry is unique.
        
        To say this in a different way, each column of the M-by-M identity matrix
        appears *exactly once* as a column of the matrix A in the
        linear system of equations Ax = b

        For example, the matrix
                   
            array([[0, 1, 4, 5, 7, 0],
                   [1, 0, 0, 3, 1, 0],
                   [0, 0, 0, 0, 0, 1]])

        is in canonical form, whereas 


            array([[0, 4, 5, 6, 7, 0],
                   [1, 0, 3, 4, 1, 0],
                   [0, 0, 0, 0, 0, 1]])

        is not, and 

            array([[0, 1, 1, 5, 7, 0],
                   [1, 0, 0, 3, 1, 0],
                   [0, 0, 0, 0, 0, 1]])
        
        is not.
    """
    M, N = A.shape # A is an M by N matrix
    
    E = np.eye(M)

    for m in range(M):
        # this tests if each column is elementwise equal to the mth row/column
        # of E, i.e. all zeros except for a one in the mth position
        test = [all(E[m] == col) for col in A.T]

        # if this fails then there are two basic variables in some row
        if sum(test) != 1:
            return False
        else:
            k = test.index(1) # x_k is a basic variable and nonzero in row m
        print("basic variable x_{} in row {}".format(k,m))

    return True

def is_standard_form(f, A, b):
    
    pass

if __name__ == "__main__":

     import numpy as np
     A = np.array([[0, 1, 4, 5, 6, 7, 0],
                   [1, 0, 0, 3, 4, 1, 0],
                   [0, 0, 0, 0, 0, 0, 1]])
