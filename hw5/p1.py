#!/usr/bin/env python3


import numpy as np
from lp import simplex

# problem 1 in canonical form. note that f and b are 1D arrays

f = np.array([-8, -60, -45, 0, 0])

A = np.array([[2, 12, 15, 1, 0],
              [1,  8,  6, 0, 1]])

b = np.array([1500, 920])

# the constant in the objective function (bottom right of tableau)
z0 = 0

T = simplex(f, A, b)
