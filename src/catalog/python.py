# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
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
Data Node
"""

__license__= "Cecill-C"
__revision__=" $Id: simple_models.py 331 2007-02-02 15:50:47Z dufourko $ "



def setitem(obj, key, value):
    """ call __setitem__ on obj """
    ret = obj.__setitem__(key, value)
    return obj


def getitem(obj, key):
    """ call __getitem__ on obj"""

    ret = obj.__getitem__(key)
    return (ret,)


def delitem(obj, key):
    """ call __delitem__ on obj"""
    
    ret = obj.__delitem__(key)
    return (obj,)


def keys(obj):
    """ call keys() on obj """

    ret = obj.keys()
    return (ret,)


def values(obj):
    """ call values() on obj """

    ret = obj.values()
    return (ret,)


def items(obj):
    """ call items() on obj """

    ret = obj.items()
    return (ret,)


def append(obj, val):
    """ call append(val) on obj """

    ret = obj.append(val)
    return (obj,)


def pyrange(start, stop, step):
    """ range(start, stop, step) """

    if(start == None): start = 0
    if(stop == None): stop = 0
    if(step == None): step = 1
    return (range(start, stop, step),)


def pymap(func, seq):
    """ map(func, seq) """

    if func and seq:
        return ( map(func,seq), )
    else:
        return ( [], )


def pyfilter(func, seq):
    """ filter(func, seq) """

    if func and seq:
        return ( filter(func,seq), )
    else:
        return ( [], )


def pyreduce(func, seq):
    """ filter(func, seq) """

    if func and seq:
        return ( reduce(func,seq), )
    else:
        return ( [], )


def pylen(obj):
    """ len(obj) """

    f= None
    if callable(obj):
        f= lambda x: len(obj(x))
    else:
        f= len(obj)
    return ( f, )


