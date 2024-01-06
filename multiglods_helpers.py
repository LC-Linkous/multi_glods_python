#! /usr/bin/python3
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

# replicate 
def replicate(v, M):
    if np.ndim(v) < 2:
        v = np.array([v])

    M_new = np.hstack([M, np.tile(v[0][0], (np.shape(M)[0], 1))])
    if (np.shape(v)[0] > 1):
        for i in np.linspace(2, np.shape(v)[0], np.shape(v)[0]-1):
            M_new = np.vstack([M_new,
                               np.hstack([M,
                                          np.tile(v[int(i-1)],
                                                  (np.shape(M)[0],
                                                   1))])])

    return M_new

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

# logical indexing
def logical_index_v2d(log_idx, list):
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
        count = 0
        for i in range(0, length):
            if log_idx[i]:
                ret_list[count, :] = list[i, :]
                count = count + 1

        ret_list = ret_list[0:count, :]

    return ret_list

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
    prob['xtemp'] = xlist   
    return state, prob

# handle objective function return at appropriate call location
def f_eval_return(state, prob, alg, location):
    if state['eval_return'] and (state['location'] == location):
        state['eval_return'] = 0
        prob['Ftemp'] = abs(alg['targets']-prob['FValtemp'])
        
    return state, prob

# call objective function, allow it to update when desired
def f_eval_objective_call(state, prob, ctl, allow_update):
    if state['evaluate']:
        prob['FValtemp'] = ctl['obj_func'](prob['parent'], prob['xtemp'])
        if allow_update:
            state['evaluate'] = 0
            state['eval_return'] = 1
    return state, prob
 