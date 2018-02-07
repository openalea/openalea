        # -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): 
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""Signature class that instropect python functor based on the code"""

__license__ = "Cecill-C"
__revision__ = " $Id:  $ "

from openalea.core import funcsigs
from openalea.core.signature import Signature as OldSignature
from openalea.core.interface import TypeInterfaceMap, TypeNameInterfaceMap
from collections import OrderedDict

"""
class Signature(OldSignature):
    def __init__(self, f):
        super(Signature, self).__init__(f)
        self.outputs = None
        
        # TODO : use funcsigs.signature to complete
        
        if hasattr(f, __inputs__):
            self.parameters = f.__inputs__
        if hasattr(f, __outputs__):
            self.outputs = f.__outputs__
"""
        

def sign_inputs(f):
    """
    Return list of inputs detected from f.__inputs__
    """
    new_inputs = []
    if hasattr(f, "__inputs__"):
        inputs = f.__inputs__
        if isinstance(inputs, str):
            new_inputs += sign_from_string(f, f.__inputs__)

        if isinstance(inputs, list):
            for input_ in inputs:
                new_inputs += sign_from_string(f, input_)
            
    return new_inputs
    
def sign_outputs(f):
    """
    Return list of outputs detected from f.__outputs__
    """
    new_outputs = []
    if hasattr(f, "__outputs__"):
        outputs = f.__outputs__
        if isinstance(outputs, str):
            new_outputs += sign_from_string(f, f.__outputs__)

        if isinstance(outputs, list):
            for output in outputs:
                new_outputs += sign_from_string(f, output)
            
    return new_outputs

def sign_from_string(f, string):
    inputs = string
    new_inputs = []
    inps = inputs.split(",")
    for inp in inps:
        n = ""
        v = None
        interface = None
        
        inpsplit = inp.split("=")
        
        if len(inpsplit) == 2:
            v = inpsplit[1]
            inpsplit2 = inpsplit[0].split(":")
            # Case "a=4"
            if len(inpsplit2) == 1:
                n = inpsplit2[0]
                p = eval(v)
                interface = TypeInterfaceMap().get(type(p),None)
            # Case "a:int=4"
            elif len(inpsplit2) == 2:
                n = inpsplit2[0]
                interface = inpsplit2[1]
                try:
                    p = eval("%s()"%interface)
                    interface = TypeInterfaceMap().get(type(p),None)
                except:
                    pass
        else:
            inpsplit = inp.split(":")
            # Cases "a"
            if len(inpsplit) == 1:
                n = inpsplit[0]
                v = None
                interface = TypeInterfaceMap().get(type(v),None)
            # Cases "a:int"
            elif len(inpsplit) == 2:
                n = inpsplit[0]
                v = None
                interface = inpsplit[1]

        new_inputs.append(dict(name=n, interface=interface, value=v))
            
    return new_inputs
