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


def cm_rk4(F_strings, F_args, x0, N):

    F, X = parse_symbolic(F_strings, F_args)
    print("system parsed!")
    J = F.jacobian(X)   # symbolic jacobian matrix
    print("jacobian formed!")

    Jinv = J.inv()  # calculate inverse (method can be specified)
    print("...and inverted!")
    #Jinv.simplify() # simplify result (for logging)
    print("...and simplified")
    
    F0 = F.subs(list(zip(X, x0))) # don't know why list() is req'd
    print("initial system calculated")

    # x`(λ) = [J(x(λ)]^(-1) * F0
    # this is an nx1 matrix that describes the set of differential equations
    #   dx_i / dλ = [x`(λ)]_i

    xpl = -Jinv.multiply(F0) # mat_mul syntax is different within sympy?
    print("ODE system calculated")

    # simplify method works in place, whereas sympy.simplify returns!
    #xpl.simplify() # for logging
    print("...and simplified")
    
    print("running RK4 with N={}".format(N))

    x_sol = rk4(xpl, X, x0, N)

    return x_sol

def rk4(Φ, X, x0, N):
    """
    Runge-Kutta Method (Order 4)
    Φ is a symbolic vector whose components give the system of
    differential equations
    
       [ d(X[i]) / dλ ] = Φ[i]

    where
    
    X is the symbolic args referred to in Φ
    x0 is the initial guess of the system
    N is the partition size (integer >1)
    """ 
    
    # pseudocode, treating Φ as a function
    h = 1/N
    w = x0
    
    mat2array = [{'ImmutableMatrix': np.array}, 'numpy']
    phi = sympy.lambdify(X, Φ, modules=mat2array)

    print("x(λ_0 = 0) =")
    print("\t", w.T)
    print("*"*30)


    for j in range(N):

        k1 = h*phi(*w.flatten())
        k2 = h*phi(*(w + (1/2)*k1).flatten())
        k3 = h*phi(*(w + (1/2)*k2).flatten())
        k4 = h*phi(*(w + k3).flatten())
        
        w = w + (1/6)*(k1 + 2*k2 + 2*k3 + k4)

        print("x(λ_{} = {}/{}) = ".format(j+1,j+1,N))
        print("\t", w.T)
        print("*"*30)
   
    print("done!")
    return w

if __name__ == "__main__":

    N = 4

    ex1 = ["3*x1 - cos(x2*x3) - 0.5",
            "x1^2 - 81*(x2 + 0.1)^2 + sin(x3) + 1.06",
            "-x2*exp(-x1*x2) + 20*x3 + (10*pi - 3)/3"
            ]
    args = "x1,x2,x3"
    
    x0 = np.array([[0,0,0]]).T

    #F_strings, F_args = ex1, args
    
    #F, X = parse_symbolic(F_strings, F_args)
    #print("parsed!")
    #J = F.jacobian(X)   # symbolic jacobian matrix
    #print("jacobian found")
    #Jinv = J.inv()  # calculate inverse (method can be specified)
    #print("jacobian inverted")

    ## simplifying takes waaaaay tooooo long
    ##Jinv = sympy.simplify(Jinv) # simplify result (for logging)
    #
    #F0 = F.subs(list(zip(X, x0))) # don't know why list() is req'd
    #print("found F[0]")

    ## x`(λ) = [J(x(λ)]^(-1) * F0
    ## this is an nx1 matrix that describes the set of differential equations
    ##   dx_i / dλ = [x`(λ)]_i

    #xpl = -Jinv.multiply(F0) # mat_mul syntax is different within sympy?

    ## simplifying takes waaaaay tooooo long
    ##xpl = xpl.simplify() # for logging
    #
    #print("set up complete. running runge-kutta.")
    #x_sol = rk4(xpl, X, x0, N)
   
    x_sol = cm_rk4(ex1, args, x0, 4)
