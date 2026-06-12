#! /usr/bin/python3

##--------------------------------------------------------------------\
#   multi_glods_python
#   './multi_glods_python/src/multiglods_helpers.py'
#   MultiGLODS helper functions for supporting algorithm, controller, 
#       and statemachine
#
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: June 20, 2025
##--------------------------------------------------------------------\


import numpy as np
import copy

# check feasibility
def feasible(x, ubound, lbound, n, ctl):
    feas = 1
    bound = np.array([[x - ubound], [lbound - x]])
    if np.sum(bound <= 0) != 2*n:
        feas = 0
    if feas:
        feas = ctl['constr_func'](x)
    return feas

# increment iteration
def inc_iter(ctl, run_ctl):
    if not (ctl['poll_loop'] or ctl['search_loop']):
        run_ctl['iter'] = run_ctl['iter'] + 1

    return run_ctl

# replicate - NOT USED. 
# Included to support features not yet integrated from the original MultiGLODS
# 
# def replicate(v, M):
#     if np.ndim(v) < 2:
#         v = np.array([v])

#     M_new = np.hstack([M, np.tile(v[0][0], (np.shape(M)[0], 1))])
#     if (np.shape(v)[0] > 1):
#         for i in np.linspace(2, np.shape(v)[0], np.shape(v)[0]-1):
#             M_new = np.round(np.vstack([M_new,
#                                np.hstack([M,
#                                           np.tile(v[int(i-1)],
#                                                   (np.shape(M)[0],
#                                                    1))])])

#     return M_new

# logical indexing
def logical_index_1d(log_idx, list_in):
    log_idx = copy.deepcopy(log_idx)
    list_out = copy.deepcopy(list_in)
    if np.shape(log_idx):
        log_idx = log_idx.astype(int)
    else:
        log_idx = int(log_idx)

    ret_list = list_out

    if np.shape(np.shape(list_out))[0]:
        if np.shape(np.shape(list_out))[0] > 1:
            if np.shape(list_out)[0] > np.shape(list_out)[1]:
                length = np.shape(list_out)[0]
            else:
                length = np.shape(list_out)[1]
        else:
            length = np.shape(list_out)[0]
        count = 0
        for i in range(0, length):
            if np.shape(log_idx):
                if np.squeeze(log_idx)[i]:
                    ret_list[count] = np.squeeze(list_out)[i]
                    count = count+1

            else:
                if log_idx:
                    ret_list = list_out
                    count = count+1
        if np.shape(np.shape(ret_list))[0] > 1:
            ret_list = ret_list[0][0:count]
        else:
            ret_list = ret_list[0:count]

    return ret_list

# logical indexing
def logical_index_h2d(log_idx, list):
    log_idx = copy.deepcopy(log_idx)
    if np.shape(log_idx):
        log_idx = log_idx.astype(int)
    else:
        log_idx = int(log_idx)
    ret_list = list
    if np.shape(np.shape(list))[0]:
        if (np.shape(np.shape(list))[0] > 1):               
            length = np.shape(list)[1]
        else:         
            length = np.shape(list)[0]
        count = 0
        for i in range(0, length):
            if np.shape(log_idx):
                if np.squeeze(log_idx)[i]:
                    ret_list[:, count] = list[:, i]
                    count = count + 1
            else:
                if log_idx:
                    ret_list = list
                    count = count + 1
        if count:
            ret_list = ret_list[:, 0:count]

    return ret_list

# logical indexing
def logical_index_h2d_Plist(log_idx, list):
    log_idx = copy.deepcopy(log_idx)
    if np.shape(log_idx):
        log_idx = log_idx.astype(int)
    else:
        log_idx = int(log_idx)
    ret_list = list
    if np.shape(np.shape(list))[0]:

        if (np.shape(np.shape(list))[0] > 1):
            length = np.shape(list)[1]
        else:
            length = np.shape(list)[0]
        count = 0
        for i in range(0, length):
            if np.shape(log_idx):
                if np.squeeze(log_idx)[i]:
                    ret_list[:, count] = list[:, i]
                    count = count + 1
            else:
                if log_idx:
                    ret_list = list
                    count = count + 1
        if count:
            ret_list = ret_list[:, 0:count]

    return ret_list

