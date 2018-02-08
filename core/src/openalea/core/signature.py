        # -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
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
"""Signature class that instropect python functor based on the code"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


import inspect
import types
import re
import traceback
import copy
from openalea.core.interface import TypeInterfaceMap


class Signature(object):
    """Object to represent the signature of a function/method.

    :param f: a function object containing __name__ variable
    """

    def __init__(self, f):
        """ f is a function object or instance method,
        functor class are managed but need to be tested more carefully"""
        if isinstance(f, dict):   #recreate from serialised
            self.name = f.get("name")
            self.f_doc = f.get("f_doc")
            self.parameters = f.get("parameters", [])
            self.varargs  = f.get("varargs", False)
            self.keywords = f.get("keywords", False)
            self.isMethod = f.get("isMethod", False)
            self.isValid  = f.get("isValid", True)
        elif isinstance(f, Signature):  #copy contructor
            self.name = f.name
            self.f_doc = f.f_doc
            self.parameters = copy.deepcopy(f.parameters)
            self.varargs  = f.varargs
            self.keywords = f.keywords
            self.isMethod = f.isMethod
            self.isValid  = f.isValid
        else: #normal function inspection
            self.name = f.__name__
            self.f_doc = inspect.getdoc(f)
            self.parameters = []
            self.varargs  = None
            self.keywords = None
            self.isMethod = False
            self.isValid  = True

            try:
                # -- inspect the callable
                args, defaults, varargs, keywords, self.isMethod = Signature.get_callable_arguments(f)

                # -- the signature might have not been resolved
                # however, we might not want to raise an exception
                # so we put the isValid flag to false and stop the init.
                if args==defaults==varargs==keywords==self.isMethod==-1:
                    self.isValid = False
                    return

                # -- create a set out of the default arg names for later reference
                defaultArgNames = [] if len(defaults)==0 else set(zip(*defaults)[0])

                # -- create parameters that do not have defaults (not in defaultArgNames)
                for arg in args:
                    if arg not in defaultArgNames:
                        self.parameters.append(dict(name=arg, interface=None,
                                                    value=None))

                # -- create parameters that have defaults
                for arg, val in defaults:
                    interface = TypeInterfaceMap().get(type(val), None)
                    self.parameters.append(dict(name=arg, interface=interface,
                                                value=val))

                # -- do we have varargs? (*args)
                if varargs is not None:
                    self.varargs = {"varargs":arg, "interface": "ISequence", "value":[]}

                # -- do we have keyword args? (**kwargs)
                if keywords is not None:
                    self.keywords = {"keywords":arg, "interface":"IDict","value":{}}

            except Exception, e:
                traceback.print_exc()



    def __repr__(self):
        return "{'name':"      +repr(self.name)       +", " + \
               "'f_doc':"      +repr(self.f_doc)      +", " + \
               "'parameters':" +repr(self.parameters) +", " + \
               "'varargs':"    +repr(self.varargs)    +", " + \
               "'keywords':"   +repr(self.keywords)   +", " + \
               "'isMethod':"   +repr(self.isMethod)   +", " + \
               "'isValid':"    +repr(self.isValid)    +"}"

    def get_name(self):
        return self.name

    def get_doc(self):
        return self.f_doc

    def get_parameters(self, eludeSelf=True):
        if eludeSelf and self.isMethod:
            return self.parameters[1:]
        else:
            return self.parameters[:]

    def get_returns(self):
        """ Return the outputs of a functor based on a predifened contract.
        TO BE DEFINED
        TODO
        """
        return dict(name="out", interface=None), 

    def get_varargs(self):
        return self.varargs

    def get_keywords(self):
        return self.keywords

    def get_all_parameters(self, eludeSelf=True):
        params = self.get_parameters(eludeSelf=eludeSelf)
        if self.varargs:
            params += [self.varargs]
        if self.keywords:
            params += [self.keywords]
        return params

    @staticmethod
    def get_callable_arguments(function):
        """ Static method that returns 5 values for one entry object which can be
        any callable. The returned 5-uple is as follows:
        0 - list-of-simple-arguments. Can be an empty list.
        1 - list-of-(argname,argvalue)-arguments-with-defaults. Can be an empty list.
        2 - name-of-vararg-argument. Can be None.
        3 - name-of-keyword-argument. Can be None.
        5 - boolean : True if function is a method, False otherwise...
        For Python defined callables, uses the "inspect" module. For builtins, tries
        some regexp parsing of the docstring.
        """
        isMethod = inspect.ismethod(function)
        if isMethod or inspect.isfunction(function):
            argspec  = inspect.getargspec(function)
            if argspec.defaults:
                ndefs    = len(argspec.defaults)
                args     = argspec.args[:-ndefs]
                defaults = zip(argspec.args[-ndefs:], argspec.defaults)
            else:
                args     = argspec.args
                defaults = []
            return args, defaults, argspec.varargs, argspec.keywords, isMethod

        elif inspect.isbuiltin(function):
            # builtins have no argument description
            # we can only try to do some rough docstring parsing.
            args, defaults, varargs, keywords = Signature.regexp_args(function)
            return args, defaults, varargs, keywords, False

        elif inspect.isclass(function) and "__call__" in function.__dict__:
            func = function.__call__
            return Signature.get_callable_arguments(func)

        elif isinstance(function, types.InstanceType) and "__call__" in function.__dict__:
            func = function.__call__
            return Signature.get_callable_arguments(func)
        else:
            return -1,-1,-1,-1,-1

    @staticmethod
    def regexp_args(function):
        assert inspect.isbuiltin(function)
        name = function.__name__
        re_str = r"\s*.*"+name+r"\s*\(([(){}\[\]a-zA-Z0-9*='\",\s]*)\).*"
        m = re.match(re_str, inspect.getdoc(function))

        args, defaults, varargs, keywords = [], [], None, None
        if m is not None:
            prototype = [ s.strip() for s in  m.groups()[0].split(",") ]
            for arg in prototype:
                if "=" in arg:
                    n,v = arg.split("=")
                    try:
                        v = eval(v)
                    except:
                        pass
                    defaults.append([n,v])
                elif len(arg)>0:
                    starCount = arg.count("*")
                    if starCount == 0:
                        args.append(arg)
                    elif starCount == 1:
                        varargs = arg
                    elif starCount == 2:
                        keywords = arg
                    else:
                        raise Exception("Unknown argument type : "+arg)
        return args, defaults, varargs, keywords


