# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
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
###############################################################################

__doc__="""
Signature class that instropect python functor based on the code
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


import inspect
import types
from interface import TypeInterfaceMap


class Signature(object):
    """ Instrospect function objects """

    def __init__(self, func):
        """ func is a function object or a functor class """




def get_parameters(f):
    """ Return the list of
    dict(name='name', interface=None, value=None) corresponding
    to the function parameters """

    try:
        # if f is a class
        if(not isinstance(f, types.FunctionType)):
            specs = inspect.getargspec(f.__call__)
            varnames = specs[0]
            varnames = varnames[1:]
            defaults = specs[3]
            
        # f is a function
        else:
            specs = inspect.getargspec(f)
            varnames = specs[0]
            defaults = f.func_defaults
            defaults = specs[3]

    except Exception, e:
        print e
        return ()

    if(defaults == None): defaults = []
    if(varnames == None): varnames = []
    
    args= []
    nv = len(varnames)
    nd = len(defaults)
    # parse args without default value
    for i,name in enumerate(varnames[:nv - nd]):
        args.append(dict(name=name, interface=None, value=None))

    # parse args with default value
    for i,name in enumerate(varnames[nv - nd:]):
        v = defaults[i]
        interface = TypeInterfaceMap().get(type(v),None)
        args.append(dict(name=name, interface=interface, value=v))

    return args

