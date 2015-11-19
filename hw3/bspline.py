#!/usr/bin/env python3


"""
create a bspline from a sequence of data points, or apply to a mesh
directly.
"""
import numpy as np

def blending_mesh(meshsize=500):
    """
    with blending functions for a bspline, create a (meshsize x 4) array B
    such that a meshgrid of the bspline g = B@G where G is 4 consecutive
    points (i.e. G is shape (4,3). This is *fixed* for the bspline method--
    the only thing that varies from input to input is out of the realm of this
    function (namely, the geometry [P_i, ... P_{i+3}])

    note: in the theory presented in lecture, this actually returns B.T
    """

    # component blending functions (
    b1 = lambda t: (1/6)*(1-t)**3
    b2 = lambda t: (1/6)*(3*t**3 - 6*t**2 + 4)
    b3 = lambda t: (1/6)*(-3*t**3 + 3*t**2 + 3*t + 1)
    b4 = lambda t: (1/6)*t**3

    mesh = np.linspace(0,1,num=meshsize) # [0,1] mesh with ``meshsize'' points
    
    # build a meshsize x 4 array by applying these b_i to the mesh
    B = [[b1(t), b2(t), b3(t), b4(t)] for t in mesh]

    return np.array(B)

def b_splines(P, meshsize=500):        
    """
    a generator for bsplines (e.g. to be iterated over in a for loop);
    each call returns a successive b-spline (which is an array of shape
    (meshsize, P.shape[1])) to be graphed. (P.shape[0] - 3) such
    arrays will be generated. This function does not return a lambda/symbolic
    version of these splines but instead the actual meshgrid.

    """
    
    N = P.shape[0] # for convenience, the number of total points

    assert N > 3, "Not enough points to make a spline!"
    
    B = blending_mesh(meshsize) # it's constant

    for k in range(N-3):

        yield B @ P[k:k+4] 

