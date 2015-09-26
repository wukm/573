#!/usr/bin/env python3

import numpy as np
from newtons_for_systems import solve_nonlinear_system(case_two, args, x0)

args = "a,b"

table = [(75, 1.),
         (80, .99),
         (85, .833),
         (90, .612),
         (95, .412)]

fi_spec = "{} - b*({})^a"

case_two = [fi_spec.format(*pair) for pair in table]

# make an initial guess for a and b, i dunno
x0 = np.array([[1,1]]).T


