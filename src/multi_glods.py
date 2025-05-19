#! /usr/bin/python3

##--------------------------------------------------------------------\
#   multi_glods_python
#   './multi_glods_python/src/multi_glods.py'
#   Class for intializing and interfacing with the multiGLODS algorithm
#   NOTE: multiglods.py is the statemachine, 
#       and multiglods_ctl.py is the controller
#
#   Author(s): Jonathan Lundquist, Lauren Linkous 
#   Last update: March 13, 2025
##--------------------------------------------------------------------\


import numpy as np
import sys

try: # for outside func calls, program calls
    sys.path.insert(0, './multi_glods_python/src/')
    from multiglods_ctl import one_time_init
    from multiglods_helpers import f_eval_objective_call
    from multiglods import multiglods

except:# for local, unit testing
    from multiglods_ctl import one_time_init
    from multiglods_helpers import f_eval_objective_call
    from multiglods import multiglods

class multi_glods:
        # arguments should take form: 
    # multi_glods([[float, float, ...]], [[float, float, ...]], [[float, ...]], float, int,
    # func, func,
    # dataFrame,
    # class obj, 
    # bool, [int, int, ...]) 
    #  
    # opt_df contains class-specific tuning parameters
    # BP: float
    # GP: int
    # SF: int
    #
    def __init__(self, LB, UB, TARGETS, TOL, MAXIT,
                    obj_func, constr_func, 
                    opt_df,
                    parent=None, 
                    evaluate_threshold=False, obj_threshold=None):


        #unpack the opt_df standardized vals
        BP = float(opt_df['BP'][0])
        GP = float(opt_df['GP'][0])
        SF = float(opt_df['SF'][0])
   
        #reformat since multi_glods needs single []
        LB = LB[0]
        UB = UB[0]

        # enforce typing
        NO_OF_VARS = int(len(LB))
        TOL = float(TOL)
        MAXIT = int(MAXIT)
        TARGETS = TARGETS


        #evaluation method for targets
        # True: Evaluate as true targets
        # False: Evaluate as thesholds based on information in obj_threshold
        if evaluate_threshold==False:
            THRESHOLD = None # for error checking later via wrapper

        else:
            if not(len(obj_threshold) == len(TARGETS)):
                print("WARNING: THRESHOLD option selected.  +\
                Dimensions for THRESHOLD do not match TARGET array. Defaulting to TARGET search.")
                evaluate_threshold = False
                THRESHOLD = None
            else:
                evaluate_threshold = evaluate_threshold #bool
                THRESHOLD = np.array(obj_threshold).reshape(-1, 1) #np.array
        




        self.init, self.run_ctl, self.alg, \
            self.prob, self.ctl, self.state = \
                one_time_init(NO_OF_VARS, LB, UB, TARGETS, TOL, MAXIT,
                              BP, GP, SF, obj_func, constr_func, evaluate_threshold, THRESHOLD)

        self.prob['parent'] = parent
        self.done = 0

    def step(self, suppress_output):
        self.done, self.init, self.run_ctl, \
            self.alg, self.prob, self.ctl, self.state = \
                multiglods(self.init, self.run_ctl, self.alg, 
                           self.prob, self.ctl, self.state, 
                           suppress_output)
        
   
    def call_objective(self, allow_update):
        self.state, self.prob, noErrorBool = f_eval_objective_call(self.state, 
                                                      self.prob, 
                                                      self.ctl,
                                                      allow_update)
        return noErrorBool

    def export_glods(self):
        glods_export = {'init': self.init, 'run_ctl': self.run_ctl,
                        'alg': self.alg, 'prob': self.prob,
                        'ctl': self.ctl, 'state': self.state}
        return glods_export
    
    def import_glods(self, glods_export, obj_func):
        self.init = glods_export['init']
        self.run_ctl = glods_export['run_ctl']
        self.alg = glods_export['alg']
        self.prob = glods_export['prob']
        self.ctl = glods_export['ctl']
        self.state = glods_export['state']
        self.ctl['obj_func'] = obj_func

    def complete(self):
        return self.done
    
    def get_obj_inputs(self):
        if self.state['init']:
            return self.init['x_ini']
        else:
            return self.prob['xtemp']
        
    def get_convergence_data(self):
        if len(np.shape(self.ctl['Flist'])) > 1:
            best_eval = np.linalg.norm(self.ctl['Flist'][:,0])
        else:
            best_eval = np.linalg.norm(self.ctl['Flist'])

        # return iteration for objective function call.
        #  There's several 'iter' counters.
        #  self.run_ctl['iter'] : 
        #  self.ctl['objective_iter'] : objective func call counter   
    
        iteration = 1*self.ctl['objective_iter']
        return iteration, best_eval 

    def get_optimized_soln(self):
        soln = np.vstack(self.prob['Plist'][:,0])
        return soln
    
    def get_optimized_outs(self):
        soln = np.vstack(self.ctl['Flist'][:,0])
        return soln
    

    # for plotting
    def get_search_locations(self):
        x_locations = self.prob['Plist'] 
        return x_locations

    def get_fitness_values(self):
        x_locations = self.ctl['Flist']
        return x_locations
