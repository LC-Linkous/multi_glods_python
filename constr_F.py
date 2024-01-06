#! /usr/bin/python3
import numpy as np


def constr_F(x):
    print(x)
    F = True
    if (x[2] > x[0]/2) or (x[2] < 0.1):
        F = False

    return F