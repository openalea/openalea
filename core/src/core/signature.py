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


import types
import inspect

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
      
    args= []
    for i,name in enumerate(varnames):
        interface = None
        cur_default = None
        args.append(dict(name=name, interface=interface, value=cur_default))

    return args

