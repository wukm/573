#!/usr/bin/env python3

from bspline import blending_mesh, b_splines
import numpy as np
import matplotlib.pyplot as plt

# copied & pasted from pdf & sorted into lines
table_x = """ 378 343 297 295 310 282 281 309 278 253
        206 135 121 114 74 33 45 30 31 0
        37 55 48 63 124 174 193 170 206 216
        266 259 290 318 357 378 343 297"""

table_y = """ 256 211 228 198 161 103 73 35 9 0
        47 66 54 17 2 45 99 149 165 239
        292 269 237 217 230 217 245 396 419 385
        407 384 375 361 367 256 211 228 """

# make this something i can actually use
data = [(float(x), float(y)) for x, y in zip(table_x.split(), table_y.split())]

P = np.array(data)

if __name__ == "__main__":
    
   
    fig = plt.figure()
    ax = fig.gca()
    ax.set_aspect('equal')

    ax.scatter(*P.T)    # plot control points
   
    B = blending_mesh() # it's constant!!!

    # iterate over {P[i],P[i+1],P[i+2],P[i+3]} via a generator
    for spline in b_splines(P):
        ax.plot(*spline.T)

    fig.savefig('report/doggy_splines.png')
