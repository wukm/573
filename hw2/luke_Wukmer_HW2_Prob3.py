#!/usr/bin/env python3

import numpy as np
from continuation import cm_rk4, rk4
from newtons_for_systems import parse_symbolic
from sympy.solvers import nsolve
import sys

case_one = ["z^2 + 1 - x*y",
            "x^2 + 2 - x*y*z - y^2",
            "exp(y) + 3 - exp(x) - z"
        ]

args = "x,y,z"

# really sloppy handling, use argparse
if len(sys.argv) > 1:
    try:
        N = int(sys.argv[1])
    except:
        raise Exception("argument must be an integer N (partition size in RK4)")

else:
    N = 4

# just set verbosity based on size of N
v = (N < 5)
x0 = np.array([[1,1,1]]).T

x_sol = cm_rk4(case_one, args, x0, N, verbose=v)

# now just do some data
F, X = parse_symbolic(case_one, args)

# get F value at x*
F1 = F.subs(list(zip(X, x_sol)))

err = F1.norm() # wow, these methods are great
print("||F(x*)|| = ", err)

x_check = nsolve(F, X, (1,1,1))
print("solution according to sympy.solvers.nsolve:")
print(x_check.T)
