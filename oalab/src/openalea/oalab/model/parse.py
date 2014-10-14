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
from openalea.core.service.interface import interface_class, guess_interface
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
# Safe ast parsing
#########################################


def ast_parse(string):
    logger.debug("Parse code: " + string[:10] + "...")
    try:
        M = ast.parse(string)
    except SyntaxError, e:
        #raise e
        logger.warning(str(e))
        wraper = textwrap.TextWrapper(width=30)
        txt = wraper.wrap(string)[0]  # Python 2
        # txt = textwrap.shorten(string, width=30, placeholder="...") # Python 3
        logger.warning("Syntax error when parsing: " + txt + "...")
        M = ast.parse("")
    return M


#########################################
# Detect inputs and outputs in docstring
#########################################
def parse_docstring(string):
    """
    parse a string (not a docstring), get the docstring and return information on the model.

    :use: model, inputs, outputs = parse_docstring(multiline_string_to_parse)

    :param string: docstring to parse (string)
    :return: model, inputs, outputs
    """
    d = get_docstring(string)
    model, inputs, outputs = parse_doc(d)
    return model, inputs, outputs


def get_docstring(string):
    """
    Get a docstring from a string
    """
    M = ast_parse(string)
    docstring = ast.get_docstring(M)
    if docstring is not None:
        return docstring

    return parse_lpy(string)


def parse_doc(docstring):
    """
    Parse a docstring.

    :return: model, inputs, outputs
    """
    model, inputs, outputs = parse_function(docstring)

    inputs2, outputs2 = parse_input_and_output(docstring)

    # TODO: make a real beautifull merge
    if inputs2:
        inputs = inputs2
    if outputs2:
        outputs = outputs2

    ret_inputs = None
    ret_outputs = None
    if inputs:
        ret_inputs = [InputObj(inp) for inp in inputs]
    if outputs:
        ret_outputs = [OutputObj(outp) for outp in outputs]

    return model, ret_inputs, ret_outputs


def parse_function(docstring):
    """
    Parse a docstring with format:
        my_model(a:int=4, b)->r:int

    Unused.

    :return: model, inputs, outputs
    """
    inputs = None
    outputs = None
    model = None
    if hasattr(docstring, "splitlines"):
        for docline in docstring.splitlines():
            if ("->" in docline):
                outputs = docline.split("->")[-1].split(",")
                model = docline.split("->")[0].split("(")[0]
                inputs = docline.split("(")[-1].split(")")[0].split(",")
    return model, inputs, outputs


def _replace_regex(line, regex, replaced="_"):
    """
    Search *regex* inside *line* and replace it by *replaced*

    :return: line replaced
    :use:
    >>> line = "a=(1,2,3), b=[1,2], c=4, d=([1,2,3],4)"
    >>> _replace_regex(line, "\([A-Za-z0-9_,()]*\)", "_")
    >>> "a=_______, b=[1,2], c=4, d=___________"
    """
    line2 = line
    search = re.search(regex, line2)
    while search is not None:
        start = search.start()
        end = search.end()
        n = end - start
        # Replace found part by n*"_"
        line2 = line2[:start] + (n * replaced) + line2[end:]
        # Search again
        search = re.search(regex, line2)
    return line2


def _replace_bracket(line):
    # Search something with
    #   - one opening bracket (
    #   - what you want
    #   - one closing bracket )
    return _replace_regex(line, "\([A-Za-z0-9_,()]*\)")


def _replace_square_bracket(line):
    # Search something with
    #   - one opening square bracket [
    #   - what you want
    #   - one closing square bracket ]
    return _replace_regex(line, "\[[A-Za-z0-9_,()]*\]")


def _replace_quoted(line):
    # Search something with
    #   - one opening quote '
    #   - what you want
    #   - one closing quote '
    return _replace_regex(line, "\'\s*([^\"]*?)\s*\'")


def _replace_double_quoted(line):
    # Search something with
    #   - one opening quote "
    #   - what you want
    #   - one closing quote "
    return _replace_regex(line, "\"\s*([^\"]*?)\s*\"")


