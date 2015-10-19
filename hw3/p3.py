#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from least_squares import *

# table 2 copy pasted from hw pdf
hw = [302, 339, 331, 347, 326, 323, 304, 337, 343, 185,
    325, 334, 279, 343, 233, 337, 319, 351, 314, 340,
    285, 322, 316, 290, 254, 337, 234, 339, 344, 316]
final = [ 45, 54, 99, 99, 76, 83, 62, 53, 83, 59,
    72, 79, 63, 83, 57, 99, 66, 100, 42, 75,
    54, 65, 65, 74, 45, 70, 51, 67, 79, 45]

data = np.array([hw, final])

# part a 

A = polynomial_lsq(data, 2)
X = np.linspace(0, 400, 200) # fix bounds to match size of data
p = lambda x: sum(ai*(x**i) for i, ai in enumerate(A))
Y = p(X)

plt.scatter(*data)
plt.plot(X,Y)
