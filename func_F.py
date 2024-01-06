#! /usr/bin/python3
import numpy as np


def func_F(parent, x):
    parent = parent
    NO_OF_OUTS = 2
    F = np.zeros((NO_OF_OUTS, 1))
    F[0] = (x[0]-0.5) ** 2 + (x[1]-0.1) ** 2
    F[1] = (x[2]-0.2) ** 4 

    return F
