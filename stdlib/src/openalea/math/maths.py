# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
""" Math Nodes """

__license__ = "Cecill-C"
__revision__ = " $Id$ "



from openalea.core import *



def py_cmp(a=0.,b=0.):
    """ cmp(a,b) """
    return cmp(a,b)


def py_round(x=0.,n=1):
    """ round(x,n) """
    return round(x,n)


def py_min(l=[]):
    """ min(l) """
    return min(l)


def py_max(l=[]):
    """ max(l) """
    return max(l)

    
def py_randlist(a=0, b=100, size=10):
    """Return a list of size 'size' of random integer in range [a, b(."""
    import random
    a = int(a)
    b = int(b)
    return ([random.randrange(a, b) for i in xrange(size)],)
