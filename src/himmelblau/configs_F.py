#! /usr/bin/python3

##-------------------------------------------------------------------------------\
#   multi_glods_python
#   '.src/himmelblau/configs_F.py'
#   configurations for function compatable with project optimizers
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: June 1, 2025
##-------------------------------------------------------------------------------\


import sys
try: # for outside func calls
    sys.path.insert(0, './multi_glods_python/src/')
    from himmelblau.func_F import func_F
    from himmelblau.constr_F import constr_F
except: # for local
    from func_F import func_F
    from constr_F import constr_F

OBJECTIVE_FUNC = func_F
CONSTR_FUNC = constr_F
OBJECTIVE_FUNC_NAME = "himmelblau.func_F"
CONSTR_FUNC_NAME = "himmelblau.constr_F"

# problem dependent variables
LB = [[-5, -5]]             # Lower boundaries
UB = [[5, 5]]               # Upper boundaries
IN_VARS = 2                 # Number of input variables (x-values)
OUT_VARS = 1                # Number of output variables (y-values) 
TARGETS = [0]               # Target values for output
GLOBAL_MIN = [[3, 2]]       # Global minima sample, if they exist. 
# (-3.78, -3.28), (-2.81, 3.13), (3.58, -1.85), and (3, 2)