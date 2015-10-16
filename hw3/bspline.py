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

        