def _safe_split(line):
    """
    Split a text by ",",
    Manage case where you have a list, a tuple, a string, ...

    :param line: text line to split (str)
    :return: splitted line (list)

    :use:
    >>> line = "a=(1,2,3), b=[1,2], c=4, d=([1,2,3],4)"
    >>> _safe_split(line)
    >>> ["a=(1,2,3)", "b=[1,2]", "c=4", "d=([1,2,3],4)"]
    """
    line2 = line
    line2 = _replace_bracket(line2)
    line2 = _replace_square_bracket(line2)
    line2 = _replace_quoted(line2)
    line2 = _replace_double_quoted(line2)

    # Resulting object is something without (square) bracket
    # "a=[1,2,3], b=(1,2), c=1" become "a=_______, b=_____, c=1"
    # Split object that have no special character (no bracket, no square bracket)
    line_without_specials_splitted = line2.split(',')

    # Stock places where split occurred
    i = 0
    virgule_places = []
    for part in line_without_specials_splitted:
        i = i + len(part) + 1
        virgule_places.append(i)

    # Come back to **first object** and split it at the places **virgule_places**
    final_lines = []
    old = 0
    for virgule_place in virgule_places:
        final_lines.append(line[old:virgule_place - 1])
        old = virgule_place

    # Simple strip
    return [x.strip() for x in final_lines]


def parse_input_and_output(docstring):
    """
    Parse a docstring with format:
        inputs = input_name:input_type=input_default_value, ...
        outputs = output_name:output_type, ...

    :use:
        >>> comment = '''
        >>> inputs = a:int=4, b
        >>> outputs = r:float
        >>> '''
        >>> inputs, outputs = parse_input_and_output(comment)
        >>> inputs
        ['a:int=4', 'b']
        >>> outputs
        ['r:float']

    :return: inputs, outputs
    """
    inputs = []
    outputs = []
    if hasattr(docstring, "splitlines"):
        docsplit = docstring.splitlines()
        for line in docsplit:
            line = line.strip()
            if re.search('^input\s*=', line):
                line = "input".join(line.split('input')[1:])
                line = "=".join(line.split('=', 1)[1:]).strip()
                inputs = _safe_split(line)
            if re.search('^output\s*=', line):
                line = "output".join(line.split('output')[1:])
                line = line.split('=', 1)[1].strip()
                outputs = _safe_split(line)
    return inputs, outputs


def parse_lpy(string):
    """
    Take a lpy string_file, parse it and return only the docstring of the file.

    :param string: string representation of lpy file
    :return: docstring of the file if exists (must be a multiline docstring!). If not found, return None.

    :use:
        >>> f = open(lpyfilename, "r")
        >>> lpystring = f.read()
        >>> f.close()
        >>>
        >>> docstring = parse_lpy(lpystring)
        >>>
        >>> from openalea.oalab.model.parse import parse_doc
        >>> if docstring is not None:
        >>>     model, inputs, outputs = parse_doc(docstring)
        >>>     print "model : ", model
        >>>     print "inputs : ", inputs
        >>>     print "outputs : ", outputs
    """
    # TODO: need a code review
    begin = None
    begintype = None
    doclines = string.splitlines()
    i = 0
    for docline in doclines:
        i += 1
        if docline == '"""':
            begin = i
            begintype = '"""'
            break
        elif docline == "'''":
            begin = 1
            begintype = "'''"
            break
        elif docline == '"""':
            begin = 2
            begintype = '"""'
            break
        elif docline == "'''":
            begin = 2
            begintype = "'''"
            break

    if begin is not None:
        end = begin - 1
        for docline in doclines[begin:]:
            end += 1
            if docline == begintype:
                docstrings = doclines[begin:end]
                return "\n".join(docstrings)
    return None


###########################
# Input and Output Objects
###########################
class InputObj(object):

    """
    Inputs object with:
        - an attribute *name*: name of the input obj (str) (mandatory)
        - an attribute *interface*: interface/type of the input obj (str) (optional)
        - an attribute *default*: default value of the input obj (str) (optional)

    >>> obj = InputObj('a:float=1')
    >>> obj.name
    'a'
    >>> obj.default
    1
    >>> obj.interface
    'IFloat'

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


def prepare_inputs(inputs_info, *args, **kwargs):
    """
    >>> inputs_info = [InputObj('a:int=1'), InputObj('b:int=2')]
    >>> prepare_inputs(inputs_info) #DOCTEST: +IGNORE
    {'a':1, 'b':2}
    >>> prepare_inputs(inputs_info, 10) #DOCTEST: +IGNORE
    {'a':10, 'b':2}
    >>> prepare_inputs(inputs_info, 10, 20) #DOCTEST: +IGNORE
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
                        raise Exception("We can not put ", name, "inside inputs of model", name,
                                        "because such an input is not declared in the model.")

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
    parse the code *codestring* and detect what are the functions defined inside (search *init*, *step*, *animate* and *run*)
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
            wrapped = ast.Interactive(body=[x.body[-1]])
            try:
                code = compile(wrapped, 'tmp', 'single')
            except:
                pass
            else:
                exec_funcs[x.name] = code

    exec_funcs_list = [exec_funcs[func_name] for func_name in exec_funcs_names]
    return exec_funcs_list
