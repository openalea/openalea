# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Mathematics
"""

__license__= "Cecill-C"
__revision__=" $Id$ "



from openalea.core import *


def py_equal(a, b):
    """ a == b """
    return a == b


def py_greater(a,b):
    """ a > b """
    return a > b
        

def py_greater_or_equal(a,b):
    """ a >= b """
    return a >= b 


def py_and(a,b):
    """ Boolean AND : a and b """
    return a and b

def py_or(a,b):
    """ Boolean OR : a or b """
    return a or b


def py_not(a):
    """ Boolean Not : not a """
    return not a


################################################################################

def py_add(a=0.,b=0.):
    """ a + b """
    return a + b


def py_sub(a=0.,b=0.):
    """ a - b """
    return a - b


def py_mult(a=0.,b=0.):
    """ a * b """
    return a * b


def py_div(a=0.,b=1.):
    """ a / b """
    return a / b


def py_abs(a=0.):
    """ abs(a) """
    return abs(a)


def py_cmp(a=0.,b=0.):
    """ cmp(a,b) """
    return cmp(a,b)


def py_pow(a=0.,b=1):
    """ pow(a,b) """
    return pow(a,b)


def py_round(x=0.,n=1):
    """ round(x,n) """
    return round(x,n)


def py_min(l=[]):
    """ min(l) """
    return min(l)


def py_max(l=[]):
    """ max(l) """
    return max(l)


def py_randint(a=0, b=100):
    """Return random integer in range [a, b], including both end points."""
    import random
    return random.randint(a,b)
    
