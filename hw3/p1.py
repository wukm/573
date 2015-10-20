#!/usr/bin/env python3

"""
math check for problem #1
also graphs for funsies
"""

import numpy as np
from least_squares import *
import matplotlib.pyplot as plt

#Table 1: Data for problem 1
TABLE_1    = [[  1.0,    1.1,    1.3,    1.5],
              [ 1.84,   1.96,   2.21,   2.45]]


if __name__ == "__main__":
    X = np.linspace(0, 2, 100) # fix bounds to match range of data

    # conveniences
    x = np.array(TABLE_1[0])
    y = np.array(TABLE_1[1])


    for i, n in enumerate([2,3],1):
        
        titles = ["(a)", "(b)"] # ew

        print("least squares poly, deg={}".format(n) , "*"*40)
        fig = plt.figure(i)

        a = poly_lsq(TABLE_1, n)
        print("found coefficients:", a)
        p = lambda x: sum((ai*x**i for i, ai in enumerate(a))) 
        Y = p(X)

        ax = fig.gca() 
        ax.scatter(*TABLE_1)
        ax.plot(X,Y)
        ax.set_title(titles[i-1])   # ew

        lsq_error = np.sum((p(x) - y)**2)
        print("E_2(a)=", lsq_error)
        fig.savefig("report/p1_{}.png".format(n))

    # now exponential (part (c))
    fig = plt.figure(3)
    a,b = exponential_lsq(TABLE_1)
    print("found coefficients:", a,b)
    p = lambda x: b*x**a
    Y = p(X)

    ax = fig.gca()
    ax.scatter(*TABLE_1)
    ax.plot(X,Y)
    ax.set_title("(c)")
    lsq_error = np.sum((p(x) - y)**2)

    print("E_2(a)=", lsq_error)
    fig.savefig("report/p1_exp.png")

