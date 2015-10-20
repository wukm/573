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
#conveniences
x, y = data

# part a 

A = poly_lsq(data, 1)

print("line coefficients:", A)
X = np.linspace(100, 400, 200) # fix bounds to match size of data
p = lambda x: sum(ai*(x**i) for i, ai in enumerate(A))
print("p_1(90)=",  p(90))
print("p_1(60)=",  p(60))

lsq_error = np.sum((p(x) - y)**2)
print("linear error = ", lsq_error)

Y = p(X) # for graphing

a, b = exponential_lsq(data)
print("exp. coefficients, a={}, b={}".format(a,b))
pe = lambda x: b*x**a
print("p_e(90)=",  pe(90))
print("p_e(60)=",  pe(60))
YX = pe(X)
exp_error = np.sum((pe(x) - y)**2)
print("exponential error = ", exp_error)


# graphing stuff

fig = plt.figure(1)
ax = fig.gca()
ax.scatter(*data)
ax.plot(X,Y, label=r'$p_2(x)$')
ax.plot(X,YX, label=r'$y(x)=bx^a$')
ax.set_title('least squares problem 3(a)')
ax.set_ylabel('final score (pts)')
ax.set_xlabel('hw score (pts)')
ax.legend()

fig.savefig('report/p3.png')
