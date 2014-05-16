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
"""
:use: model, inputs, outputs = parse_string(multiline_string_to_parse)
"""

import ast


def parse_string(string):
    d = get_docstring(string)
    model, inputs, outputs = parse_doc(d)
    return model, inputs, outputs


def get_docstring(string):
    M = ast.parse(string)
    return ast.get_docstring(M)


def parse_doc(docstring):
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
    inputs = None
    outputs = None
    model = None
    for docline in docstring.splitlines():
        if ("->" in docline):
            outputs = docline.split("->")[-1].split(",")
            model = docline.split("->")[0].split("(")[0]
            inputs = docline.split("(")[-1].split(")")[0].split(",")
    return model, inputs, outputs


def parse_input_and_output(docstring):
    inputs = None
    outputs = None
    if 'input' in docstring:
        in_code = docstring.split('input')[1]
        in_code = '='.join(in_code.split("=")[1:])
        line = in_code.split('\n')[0]
        inputs = line.split(",")
    if 'output' in docstring:
        out_code = docstring.split('output')[1]
        out_code = '='.join(out_code.split("=")[1:])
        line = out_code.split('\n')[0]
        outputs = line.split(",")
    return inputs, outputs


class InputObj(object):
    def __init__(self, string):
        self.name = None
        self.interface = None
        self.default = None
        if "=" in string:
            if ":" in string:
                self.name = string.split(":")[0].strip()
                self.interface = string.split(":")[1].split("=")[0].strip()
                self.default = string.split("=")[-1].strip()
            else:
                self.name = string.split("=")[0].strip()
                self.default = string.split("=")[1].strip()
        elif ":" in string:
            self.name = string.split(":")[0].strip()
            self.interface = string.split(":")[1].strip()
        else:
            self.name = string.strip()

    def __repr__(self):
        return "InputObject. Name: " + str(self.name) + ". Interface: " + str(self.interface) + ". Default Value: " + str(self.default) + "."


class OutputObj(InputObj):
    def __repr__(self):
        return "OutputObject. Name: " + str(self.name) + ". Interface: " + str(self.interface) + ". Default Value: " + str(self.default) + "."