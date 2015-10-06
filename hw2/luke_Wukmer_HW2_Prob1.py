#!/usr/bin/env python3

import numpy as np
from newtons_for_systems import solve_nonlinear_system
from continuation import cm_rk4 

system = ["4*x1^2 - 20*x1 + (1/4)*x2^2 + 8",
          "(1/2)*x1*x2^2 + 2*x1 - 5*x2 + 8"]
args = "x1, x2"

x0 = np.array([[0,0]]).T

print("newton's method (one iteration)")
x_a = solve_nonlinear_system(system, args, x0, M=1)

print("(newton's method):", x_a.T)
print("*"*40)
print("continuation method (one iteration)")

x_c = cm_rk4(system, args, x0, N=1, verbose=False)

print("x^(1) = ", x_c.T)