# # logical indexing -NOT USED. 
# Included to support features not yet integrated from the original MultiGLODS
# 
# def logical_index_v2d(log_idx, list):
#     log_idx = copy.deepcopy(log_idx)
#     log_idx = log_idx.astype(int)
#     ret_list = list

#     if np.shape(np.shape(list))[0]:

#         if np.shape(np.shape(list))[0] > 1:
#             if np.shape(list)[0] > np.shape(list)[1]:
#                 length = np.shape(list)[0]
#             else:
#                 length = np.shape(list)[1]
#         else:
#             length = np.shape(list)[0]
#         count = 0
#         for i in range(0, length):
#             if log_idx[i]:
#                 ret_list[count, :] = list[i, :]
#                 count = count + 1

#         ret_list = ret_list[0:count, :]

#     return ret_list

# set value from logical index
def logical_set_val(log_idx, list, val):
    log_idx = copy.deepcopy(log_idx)
    log_idx = log_idx.astype(int)
    ret_list = list

    if np.shape(np.shape(list))[0]:
        if np.shape(np.shape(list))[0] > 1:
            if np.shape(list)[0] > np.shape(list)[1]:
                length = np.shape(list)[0]
            else:
                length = np.shape(list)[1]
        else:
            length = np.shape(list)[0]

        for i in range(0, length):
            if length == 1 and np.squeeze(log_idx):
                ret_list = val
            else:
                if np.squeeze(log_idx)[i]:
                    ret_list[i] = val[i]
    else:
        if log_idx:
            ret_list = val

    return ret_list

# debug statement for multiglods main loop
def print_debug(run_ctl, state, ctl, prob, init, alg, NO_OF_LOOPS, INSPECT_LOOP):

    if NO_OF_LOOPS == INSPECT_LOOP:
        print("run_ctl")
        print(run_ctl)
        print("state")
        print(state)
        print("ctl")
        print(ctl)
        print("prob")
        print(prob)
        print("init")
        print(init)
        print("alg")
        print(alg)
        state['main_loop']['run'] = 0

    NO_OF_LOOPS = NO_OF_LOOPS + 1
    return state, NO_OF_LOOPS

# mark objective function for evaluation
def  f_eval(state, xlist, prob, location):
    state['evaluate'] = 1
    state['location'] = location
    prob['xtemp'] = xlist   # here prob['xtemp'] is being set with prob['xtemp'] from multiglods.py
    return state, prob

# handle objective function return at appropriate call location
# NOTE: decoupled. The fitness evaluation (Ftemp) is now computed in
# f_eval_objective_call() at the time the objective is called, so the
# controller can check termination conditions against FRESH data
# before the next step() consumes it and advances the state machine.
# This function is now purely the state handshake that lets the state
# machine resume at the matching call location (1=init, 2=search, 3=poll).
def f_eval_return(state, prob, alg, location):
    if state['eval_return'] and (state['location'] == location):
        state['eval_return'] = 0

    return state, prob

