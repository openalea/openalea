""" here is a dummy documentation"""


import os


def square(a):
    """short description of the function square

    longish explanation: returns the square of a: :math:`a^2`

    :param a: an input argument

    :returns: a*a
    """
    return a*a

assert 4 == square(2)
