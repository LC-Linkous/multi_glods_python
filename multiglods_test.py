#! /usr/bin/python3
from multi_glods import multi_glods
from func_F import func_F

NO_OF_VARS = 3    # Number of input variables (x-values)
TOL = 10 ** -3    # Convergence Tolerance (This is a radius 
                  # based tolerance, not target based tolerance)
LB = [0, 0, 0]    # Lower boundaries
UB = [1, 1, 1]    # Upper Boundaries
BP = 0.5          # Beta Par
GP = 1            # Gamma Par
SF = 2            # Search Frequency
TARGETS = [0, 0]  # Target values for output
MAXIT = 3000      # Maximum allowed iterations  

suppress_output = False  # Suppress the console output of multiglods

allow_update = True      # Allow objective call to update state 
                         # (Can be set on each iteration to allow 
                         # for when control flow can be returned 
                         # to multiglods)

# instantiation of multiglods optimizer 
myGlods = multi_glods(NO_OF_VARS, LB, UB, BP, GP, 
                      SF, TARGETS, TOL, MAXIT, func_F)

# loop to run optimizer in
while not myGlods.complete():

    # step through optimizer processing
    myGlods.step(suppress_output)

    # call the objective function, control 
    # when it is allowed to update and return 
    # control to optimizer
    myGlods.call_objective(allow_update)


