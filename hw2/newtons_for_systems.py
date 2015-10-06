#!/usr/bin/env python3

"""
Math 573 Homework #2, Question 2(a)

Solve a symbolic(!?) non-linear system of equations
via Newton's method.

GENERAL NOTES:

*   since python is 0 indexed, so f_1 is actually accessed as F[0]
    internally. shouldn't really matter but hey

*   sympy.sympify uses eval() so santitize input

*   to evaluate a component F[i] for some particular \vec{x}, you can do the
    following:

    F[i].subs((x,xi) for x, xi in zip(X, (3,4,5)) # for example

    i.e. this will return the value of f_{i+1}(x) when x=(3,4,5).T
    
    this works for quick evaluation, but for any extended use, it's way more
    favorable to use sympy.lambdify(x, expr, "numpy"). see docs

*   note that all sympy expressions are immutable (like strings)

*   turn this into a class or sumit?
"""

import sympy
import numpy as np
from scipy.linalg import norm, solve, pinv
from numpy.linalg import cond

def parse_symbolic(F_strings, F_args, assert_real=False):
    """
    INPUT

    F_strings:  an iterable of n strings, each of which refers to up to
    n symbolic variables in an internally consistent way.
    F_args: a (comma or whitespace) delimited string containing the n symbolic
    variables used in F_strings
    assert_real: F_args refer to real numbers. If not, no such assumption is
                 made (note: deprecated)

    OUTPUT
    
    F    A sympy.Matrix of shape (n,1) whose elements are the symbolic equations
         f1, f2, ... fn
    X    A tuple of sympy symbol objects representing the variables in F

    NOTES:
    
    *   you should actually bundle all of the parsing and such in a separate
        function, like "get_shit()" and "build_jacobian()" etc.

    *   symbolic input kinda works as expected, i guess? check for bugs. i know
        for a fact that curly brackets '{','}', etc. are a no-go, so it's not
        *exactly* latex syntax.

    """

    # each arg can be accessed now as X[i] in the order listed
    if not assert_real:
        X = sympy.symbols(F_args)
    else:
        X = sympy.symbols(F_args, real=True)

    # similarly, access each component function as F[i] 
    F = tuple((sympy.sympify(fi) for fi in F_strings))
    
    # now make it a matrix
    F = sympy.Matrix(F)

    return F, X

def solve_nonlinear_system(F_strings, F_args, x0, M=100, ε=10e-6,
        test_condition_number=False, x_convergence=False):
    """

    INPUT
    -----

    F_strings:  an iterable of n strings, each of which refers to up to
    n symbolic variables in an internally consistent way.

    F_args: a (comma or whitespace) delimited string containing the n symbolic
    variables used in F_strings

    x0: initial "guess" solution. an nx1 np.array

    M: max iterations

    ε: convergence tolerance
    
    optional arguments:

    x_convergence:  if True, convergerce will be tested on size of Δx rather
                    than size of F(x). Not useful; defaults to False
    
    test_condition_number: at each iteration, the jacobian's condition
                           number is evaluated to test for singularity.
                           Expensive; defaults to False

    OUTPUT
    ------
    
    a solution x
    """
    

    F, X = parse_symbolic(F_strings, F_args)
    J = F.jacobian(X)

    # see lambdify docstring; lambda will return np.array not np.matrix
    mat2array = [{'ImmutableMatrix': np.array}, 'numpy']

    # args to these must be 1D, so flatten and/or expand
    f = sympy.lambdify(X, F, modules=mat2array)
    j = sympy.lambdify(X, J, modules=mat2array)

    # set x to initial guess
    x = x0
    Δx = None # declare (if we're testing convergence in x)

    #norms = list()
    for i in range(M):
        
        fi = f(*x.flatten())
        #norms.append(norm(fi))
        if x_convergence and Δx is not None:
            if norm(Δx) < ε:
                print("tolerance reached in {} iterations!".format(i))
                break 
        else:
            if norm(fi) < ε:
                print("tolerance reached in {} iterations!".format(i))
                break
        ji = j(*x.flatten())
        
        # check condition number of ji and error if >10e6 or something
        if test_condition_number:
            if cond(ji) > 10e6:
                raise Exception("jacobian looks singular. aborting.")
            
        # use pseudoinverse for nonsquare systems
        if ji.shape[0] == ji.shape[1]: 
            Δx = solve(ji, -fi)
        else:
            Δx = -pinv(ji).dot(fi) 

        x = x + Δx

        print('_'*40, 'i={}:'.format(i+1))
        print("x =", x.flatten())
        print("F[x] =", fi.flatten())
        print("||F[x]|| =", norm(fi))
        #print("J[x] =\n", ji)
    else:
        print("could not find solution within {} iterations".format(M))


    
    return x

if __name__ == "__main__":

    case_one = ["z^2 + 1 - x*y",
                "x^2 + 2 - x*y*z - y^2",
                "exp(y) + 3 - exp(x) - z"
            ]

    args = "x,y,z"

    x0 = np.array([[1,1,1]]).T

    x_sol = solve_nonlinear_system(case_one, args, x0, ε=10e-6)
    print("x_sol =", x_sol.flatten())

