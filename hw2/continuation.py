#!/usr/bin/env python3

"""
MATH 573 Homework #2, Question 3
Solution of a nonlinear system of equations via (Newton's) continuation
method.

GENERAL NOTES/TODO:

    *   many of the symbolic handling here is similar to the other algorithm
    used in this HW set, Newton's method. Presently, that code is duplicated
    here, although this should be refactored to common functions.

    *   there should be a way to either produce a solution in a conventional
    manner (floating point calculations within numpy) *or* to track each
    individual iteration symbolically (overhead and all).

    *   logging overhaul (as a matter of fact, a wrapper would be very helpful)

    *   should ideally turn such algorithms into a class, so that all parts of
    the problem are accessible after the loop exits. the end goal is to have a
    streamlined implementation for when the answer is desired as well as more
    verbose, "analyzeable" implementation (iterations are saved for graphing,
    etc, output can be pickled, etc).

"""

import sympy
import numpy as np
from newtons_for_systems import parse_symbolic
import os, sys

def cm_rk4(F_strings, F_args, x0, N, verbose=True):
    
    #you should really do this in a decorator
    if verbose:
        fs = sys.stdout # this is default for the print function
    else:
        fs = open(os.devnull, 'w') 

    F, X = parse_symbolic(F_strings, F_args)

    print("system parsed successfully...", file=fs)

    J = F.jacobian(X)   # symbolic jacobian matrix

    print("jacobian found", end=" ", file=fs) 

    Jinv = J.inv()  # calculate inverse (method can be specified)

    print("...and inverted!", end=" ", file=fs)
    

    #Jinv.simplify() # simplify symbolic expression (for logging)
                    # note that this occurs in place!

    #print("...and simplified!", end=" ", file=fs) 
    
    print("\n", file=fs)

    # get a value for F_0 = F(x0)
    F0 = F.subs(list(zip(X, x0)))

    print("initial system calculated", file=fs)

    # x`(λ) = [J(x(λ)]^(-1) * F0
    # this is an nx1 matrix that describes the set of differential equations
    #   dx_i / dλ = [x`(λ)]_i

    xpl = -Jinv.multiply(F0) # matmul syntax is different within sympy

    print("ODE system x`(λ) calculated", file=fs)
    print("...and simplified", file=fs)
    print("running RK4 with N={}".format(N), file=fs)

    # pass everything to RK4 (including verbosity setting) 
    x_sol = rk4(xpl, X, x0, N, verbose=verbose)
    
    # do you need to close /dev/null?
    if not verbose:
        try:
            fs.close()
        except:
            pass    # this is bad code

    return x_sol

def rk4(Φ, X, x0, N, verbose=True):
    """
    Runge-Kutta Method (Order 4)
    
    INPUT

    Φ   a symbolic vector (e.g. a matrix in sympy) whose components
        give the system of differential equations
    
                [ d(X[i]) / dλ ] = Φ[i]
    
    X   a list of symbolic args referred to in Φ
    x0  the initial approximation (currently an nx1 np.array)
    N   the partition size to use in RK4 (integer >1)
    
    OUTPUT

    x_sol   an np.array of shape x0.shape

    NOTES

    To speed implementation, the symbolic system of equations Φ(X) is
    "lambdified", that is, each symbolic equation is converted into a function
    that returns a floating point number. The advantage is that all references
    to symbolic objects are dropped (along with the hefty overhead) within the
    main loop, and instead everything is done in terms of floats and np.arrays.
    
    It should be noted that the specific line 

        mat2array = [{'ImmutableMatrix': np.array}, 'numpy'] # see docstring
        phi = sympy.lambdify(X, Φ, modules=mat2array)
    
    instructs the function sympy.lambdify to create a function that returns an
    array (rather than the less common np.matrix).  See documentation for lambdify.
    This behavior will be fixed in the next version of sympy and we will simply
    be able to write

        phi = sympy.lambdify(X, Φ, 'numpy')
    
    Refer to readme for explanation of *w.flatten() usage.

    Lastly, it should be noted that this speedup is really only worthwhile
    for smaller meshes (N large) or large systems (n := len(X) large). A future
    version of this code may implement an optional argument keep_symbolic to
    manually bypass this behavior.
    """ 
    
    h = 1/N # meshsize
    w = x0 
    
    # create a function that returns an np.array
    mat2array = [{'ImmutableMatrix': np.array}, 'numpy'] # see docstring
    phi = sympy.lambdify(X, Φ, modules=mat2array)

    if verbose:
        print("x(λ_0 = 0) =")
        print("\t", w.T)
        print("*"*30)

    
    for j in range(N):

        # treat each ki as a vector (np.array). 
        k1 = h*phi(*w.flatten())
        k2 = h*phi(*(w + (1/2)*k1).flatten())
        k3 = h*phi(*(w + (1/2)*k2).flatten())
        k4 = h*phi(*(w + k3).flatten())
        
        # update rule for W
        w = w + (1/6)*(k1 + 2*k2 + 2*k3 + k4)

        if verbose:
            print("x(λ_{} = {}/{}) = ".format(j+1,j+1,N))
            print("\t", w.T)
            print("*"*30)
    
    if verbose:
        print("done!")

    return w

if __name__ == "__main__":

    N = 4

    # this is Example 1 from Burden & Faires Ch10.5 (p664)

    ex1 = ["3*x1 - cos(x2*x3) - 0.5",
            "x1^2 - 81*(x2 + 0.1)^2 + sin(x3) + 1.06",
            "exp(-x1*x2) + 20*x3 + (10*pi - 3)/3"
            ]

    args = "x1,x2,x3"
    
    x0 = np.array([[0,0,0]]).T # create an 3x1 zero vector

    x_sol = cm_rk4(ex1, args, x0, 4, verbose=True)
