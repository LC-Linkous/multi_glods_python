#! /usr/bin/python3
import numpy as np

#unit testing vs. program call
try:
    from multglods_ctl import one_time_init
    from multiglods_helpers import f_eval_objective_call
    from multiglods import multiglods
except:
    from optimizers.GLODS.multi_glods_python.multglods_ctl import one_time_init
    from optimizers.GLODS.multi_glods_python.multiglods_helpers import f_eval_objective_call
    from optimizers.GLODS.multi_glods_python.multiglods import multiglods


class multi_glods:

    def __init__(self, NO_OF_VARS, LB, UB, BP, 
                 GP, SF, TARGETS, TOL, MAXIT, func_F, constr_func):

        self.init, self.run_ctl, self.alg, \
            self.prob, self.ctl, self.state = \
                one_time_init(NO_OF_VARS, LB, UB, BP, GP, 
                              SF, TARGETS, TOL, MAXIT, func_F, constr_func)
    
        self.done = 0

    def step(self, suppress_output):
        self.done, self.init, self.run_ctl, \
            self.alg, self.prob, self.ctl, self.state = \
                multiglods(self.init, self.run_ctl, self.alg, 
                           self.prob, self.ctl, self.state, 
                           suppress_output)
    
    def call_objective(self, parent, allow_update):
        self.prob['parent'] = parent
        self.state, self.prob = f_eval_objective_call(self.state, 
                                                      self.prob, 
                                                      self.ctl,
                                                      allow_update)
        
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
        iteration = 1*self.run_ctl['iter']
        return iteration, best_eval

    def get_optimized_soln(self):
        soln = np.vstack(self.prob['Plist'][:,0])
        return soln
    
    def get_optimized_outs(self):
        soln = np.vstack(self.ctl['Flist'][:,0])
        return soln