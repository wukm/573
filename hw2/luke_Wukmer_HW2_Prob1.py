#!/usr/bin/env python3

import numpy as np
from newtons_for_systems import solve_nonlinear_system

system = ["4*x1^2 - 20*x1 + (1/4)*x2^2 + 8",
          "(1/2)*x1*x2^2 + 2*x1 - 5*x2 + 8"]
args = "x1, x2"

x0 = np.array([[0,0]]).T

x_sol = solve_nonlinear_system(system, args, x0)

