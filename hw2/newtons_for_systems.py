#!/usr/bin/env python3

"""
Math 573 Homework #2, Question 2(a)

Solve a symbolic(!?) non-linear system of equations
via Newton's method.

all right, buckle the fuck up

GENERAL NOTES:

*   since python is 0 indexed, so f_1 is actually accessed as F[0]
    internally. shouldn't really matter but hey

*   holy shit, error handling, what is all this nonsense

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
from scipy.linalg import norm, solve

def parse_symbolic(F_strings, F_args):
    """
    INPUT

    F_strings:  an iterable of n strings, each of which refers to up to
    n symbolic variables in an internally consistent way.
    F_args: a (comma or whitespace) delimited string containing the n symbolic
    variables used in F_strings

    OUTPUT
    
    the system F which is totally cool

    NOTES:
    
    *   you should actually bundle all of the parsing and such in a separate
        function, like "get_shit()" and "build_jacobian()" etc.

    *   symbolic input kinda works as expected, i guess? check for bugs. i know
        for a fact that curly brackets '{','}', etc. are a no-go, so it's not
        *exactly* latex syntax.

    """

    # each arg can be accessed now as X[i] in the order listed
    X = sympy.symbols(F_args)

    # similarly, access each component function as F[i] 
    F = tuple((sympy.sympify(fi) for fi in F_strings))
    
    # now make it a matrix
    F = sympy.Matrix(F)

    return F, X

def _lambdify_matrix(A):
    """
    a symbolic "matrixoid" A is turned into a function such that
    λ_A(x) = A at a particular X, a numpy array

    idk. a magic method
    """
    pass


if __name__ == "__main__":
    
    max_iterations = 100
    tol = 10e-6
    
    case_one = ["z^2 + 1 - x*y",
                "x^2 + 2 - x*y*z + y^2",
                "exp(y) + 3 - exp(x) + z"
            ]

    args = "x,y,z"

    #inital guess
    x = np.array([[1,1,1]]).T   # this shape is annoying to work with

    

    F, X = parse_symbolic(case_one, args)
    J = F.jacobian(X)

    # see lambdify docstring; lambda will return np.array not np.matrix
    mat2array = [{'ImmutableMatrix': np.array}, 'numpy']

    # args to these must be 1D, so flatten and/or expand
    f = sympy.lambdify(X, F, modules=mat2array)
    j = sympy.lambdify(X, J, modules=mat2array)

    for i in range(max_iterations):
        
        fi = f(*x.flatten())
        if norm(fi) < tol:
            print("tolerance reached in {} iterations!".format(i))
            break
        ji = j(*x.flatten())

        # check condition number of ji and error if >10e6 or something
        
        if False:
            raise Exception("J(x^{}) looks singular, aborting".format(i))


        # should maybe use a faster method of solving
        Δx = solve(ji, -fi)

        x = x + Δx
        print('iteration {}:'.format(i))
        print("x =", x.flatten())
        print("F[x] =", fi.flatten())
        print("J[x] =\n", ji)
        print('\n')
