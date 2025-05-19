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
#   Last update: March 13, 2025
##--------------------------------------------------------------------\


import sys
import pandas as pd
import numpy as np
# multiGLODS functions
try: # for outside func calls, program calls
    sys.path.insert(0, './multi_glods_python/src/')
    from multi_glods import multi_glods

except:# for local, unit testing
    from multi_glods import multi_glods


# OBJECTIVE FUNCTION SELECTION
#import one_dim_x_test.configs_F as func_configs     # single objective, 1D input
import himmelblau.configs_F as func_configs         # single objective, 2D input
#import lundquist_3_var.configs_F as func_configs    # multi objective function


if __name__ == "__main__":
    # Constant variables
    TOL = 10 ** -6      # Convergence Tolerance (This is a radius 
                            # based tolerance, not target based tolerance)
    MAXIT = 10000       # Maximum allowed iterations  

    # Objective function dependent variables
    LB = func_configs.LB              # Lower boundaries, [[0.21, 0, 0.1]]
    UB = func_configs.UB              # Upper boundaries, [[1, 1, 0.5]]
    IN_VARS = func_configs.IN_VARS    # Number of input variables (x-values)   
    OUT_VARS = func_configs.OUT_VARS  # Number of output variables (y-values)
    TARGETS = func_configs.TARGETS    # Target values for output
    # target format. TARGETS = [0, ...] 

    # threshold is same dims as TARGETS
    # 0 = use target value as actual target. value should EQUAL target
    # 1 = use as threshold. value should be LESS THAN OR EQUAL to target
    # 2 = use as threshold. value should be GREATER THAN OR EQUAL to target
    #DEFAULT THRESHOLD
    THRESHOLD = np.zeros_like(TARGETS) 
    #THRESHOLD = np.ones_like(TARGETS)
    #THRESHOLD = [0, 1, 0]
    # Objective function dependent variables
    func_F = func_configs.OBJECTIVE_FUNC  # objective function
    constr_F = func_configs.CONSTR_FUNC   # constraint function


    # optimizer specific vars
    BP = 0.5            # Beta Par
    GP = 1              # Gamma Par
    SF = 3              # Search Frequency


    # optimizer setting values
    parent = None                 # Optional parent class for optimizer
                                    # (Used for passing debug messages or
                                    # other information that will appear 
                                    # in GUI panels)
    best_eval = 1
    suppress_output = True    # Suppress the console output of MultiGLODS
    evaluate_threshold = True # use target or threshold. True = THRESHOLD, False = EXACT TARGET
    allow_update = True       # Allow objective call to update state 
                              # (Can be set on each iteration to allow 
                              # for when control flow can be returned 
                              # to MultiGLODS)   



    # instantiation of MultiGLODS optimizer 
    # Constant variables
    opt_params = {'BP': [BP],               # Beta Par
                'GP': [GP],                 # Gamma Par
                'SF': [SF] }                # Search Frequency

    opt_df = pd.DataFrame(opt_params)
    myGlods = multi_glods(LB, UB, TARGETS, TOL, MAXIT,
                            func_F, constr_F,
                            opt_df,
                            parent=parent, 
                            evaluate_threshold=evaluate_threshold, obj_threshold=THRESHOLD)  
    # sometimes multiGLODS doesn't call the objective function, so only print out when it does
    last_iter = 0

    # loop to run optimizer in
    while not myGlods.complete():

        # step through optimizer processing
        myGlods.step(suppress_output)

        # call the objective function, control 
        # when it is allowed to update and return 
        # control to optimizer
        noErr = myGlods.call_objective(allow_update)
        if noErr == True: # checking for failure to evaluate. 

            iter, eval = myGlods.get_convergence_data()
            if (eval < best_eval) and (eval != 0):
                best_eval = eval
            if iter > last_iter:
                last_iter = iter
                if suppress_output:
                    if iter%10 == 0: #print out every 10th iteration update
                        print("************************************************")
                        print("Objective Function Iterations: " + str (iter))
                        print("Best Eval: " + str(best_eval))

        else:
            print("ERROR: in executing objective function call. " \
            "This may be due to constraints or problem definition")

    print("************************************************")
    print("Objective Function Iterations: " + str (iter))
    print("Best Eval: " + str(best_eval))
    print("Optimized Solution")
    print(myGlods.get_optimized_soln())
    print("Optimized Outputs")
    print(myGlods.get_optimized_outs())

