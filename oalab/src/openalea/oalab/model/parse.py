# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
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
from openalea.core.model_inout import (InputObj, OutputObj,
    parse_input_and_output, ast_parse, parse_docstring, get_docstring,
    parse_doc, extract_functions, parse_function, parse_doc_in_code)
import textwrap
import collections
from copy import copy

#########################################
# Function to define to parse r model
#########################################


def parse_docstring_r(code):
    """
    parse a string (not a docstring), get the docstring and return information on the model.

    :use: model, inputs, outputs = parse_docstring_r(multiline_string_to_parse)

    :param string: docstring to parse (string)
    :return: model, inputs, outputs
    """

    def parse_cmdline(comment):
        line = ''
        if 'cmdline' in comment:
            line = comment.split('cmdline')[1]
            line = line.split('=')[1]
            line = line.split('\n')[0].strip()
        return line

    comment = get_docstring_r(code)
    inputs, outputs = parse_input_and_output(comment)
    if inputs:
        inputs = map(InputObj, inputs)
    if outputs:
        outputs = map(OutputObj, outputs)

    cmdline = parse_cmdline(comment)
    return 'Rfunction', inputs, outputs, cmdline


def get_docstring_r(code):
    """
    Get a docstring from a code text
    """
    comments = []
    for l in code.splitlines():
        l = l.strip()
        if l and l.startswith('#'):
            comments.append(l)
        elif l != '':
            break

    return '\n'.join(comments)


def parse_functions_r(docstring):
    """
    Parse a docstring with format:
        my_model(a:int=4, b)->r:int

    Unused.

    :return: model, inputs, outputs
    """

    # TODO
    # print '-> parse_functions_r', docstring
    return False, True, True, True



#########################################
# Detect inputs and outputs in docstring
#########################################


parse_lpy = parse_doc_in_code



def prepare_inputs(inputs_info, *args, **kwargs):
    """
    >>> from openalea.oalab.model.parse import InputObj
    >>> inputs_info = [InputObj('a:int=1'), InputObj('b:int=2')]
    >>> prepare_inputs(inputs_info) # doctest: +SKIP
    {'a':1, 'b':2}
    >>> prepare_inputs(inputs_info, 10) # doctest: +SKIP
    {'a':10, 'b':2}
    >>> prepare_inputs(inputs_info, 10, 20) # doctest: +SKIP
    {'a':10, 'b':20}
    """
    filename = kwargs.pop('name', "unknown")
    # TODO: refactor with types.FunctionType
    _inputs = dict()
    if inputs_info:
        not_set_inputs_info = copy(inputs_info)  # Use it to know what we have to set and what is yet set

        # Set positional arguments
        if args:
            inputs = list(args)
            if len(inputs) == 1:
                if isinstance(inputs, collections.Iterable):
                    inputs = inputs[0]
                elif isinstance(inputs, collections.Iterable):
                    inputs = list(inputs)
                inputs = [inputs]
            inputs.reverse()

            if inputs_info:
                for input_info in inputs_info:
                    if len(inputs):
                        default_value = inputs.pop()
                        if input_info.name:
                            _inputs[input_info.name] = default_value
                        not_set_inputs_info.remove(input_info)
                    else:
                        break

        # Set non-positional arguments
        if kwargs:
            if len(not_set_inputs_info):
                not_set_inputs_info_dict = dict((inp.name, inp) for inp in not_set_inputs_info)
                for name in kwargs:
                    value = kwargs[name]
                    if name in not_set_inputs_info_dict.keys():
                        _inputs[name] = value
                        not_set_inputs_info.remove(not_set_inputs_info_dict[name])
                        del not_set_inputs_info_dict[name]
                    else:
                        msg = "We can not put %r inside inputs of model %r" % (name, name)
                        msg += " because such an input is not declared in the model."
                        raise Exception(msg)

        # Fill others with defaults
        if len(not_set_inputs_info):
            for input_info in copy(not_set_inputs_info):
                if input_info.default:
                    default_value = eval(input_info.default)
                    _inputs[input_info.name] = default_value
                    not_set_inputs_info.remove(input_info)

        # If one argument is missing, raise
        if len(not_set_inputs_info):
            raise Exception("Model '%s' have inputs not set. Please set %s." %
                            (filename, [inp.name for inp in not_set_inputs_info]))

    return _inputs

################################
# Detect functions in docstring
################################


def parse_functions(codestring):
    """
    Parse the code *codestring* and detect what are the functions defined inside:
      - Search *init*, *step*, *animate* and *run*
    :return: init, step, animate, run  functions (code or False)
    """
    exec_funcs = {}
    exec_funcs_names = ['init', 'step', 'animate', 'run']
    for func_name in exec_funcs_names:
        exec_funcs[func_name] = False

    r = ast_parse(codestring)
    functions_list = [x for x in ast.walk(r) if isinstance(x, ast.FunctionDef)]
    for x in functions_list:
        if x.name in exec_funcs_names:
            wrapped = ast.Interactive(body=x.body)
            try:
                code = compile(wrapped, 'tmp', 'single')
            except:
                pass
            else:
                exec_funcs[x.name] = code

    exec_funcs_list = [exec_funcs[func_name] for func_name in exec_funcs_names]
    return exec_funcs_list
