#!/usr/bin/env python3

import numpy as np
from newtons_for_systems import solve_nonlinear_system


args = "a,b"

table = [(75, 1.),
         (80, .99),
         (85, .833),
         (90, .612),
         (95, .412)]

fi_spec = "{} - b*({})^a"

case_two = [fi_spec.format(*pair) for pair in table]

# make g(a,b) term 
squared = "+".join(("({})^2".format(fi) for fi in case_two))

# solve_nonlinear_system() expects a list :/
squared_case_two = [squared,]

# make an initial guess a, b = 1, 1 idk
x0 = np.array([[1,1]]).T

print("x0 == ", x0.T, "\n\n\n")

x_sol = solve_nonlinear_system(squared_case_two, args, x0, M=1000,
        x_convergence=True, ε=10e-3)

#x_sol = solve_nonlinear_system(case_two, args, x0, M=1000, ε=10e-9, x_convergence=True)
