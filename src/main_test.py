#! /usr/bin/python3

##--------------------------------------------------------------------\
#   multi_glods_python
#   './multi_glods_python/src/main_test.py'
#   Test function/example for using the multiglods optimizer. To match
#       the format of the other optimizers in the AntennaCAT suite, this
#       file directly replaces multiglods_test.py from the main branch
#       of multi_glods_python. Format updates are for integration in
#       the AntennaCAT GUI.
#
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: June 28, 2024
##--------------------------------------------------------------------\


import sys
# multiGLODS functions
try: # for outside func calls, program calls
    sys.path.insert(0, './multi_glods_python/src/')
    from multi_glods import multi_glods

except:# for local, unit testing
    from multi_glods import multi_glods


# OBJECTIVE FUNCTION SELECTION
#import one_dim_x_test.configs_F as func_configs     # single objective, 1D input
#import himmelblau.configs_F as func_configs         # single objective, 2D input
import lundquist_3_var.configs_F as func_configs     # multi objective function


if __name__ == "__main__":
    # Constant variables
    TOL = 10 ** -6      # Convergence Tolerance (This is a radius 
                            # based tolerance, not target based tolerance)
    MAXIT = 3000        # Maximum allowed iterations  

    # Objective function dependent variables
    LB = func_configs.LB[0]              # Lower boundaries, [[0.21, 0, 0.1]]
    UB = func_configs.UB[0]              # Upper boundaries, [[1, 1, 0.5]]
    IN_VARS = func_configs.IN_VARS                 # Number of input variables (x-values)   
    OUT_VARS = func_configs.OUT_VARS  # Number of output variables (y-values)
    TARGETS = func_configs.TARGETS    # Target values for output

    # Objective function dependent variables
    func_F = func_configs.OBJECTIVE_FUNC  # objective function
    constr_F = func_configs.CONSTR_FUNC   # constraint function


    # optimizer specific vars
    BP = 0.5            # Beta Par
    GP = 1              # Gamma Par
    SF = 2              # Search Frequency


    # optimizer setting values
    parent = None                 # Optional parent class for optimizer
                                    # (Used for passing debug messages or
                                    # other information that will appear 
                                    # in GUI panels)

    best_eval = 1

    suppress_output = True   # Suppress the console output of multiglods



    detailedWarnings = False      # Optional boolean for detailed feedback
                                    # (Independent of suppress output. 
                                    #  Includes error messages and warnings)

    allow_update = True      # Allow objective call to update state 
                            # (Can be set on each iteration to allow 
                            # for when control flow can be returned 
                            # to multiglods)   



    # instantiation of multiglods optimizer 
    myGlods = multi_glods(IN_VARS, LB, UB, TARGETS, TOL, MAXIT,
                        func_F=func_F, constr_func=constr_F,
                        BP=BP, GP=GP, SF=SF,
                        parent=parent, detailedWarnings=detailedWarnings)


    # loop to run optimizer in
    while not myGlods.complete():

        # step through optimizer processing
        myGlods.step(suppress_output)

        # call the objective function, control 
        # when it is allowed to update and return 
        # control to optimizer
        myGlods.call_objective(allow_update)
        iter, eval = myGlods.get_convergence_data()

        if (eval < best_eval) and (eval != 0):
            best_eval = eval
        print("Objective Function Call Iterations")
        print(iter)
        print("Best Eval")
        print(best_eval)

    print("Optimized Solution")
    print(myGlods.get_optimized_soln())
    print("Optimized Outputs")
    print(myGlods.get_optimized_outs())

