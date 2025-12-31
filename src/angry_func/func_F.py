import numpy as np

def func_F(X, NO_OF_OUTS=2):
    print("OBECTIVE FUNCTION CALLED")
    F = np.zeros((NO_OF_OUTS))
    noErrors = True
    try:
        F[0] = (X[0]-21.5) ** 3 + (X[1]+20.1) ** 2
        F[1] = (X[2]-22.2) ** 2
    except:
        noErrors = False

    print(f"NO ERROR: {noErrors}")
    return F, noErrors
    
# def func_F(X, NO_OF_OUTS=1):
#     F = np.zeros((NO_OF_OUTS))
#     noErrors = True
#     try:
#         x = X[0]
#         F = np.sin(5 * x**3) + np.cos(5 * x) * (1 - np.tanh(x ** 2))
#     except Exception as e:
#         print(e)
#         # print("X!")
#         # print(X)
#         noErrors = False
#  return F, noErrors