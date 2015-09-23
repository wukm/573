#!/usr/bin/env python3

"""
steepest descent for solving the quadratic surface minimization thing, sexlessly
adapted from matlab code on pp42-43
"""

from scipy import optimize

def f(x,y):
    """
    the function of the surface z = f(x,y)
    """

    return 1.5*x*x + 2*x*y + 3*y*y - 2*x + 8*y

def tau_search(t, x0, y0):
    """
    find an optimal step size for a given iteration
    ...of this particular problem

    default guess is 0.2 for no interesting reason
    """
    x = x0 - t * (3*x0 + 2*y0 - 2)
    y = y0 - t * (2*x0 + 6*y0 + 8)
    
    tau = f(x,y)
    return tau

def main(max_iterations=100, tol=10e-6, verbose=False):
    """
    Inputs:
        max_iterations (default=100)
        tol:     10e-6 (tolerance of convergence) (default 10e-6)
        verbose:    print stuff for each iteration (debugging)
    
    Output:
        iterations: a list of tuples (x,y,f(x,y)) for each iteration
    """
    
    M, ε = max_iterations, tol
    x, y = 1, -0.2 # initial guesses

    # adding to a numpy array on the fly is cumbersome, so I'm storing each
    # iteration in a list of tuples (x,y,z)
    iterations = [(x,y,f(x,y))]

    for j in range(M):
        # built-in to find minimum (like fminsearch in MATLAB)
        # (default for optimize.minimize_scalar anyway, but w/ nicer interface)
        τ = optimize.brent(tau_search, args=(x,y)) # get an optimal step size
        
        # update w/ the fancy new step size (this is the "descent" part)
        x, y = (x - τ*(3*x + 2*y - 2), y - τ*(2*x + 6*y + 8))

        iterations.append((x, y, f(x,y)))
        
        if verbose:
            # don't mind me; just spilling my guts
            print("τ\t={}".format(τ))
            print("x\t={}\ny\t={}\nf(x,y)\t={}".format(*iterations[-1]))
            print("*"*60)

        # ew
        if abs(iterations[-1][-1] - iterations[-2][-1]) < ε:
            print("converged in {} iterations.".format(j+1))

            break
        else:
            continue
    else:
        print("did not converge in M={} within tolerance ε={}".format(M,ε))

    return iterations

    
if __name__ == "__main__":

    iterations = main(tol=10e-6)
    # explicitly list the iterations if there aren't that many
    if len(iterations) <= 10:
        for k, it in enumerate(iterations):
            # there are way better ways to format this but hey
            print("step {}: f({}\t,{})\t= {}".format(k,it[0],it[1],it[2]))
