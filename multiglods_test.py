#! /usr/bin/python3
from multi_glods import multi_glods
from func_F import func_F

NO_OF_VARS = 3
TOL = 10 ** -3
LB = [0, 0, 0]
UB = [1, 1, 1]
BP = 0.5
GP = 1
SF = 2
TARGETS = [0, 0]
MAXIT = 3000

myGlods = multi_glods(NO_OF_VARS, LB, UB, BP, GP, 
                      SF, TARGETS, TOL, MAXIT, func_F)

while not myGlods.done:
    myGlods.step()