# call objective function, allow it to update when desired
def f_eval_objective_call(state, prob, ctl, alg, allow_update):
    # DECOUPLE NOTE:
    # This function now does ALL of the data handling for an objective
    # function evaluation: the raw call (FValtemp) AND the target/threshold
    # fitness evaluation (Ftemp). Previously the Ftemp calculation happened
    # inside the next step() call (in f_eval_return), which meant:
    #   1) After call_objective() returned, the wrapper's convergence data
    #      (Flist, Ftemp) was one evaluation STALE.
    #   2) The same step() call that ingested the data also merged it,
    #      ran run_update(), and queued the next evaluation - so there was
    #      no point where a controller could check termination conditions
    #      against the fresh evaluation before the optimizer advanced.
    # Now step() purely CONSUMES already-evaluated data (like pso_basic:
    # check previous data, then move), and call_objective() purely
    # EVALUATES, gated by allow_update.

    noErrorBool = True #this is pretty stable, 
                        # so default of true when NOT evaluating 
                        # has not shown issues in testing. 


    if state['evaluate']:
        # NOTE: this is a change from the original multiglods_helpers.py
        # the new objective function configuration takes a horizontal array.
        FVals, noErrorBool = ctl['obj_func'](np.hstack(prob['xtemp']))
        if noErrorBool == True:
            # this is the standard setup/shape for the AntennaCAT optimizer set. 
            # left here for feature matching between optimizers. 
            prob['FValtemp'] = np.array(FVals).reshape(-1, 1)

            # adjust the fitness values output to be vertical to match multiGLODS expectations
            prob['FValtemp'] = np.vstack(prob['FValtemp'])  

            if allow_update:
                # evaluate fitness vs. target/threshold NOW, so the
                # controller sees fresh data before the next step().
                # The values for 'Ftemp' are merged into ctl['Flist'] by
                # the post_objective_* functions when step() resumes at
                # the matching state['location'].
                prob['Ftemp'] = objective_function_evaluation(prob['FValtemp'],
                                                              alg['targets'],
                                                              alg['evaluate_threshold'],
                                                              alg['threshold'])

                state['evaluate'] = 0
                state['eval_return'] = 1
                ctl['objective_iter'] = ctl['objective_iter']  + 1

        else:
            print("ERROR: error in evaluation of the objective function. Check evaluation")

    return state, prob, noErrorBool
 

def objective_function_evaluation(Fvals, targets, evaluate_threshold, obj_threshold):
        #pass in the Fvals & targets so that it's easier to track bugs
        # this is pulled directly from the antennaCAT optimizer set as a way to 
        # streamline the development. 

        # this uses the fitness values and target (or threshold) to determine the Flist values
        # Option #1: TARGET
        # get DISTANCE FROM TARGET
        # Option #2: THRESHOLD
        # use THRESHOLD TO DETERMINE INTEREST
        # if threshold is met, the distance is set to a small value (epsilon).
        #  Setting the 'distance' to epsilon, the convergence value check can
        # also remain the same format. 


        # testing different values of epsilon
        epsilon = np.finfo(float).eps #smallest system constant
        # Ex: 2.220446049250313e-16  
        # #may be greater than tolerance if tolerance is set very low for testing
        #epsilon = 10**-18
        #epsilon = 0  # causes issues with imag. numbers

        Flist = np.zeros_like(Fvals)

        if evaluate_threshold == True: #THRESHOLD
            ctr = 0
            for i in targets:
                #print(f"obj_threshold[ctr]: {obj_threshold[ctr]}")
                #o_thres = int(obj_threshold[ctr]) #force type as err check
                o_thres = int(np.squeeze(obj_threshold[ctr])) #force type as err check, squeeze to get scalar
                # o_thres = int(obj_threshold[ctr].item()) #force type as err check
                t = targets[ctr]
                fv = Fvals[ctr]

                if o_thres == 0: #TARGET. default
                    # sets Flist[ctr] as abs distance of  Fvals[ctr] from target
                    Flist[ctr] = abs(t - fv)

                elif o_thres == 1: #LESS THAN OR EQUAL 
                    # checks if the Fvals[ctr] is LESS THAN OR EQUAL to target
                    # if yes, then distance is 0 (considered 'on target)
                    # if no, then Flist is abs distance of  Fvals[ctr] from target
                    if fv <= t:
                        Flist[ctr] = epsilon
                    else:
                        Flist[ctr] = abs(t - fv)

                elif o_thres == 2: #GREATER THAN OR EQUAL
                    # checks if the Fvals[ctr] is GREATER THAN OR EQUAL to target
                    # if yes, then distance is 0 (considered 'on target)
                    # if no, then Flist is abs distance of  Fvals[ctr] from target
                    if fv >= t:
                        Flist[ctr] = epsilon
                    else:
                        Flist[ctr] = abs(t - fv)

                else: #o_thres == 0. #TARGET. default
                    print("ERROR: unrecognized threshold value. Evaluating as TARGET")
                    Flist[ctr] = abs(t - fv)

                ctr = ctr + 1

        else: #TARGET as default
            # arrays are already the same dimensions. 
            # no need to loop and compare to anything
            Flist = abs(targets - Fvals)


        return Flist
        