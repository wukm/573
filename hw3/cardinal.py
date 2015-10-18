#!/usr/bin/env python3

from sympy import *

# C = M_H G_K = M_H (A G_C) = M_C G_C


c, t = symbols('c, t')

# transformation between hermite geometry and cardinal geometry
A = Matrix([[0, 2/(1-c), 0, 0],[0,0,2/(1-c),0],[-1,0,1,0],[0,-1,0,1]])
A = (1/2)*(1-c)*A
A.simplify()

# from hermite development
MH = Matrix([[2,-2,1,1],[-3,3,-2,-1],[0,0,1,0],[1,0,0,0]])

T = Matrix([[t**3],[t**2],[t],[1]])

MC = MH.multiply(A)
MC.simplify()

# b(t) = M_C^T t
b = MC.T.multiply(T)

