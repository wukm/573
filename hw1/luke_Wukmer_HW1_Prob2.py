#!/usr/bin/env python3

"""
MATH 573 HW1 PROBLEM 2
LUKE WUKMER

Warning: matplotlib

Figures are plotted corresponding to Fig 2.1(a) (p41) and
Fig 2.3(a) (p43) in the text.

The actual implementation of gradient descent on the surface
in question is contained within a separate file, p2b.py and
imported here.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import collections as mplc
from mpl_toolkits.mplot3d import Axes3D
import p2b

fig = plt.figure(1)
fig2 = plt.figure(2)

#ax = fig.add_subplot(111,projection='3d')
#ax2 = fig2.add_subplot(111)

ax = fig.gca(projection='3d')
ax2 = fig2.gca()
meshsize = 500
# there's a better way... right?
x0 = np.linspace(0,4, num=meshsize).reshape((-1,1))
y0 = np.linspace(0,-4, num=meshsize).reshape((-1,1))

z0 = (3/2)*x0**2 + 2*x0*y0 + 3*y0**2 - 2*x0 + 8*y0
x, y = np.meshgrid(x0,y0)
z = (3/2)*x**2 + 2*x*y + 3*y**2 - 2*x + 8*y
ax.plot_surface(x,y,z, alpha=0.3)
ax.contourf(x,y,z, offset=z.min(), cmap=None)


iterations = p2b.main()
A = np.array(iterations)
endpoints, fvals = A[:,:2], A[:,2]

# create contour lines specifically at each f(x_i,y_i)
#ax2.contourf(x,y,z, fvals)
ax2.contour(x,y,z, fvals)

# get x,y points only
its = [i[:2] for i in iterations]
# now pair each (x,y) with prev. (endpoints of each line segment)
segs = [(its[i], its[i-1]) for i in range(1,len(its))]
lines = mplc.LineCollection(segs, colors='black', linewidth=1,
        antialiaseds=1)

ax2.add_collection(lines)

# now add endpoint marks. yikes, these need to be an array
X, Y = np.array(its).T
ax2.scatter(X,Y, s=40, marker='*')


# label stuff
ax.set_title('(a) a surface f(x,y) for which a minimum is found')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x,y)')

ax2.set_title('(b) the minimization process via gradient descent')
ax2.set_xlabel('x')
ax2.set_ylabel('y')


fig.savefig('fig1.png', dpi=300)
fig2.savefig('fig2.png', dpi=300)
#plt.show()
#fig2.show()
