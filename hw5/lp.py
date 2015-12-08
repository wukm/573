#!/usr/bin/env python3

def simplex(f, A, b):
    """
    solves a linear programming problem via simplex method
    input is the system f, A, b in canonical form.
    """

    # assert is_canonical(f,A,b)
    
    # if all c_i nonnegative
    if (f >= 0).all():
        print("solution found!")
        # ...

    # test theorem 2
    for s, c in enumerate(f):
        # if there exists a negative c_s
        if c < 0:
            # where a_{is} negative for all i 
            if (A[:,s] < 0).all():
                # output tableau?
                raise Exception("objective function is unbounded below by theorem 2")
    else:
        # step two complete, continue
        print("boundedness check complete, continuing")
    

    # blah

def is_canonical(f, A, b):
    """
    tests if the linear programming problem is in canonical form
    """
    
    # assert is_standard_form(f,A,b)

    if (b < 0).any():
        print("there are negative b entries")
        return False

def is_standard_form(f, A, b):
    
    pass
