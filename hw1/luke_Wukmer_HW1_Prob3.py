#!/usr/bin/env python3

""" Testing for HW#1 question 3(b):
    testing steepest descent on a given 5x5 system
"""

from steepest_descent import steepest_descent
import numpy as np

A = np.array([
    [10,  1,  2,  3,  4],
    [ 1,  9, -1,  2, -3],
    [ 2, -1,  7,  3, -5],
    [ 3,  2,  3, 12, -1],
    [ 4, -3, -5, -1, 15]], )

b = np.array([[12,-27,14,-17,12]]).T


if __name__ == "__main__":

    x = steepest_descent(A, b)

    print("x = ", x.T)
