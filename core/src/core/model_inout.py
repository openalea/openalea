# -*- python -*-
#
#       OpenAlea.Core: Multi-Paradigm GUI
#
#       Copyright 2014-2017 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.pradal@cirad.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
import ast
import re
from openalea.core import logger
from openalea.core.service.interface import interface_class, guess_interface
import textwrap
import collections
from copy import copy


###########################
# Input and Output Objects
###########################
class InputObj(object):

    """
    Inputs object with:
        - an attribute *name*: name of the input obj (str) (mandatory)
        - an attribute *interface*: interface/type of the input obj (str) (optional)
        - an attribute *default*: default value of the input obj (str) (optional)

    >>> from openalea.oalab.model.parse import InputObj
    >>> obj = InputObj('a:float=1')
    >>> obj.name
    'a'
    >>> obj.default
    '1'
    >>> obj.interface
    IFloat
    >>> obj
    InputObj('a:IFloat=1')

    :param string: string object with format "input_name:input_type=input_default_value" or "input_name=input_default_value" or "input_name:input_type" or "input_name"
    """

    def __init__(self, string=''):
        self.name = None
        self.interface = None
        self.default = None
        if "=" in string:
            if ":" in string:
                self.name = string.split(":")[0].strip()
                interf = ":".join(string.split(":")[1:])
                self.interface = interf.split("=")[0].strip()
                self.default = "=".join(string.split("=")[1:]).strip()
            else:
                self.name = string.split("=")[0].strip()
                self.default = "=".join(string.split("=")[1:]).strip()
        elif ":" in string:
            self.name = string.split(":")[0].strip()
            self.interface = ":".join(string.split(":")[1:]).strip()
        else:
            self.name = string.strip()

        set_interface(self)

    def __str__(self):
        return self.__class__.__name__ + ". Name: " + str(self.name) + ". Interface: " + str(self.interface) + ". Default Value: " + str(self.default) + "."

    def repr_code(self):
        string = self.name
        if self.interface:
            string += ":%s" % self.interface
        if self.default:
            string += "=%s" % self.default
        return string

    def __repr__(self):
        classname = self.__class__.__name__
        return "%s(%r)" % (classname, self.repr_code())


def set_interface(input_obj):
    if input_obj.interface is None:
        if isinstance(input_obj.default, str):
            try:
                default_eval = eval(input_obj.default)
                input_obj.interface = guess_interface(default_eval)
            except SyntaxError:
                input_obj.interface = guess_interface(input_obj.default)
        else:
            input_obj.interface = guess_interface(input_obj.default)
    else:
        try:
            input_obj.interface = interface_class(input_obj.interface)
        except ValueError:
            input_obj.interface = guess_interface(input_obj.default)
    if input_obj.interface == []:
        input_obj.interface = None
    elif isinstance(input_obj.interface, list):
        input_obj.interface = input_obj.interface[0]


class OutputObj(InputObj):
    pass


