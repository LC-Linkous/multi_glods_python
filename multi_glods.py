#! /usr/bin/python3
from multglods_ctl import one_time_init
from multiglods import multiglods

class multi_glods:

    def __init__(self, NO_OF_VARS, LB, UB, BP, 
                 GP, SF, TARGETS, TOL, MAXIT, func_F):

        self.init, self.run_ctl, self.alg, \
            self.prob, self.ctl, self.state = \
                one_time_init(NO_OF_VARS, LB, UB, BP, GP, 
                              SF, TARGETS, TOL, MAXIT, func_F)
    
        self.done = 0

    def step(self):
        self.done, self.init, self.run_ctl, \
            self.lg, self.prob, self.ctl, self.state = \
                multiglods(self.init, self.run_ctl, self.alg, 
                           self.prob, self.ctl, self.state)