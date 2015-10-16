#!/usr/bin/env python3


"""
create a bspline to fit
"""
import numpy as np

def blending_mesh(meshsize=500):
    """
    with blending functions for a bspline, create a (4,meshsize) shaped array
    B such that a meshgrid of the bspline g = B@G where G is 4 consecutive
    points (i.e. G is shape (4,3) This is fixed for the bspline method---the
    only thing that varies from input to input is out of the realm of this
    function.

    note: in the theory presented in lecture, this is actually B.T
    """

    # data types here could be life or death. doing naively first
    
    # component blending functions
    b1 = lambda t: (1-t)**3
    b2 = lambda t: 3*t**3 - 6*t**2 + 4
    b3 = lambda t: -3*t**3 + 3*t**2 + 3*t + 1
    b4 = lambda t: t**3

    mesh = np.linspace(0,1,num=meshsize) # [0,1] mesh with meshsize points
    
    # probably don't need to do this way
    B = [[b1(t), b2(t), b3(t), b4(t)] for t in mesh]

    return (1/6)*np.array(B)

def b_splines(P, meshsize=500):        
    """
    a generator for bsplines. each call returns a successive b-spline (which is
    an array of shape (meshsize, P.shape[1])) to be graphed. P.shape[0] - 3 such
    points will be generated. This function does not return a lambda/symbolic
    version of these splines but the actual meshgrid or whatever
    """
    
    N = P.shape[0] # for convenience, the number of total points

    assert N > 3, "Not enough points to make a spline!"
    
    B = blending_mesh(meshsize) # it's constant

    for k in range(N-3):

        yield B @ P[k:k+4] 

    


