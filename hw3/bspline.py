#!/usr/bin/env python3


"""
create a bspline to fit
"""
import numpy as np
import matplotlib.pyplot as plt

# copied & pasted from pdf & sorted into lines
table_x = """ 378 343 297 295 310 282 281 309 278 253
        206 135 121 114 74 33 45 30 31 0
        37 55 48 63 124 174 193 170 206 216
        266 259 290 318 257 378 343 297"""

table_y = """ 256 211 228 198 161 103 73 35 9 0
        47 66 54 17 2 45 99 149 165 239
        292 269 237 217 230 217 245 396 419 385
        407 384 375 361 367 256 211 228 """

# make this something i can actually use
data = [(float(x), float(y)) for x, y in zip(table_x.split(), table_y.split())]

P = np.array(data)
N = P.shape[0] # as a convenience
# by the way, to show a 2xN array like this, do plt.scatter(*P.T)

def blending_mesh(meshsize=100):
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

if __name__ == "__main__":
    
   
    fig = plt.figure()
    ax = fig.gca()

    ax.scatter(*P.T)    # plot control points
   
    B = blending_mesh() # it's constant!!!

    for k in range(N-3):
        g = B @ P[k:k+4]
        ax.plot(*g.T)
        

