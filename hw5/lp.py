#!/usr/bin/env python3

import numpy as np
import numpy.ma as ma
from itertools import count

np.set_printoptions(precision=3, suppress=True)

def simplex(f, A, b, zo=0):
    """
    solves a linear programming problem via simplex method
    input is the system f, A, b in canonical form.
    
    i.e. minimize (f^T)x subject to Ax=b

    This is immediately converted into the tableau (size M+1 by N+1)

                    | ^  
            A       | b
    ________________|___
        <-  f ->    | zo

    
    returns the final solution table T (see above)
    as well as the solution x that minimizes (f^t)x
    """
    # make sure these are the correct data type (otherwise pivoting is bad) 
    f = f.astype('f')
    A = A.astype('f')
    b = b.astype('f')
    print('testing canonicality')
    print(is_canonical(A))
    
    # MAKE INITIAL TABLEAU
    T = np.vstack((A, f))
    _b = np.vstack((b.reshape(-1,1), np.array(zo, dtype='f')))
    T = np.hstack((T, _b))

    for it in count(1):
        # this may seem weird, but now these are linked to T
        f = T[-1,:-1]
        b = T[:-1,-1]
        z0 = T[-1,-1]
        A = T[:-1,:-1]

        # if all c_i nonnegative
        if all(f >= 0):
            print("solution found in {} pivots".format(it-1))
            break
        else:
            print('no solution yet...')
            print('- '*20)


        # test theorem 2
        for s, c in enumerate(f):
            # if there exists a negative c_s
            if c < 0:
                # where a_{is} negative for all i 
                if (A[:,s] < 0).all():
                    print(T)
                    raise Exception("objective function is unbounded below by theorem 2")
        else:
            # step two complete, continue
            print("boundedness check complete, continuing")
        
        # find the smallest magnitude negative entry
        s = ma.masked_where(f >= 0, f).argmax()
        print('pivoting in column {}'.format(s))  
        
        # step 3.2 find row r that has the min{b[i] / a[i,s] : a[i,s] > 0}
        # note that argmin will print out lowest index if there is a tie
        _m = ma.masked_where(A[:,s] < 0, A[:,s])
        r = (b / _m).argmin()
        print('pivoting in row {}'.format(s))
        
        print('pivoting...')
        T[r] = T[r] / T[r,s]
 
        for i in range(T.shape[0]):
            if i == r:
                continue
            else:
                T[i] = T[i] - T[i,s]*T[r]
        print("after pivot #{}".format(it))
        print(T)
    
    # get basic variables from table
    x = basic_variables(T)
    # and the b values
    b = T[:-1, -1]

    # now set each basic_variable to the b_i value in the corresponding column
    B = b * np.eye(x.size, b.size) # basically just for broadcasting
    x = (B.T * x).sum(axis=0) # wow this got matlabby
    return T, x

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
            # this column of eye(M) appears more than once
            return False
        else:
            # x_k is a basic variable and nonzero in row m
            k = test.index(1)
        print("basic variable x_{} in row {}".format(k,m))

    return True

def basic_variables(T):
    """ 
    finds the basic variables from the simplex tableau X
    returns a 1D vector of each variable x_i where x_i == 1 if it is a basic
    variable, zero for nonbasic variables
    """

    # similar to the canonicality test
    
    M = T.shape[0] # number of rows
    E = np.eye(M)
    
    bv = np.zeros_like(T[-1,:-1])

    for m in range(M-1):
        # find each column like [0 ... 0 1 0 ... 0] in table (excl. constants)
        test = [all(E[m] == col) for col in T[:,:-1].T]
        if sum(test) != 1:
            # there are more than 1 basic variables in one row!
            raise Exception("system isn't in canonical form")
        else:
            # x_k is a basic variable and nonzero in row m
            k = test.index(1) # which row the 1 is in

            bv[k] = 1
    return bv
