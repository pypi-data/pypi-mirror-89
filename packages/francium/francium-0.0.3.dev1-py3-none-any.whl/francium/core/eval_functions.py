import numpy as np


def convex_x_square(X, Y):
    return X ** 2 + Y ** 2


def sinx_plus_x(X, Y):
    return 5 * np.sin(X ** 2 + Y ** 2) + (X ** 2 + Y ** 2)
