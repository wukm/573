#!/usr/bin/env python3

import numpy as np
from continuation import cm_rk4, rk4
from newtons_for_systems import parse_symbolic
from scipy.linalg import norm

case_one = ["z^2 + 1 - x*y",
            "x^2 + 2 - x*y*z + y^2",
            "exp(y) + 3 - exp(x) + z"
        ]

args = "x,y,z"

x0 = np.array([[1,1,1]]).T

x_sol = cm_rk4(case_one, args, x0, 300)

F, X = parse_symbolic(case_one, args)

F1 = F.subs(list(zip(X, x_sol)))

err = F1.norm() # wow, these methods are great
print("||F(x*)|| = ", err)

