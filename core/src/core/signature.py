# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2008 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
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
from openalea.core.interface import TypeInterfaceMap


class Signature(object):
    """Object to represent the signature of a function/method.

    :param f: a function object containing __name__ variable
    """

    def __init__(self, f):
        """ f is a function object or instance method, 
        functor class are managed but need to be tested more carefully"""
        
        self.name = f.__name__
        self.parameters = []
        
        try:
            #if f is an instance method
            if( inspect.ismethod(f)):
                func = f.im_func
                spec = inspect.getargspec(func)
                varnames = spec[0][1:]

            #if f is a function
            elif(inspect.isfunction(f)):
                func = f
                spec = inspect.getargspec(func)
                varnames = spec[0]

            elif(inspect.isclass(f) and hasattr(f, '__call__')):
                func = f.__call__
                spec = inspect.getargspec(func) 
                # modules have __call__ method but getargspec won't work !

                varnames=spec[0][1:]
            else:
                raise TypeError

            default_values = spec[3] or []

            parameters = []
            nv = len(varnames)
            nd = len(default_values)
            # parse args without default value
            for i,name in enumerate(varnames[:nv - nd]):
                self.parameters.append(dict(name=name, interface=None, value=None))

            # parse args with default value
            for i,name in enumerate(varnames[nv - nd:]):
                df = default_values[i]
                interface = TypeInterfaceMap().get(type(df),None)
                self.parameters.append(dict(name=name, interface=interface, value=df))

        except Exception, e:
            print e
        
    def get_name(self):
        return self.name

    def get_parameters(self):
        return self.parameters


#def get_parameters(f):
#    """ Return the list of
#    dict(name='name', interface=None, value=None) corresponding
#    to the function parameters """
#
#    try:
#        # if f is a class
#        if(not isinstance(f, types.FunctionType)):
#            specs = inspect.getargspec(f.__call__)
#            varnames = specs[0]
#            varnames = varnames[1:]
#            defaults = specs[3]
#            
#        # f is a function
#        else:
#            specs = inspect.getargspec(f)
#            varnames = specs[0]
#            defaults = f.func_defaults
#            defaults = specs[3]
#
#    except Exception, e:
#        print e
#        return ()
#
#    if(defaults == None): defaults = []
#    if(varnames == None): varnames = []
#    
#    args= []
#    nv = len(varnames)
#    nd = len(defaults)
#    # parse args without default value
#    for i,name in enumerate(varnames[:nv - nd]):
#        args.append(dict(name=name, interface=None, value=None))
#
#    # parse args with default value
#    for i,name in enumerate(varnames[nv - nd:]):
#        v = defaults[i]
#        interface = TypeInterfaceMap().get(type(v),None)
#        args.append(dict(name=name, interface=interface, value=v))
#
#    return args

