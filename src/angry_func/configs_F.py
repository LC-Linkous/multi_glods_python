import sys
try: # for outside func calls
    sys.path.insert(0, './multi_glods_python/src/')
    # from objective_funcs.angry_func.func_F import func_F
    # from objective_funcs.angry_func.constr_F import constr_F
    from angry_func.func_F import func_F
    from angry_func.constr_F import constr_F
except: # for local
    from func_F import func_F
    from constr_F import constr_F

OBJECTIVE_FUNC = func_F
CONSTR_FUNC = constr_F
OBJECTIVE_FUNC_NAME = "angry_func.func_F"
CONSTR_FUNC_NAME = "angry_func.constr_F"

# multi variable
# problem dependent variables
# LB = [[-6, -6.5, -6]]       # Lower boundaries for input
# UB = [[21, 21, 20]]          # Upper boundaries for input
# IN_VARS = 3                 # Number of input variables (x-values)
# OUT_VARS = 2                # Number of output variables (y-values)
# TARGETS = [-2, 15]            # Target values for output
# GLOBAL_MIN = None           # Global minima, if they exist

LB = [[-6.0, -6.5, -6.0]]       # Lower boundaries for input
UB = [[21.0, 21.0, 20.0]]          # Upper boundaries for input
IN_VARS = 3                 # Number of input variables (x-values)
OUT_VARS = 2                # Number of output variables (y-values)
TARGETS = [0.0, 0.0]            # Target values for output
GLOBAL_MIN = None           # Global minima, if they exist

# single variable
#  # problem dependent variables
# LB = [[0]]             # Lower boundaries
# UB = [[1]]               # Upper boundaries
# IN_VARS = 1                 # Number of input variables (x-values)
# OUT_VARS = 1                # Number of output variables (y-values) 
# TARGETS = [0]               # Target values for output
# GLOBAL_MIN = []       # Global minima sample, if they exist. 