#!/usr/bin/env python3

from sympy import *
import numpy as np
import matplotlib.pyplot as plt

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

t_mesh = np.linspace(0,1)

plt.autumn()
fig = plt.figure()

for c_val, subplot_index in zip([0, 0.25, .5, .9], [221,222,223,224]):
    
    ax = fig.add_subplot(subplot_index)
    ax.set_color_cycle(['c','m','y','k'])
    ax.tick_params(labelsize='small')
    blends = [lambdify(t, bi) for bi in b.subs(c, c_val)]
    for i, blend  in enumerate(blends, 1):
        fn_label = r'$b_{}(t)$'.format(i)
        y = blend(t_mesh)
        ax.plot(t_mesh, y, label=fn_label, linewidth=2)
    ax.set_title(r'$c={}$'.format(c_val))
    ax.set_ylabel(r'$b_i(t)$')
    ax.set_xlabel(r'$t$')
    ax.legend(fontsize='medium')

plt.subplots_adjust(hspace=0.5)

fig.savefig('report/cardinals.png')
fig.show()
