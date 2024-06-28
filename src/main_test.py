#! /usr/bin/python3

##--------------------------------------------------------------------\
#   multi_glods_python
#   './multi_glods_python/src/main_test.py'
#   Test function/example for using the 'swarm' class in particle_swarm.py.
#       This has been modified from the original to include message 
#       passing back to the parent class or testbench, rather than printing
#       error messages directly from the 'swarm' class. Format updates are 
#       for integration in the AntennaCAT GUI.
#
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: June 28, 2024
##--------------------------------------------------------------------\



import numpy as np
# OBJECTIVE FUNCTION
#import one_dim_x_test.configs_F as func_configs     # single objective, 1D input
#import himmelblau.configs_F as func_configs         # single objective, 2D input
import lundquist_3_var.configs_F as func_configs    # multi objective function

if __name__ == "__main__":
    NO_OF_PARTICLES = 50         # Number of particles in swarm
    LB = [[0.21, 0, 0.1]]        # Lower boundaries
    UB = [[1, 1, 0.5]]           # Upper boundaries
    WEIGHTS = [[0.7, 1.5, 0.5]]  # Update vector weights
    VLIM = 0.5                   # Initial velocity limit
    OUT_VARS = 2                 # Number of output variables (y-values)
    TARGETS = [0, 0]             # Target values for output
    T_MOD = 0.65                 # Variable time-step extinction coefficient
    E_TOL = 10 ** -6             # Convergence Tolerance
    MAXIT = 5000                 # Maximum allowed iterations
    BOUNDARY = 1                 # int boundary 1 = random,      2 = reflecting
                                #              3 = absorbing,   4 = invisible

    best_eval = 1

    parent = None            # for the PSO_TEST ONLY

    suppress_output = True   # Suppress the console output of particle swarm

    allow_update = True      # Allow objective call to update state 



    mySwarm = swarm(NO_OF_PARTICLES, LB, UB,
                    WEIGHTS, VLIM, OUT_VARS, TARGETS,
                    T_MOD, E_TOL, MAXIT, BOUNDARY, func_F, constr_F)  

    # instantiation of particle swarm optimizer 
    while not mySwarm.complete():

        # step through optimizer processing
        mySwarm.step(suppress_output)

        # call the objective function, control 
        # when it is allowed to update and return 
        # control to optimizer
        mySwarm.call_objective(allow_update)
        iter, eval = mySwarm.get_convergence_data()
        if (eval < best_eval) and (eval != 0):
            best_eval = eval
        if suppress_output:
            if iter%100 ==0: #print out every 100th iteration update
                print("Iteration")
                print(iter)
                print("Best Eval")
                print(best_eval)

    print("Optimized Solution")
    print(mySwarm.get_optimized_soln())
    print("Optimized Outputs")
    print(mySwarm.get_optimized_outs())

