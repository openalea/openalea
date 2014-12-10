# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#                       Guillaume Baty <guillaume.baty@inria.fr>
#                       Christophe Pradal <christophe.pradal@inria.fr>
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
from openalea.core.model import PythonModel
from openalea.core.data import Data
from openalea.oalab.model.parse import parse_docstring_r, get_docstring_r, parse_functions_r

# TODO : refactor (like class PythonModel in python.py)


class RFile(Data):
    default_name = "R"
    default_file_name = "script.r"
    pattern = "*.r"
    extension = "r"
    icon = ":/images/resources/RLogo.png"
    mimetype = "text/x-r"


class RModel(PythonModel):
    default_name = "R"
    default_file_name = "script.r"
    pattern = "*.r"
    extension = "r"
    icon = ":/images/resources/RLogo.png"
    mimetype = "text/x-r"
    dtype = "R"

    def __copy__(self):
        m = PythonModel.__copy__(self)
        m.set_code(self._initial_code)
        return m

    def repr_code(self):
        try:
            return self._initial_code
        except AttributeError:
            code = ''
            if self.inputs_info:
                code += '# input = %s\n' % (', '.join([inp.repr_code() for inp in self.inputs_info]))
            if self.outputs_info:
                code += '# output = %s\n' % (', '.join([out.repr_code() for out in self.outputs_info]))
            if 'step' in self._code:
                code += self._code['step'] + '\n'
            for fname in ['init', 'run', 'animate', 'stop']:
                if fname in self._code:
                    code += '%s <- function(){\n' % fname
                    for l in self._code[fname].split('\n'):
                        code += '    ' + l + '\n'
                    code += '}'
            return code

    def r_options(self, namespace):
        cmd = self.cmdline
        l = self.inputs_info
        input_names = [input.name for input in l]
        input_names = [name for name in input_names if name in namespace]
        #input_values = [input.split('=')[1] for input in l]

        if input_names:
            cmd += ' -i %s' % (','.join(input_names))

        l = self.outputs_info
        output_names = [input.name for input in l]
        if output_names:
            cmd += ' -o %s' % (','.join(output_names))

        print cmd

        return cmd

    def _load_r_magic(self):
        if not self.has_run:
            try:
                # better as it solves display error but needs rpy2 > 2.4.2
                self.interp.shell.run_line_magic('load_ext', 'rpy2.ipython')
            except ImportError:
                self.interp.shell.run_line_magic('load_ext', 'rmagic')

    def _universal_run(self, code, *args, **kwargs):
        """ This method is used by others...
        """
        self._push_ns()
        self._fill_namespace(*args, **kwargs)

        cmdline = self.r_options(self._ns)

        self._load_r_magic()
        self.interp.shell.run_cell_magic('R', cmdline, code)

        self._populate_ns()
        self._pop_ns()

        # Set outputs after execution
        self.outputs = self.output_from_ns(self._ns)
        return self.outputs

    def execute(self, code):
        """
        execute subpart of a model (only code *code*)
        """
        return self._universal_run(code)

    def run(self, *args, **kwargs):
        """
        execute entire model
        """
        # TODO: check if we can do by an other way for inputs, outputs (ex %%R -i inputs, -o outputs)

        self._universal_run(self._initial_code, *args, **kwargs)
        self.has_run = True
        return self.outputs

    def init(self, *args, **kwargs):
        """
        go back to initial step
        """
        if not self.has_run:
            self.run(*args, **kwargs)
        if self._init:
            code = '\ninit()\n'
            self._universal_run(code, *args, **kwargs)
            return self.outputs

    def step(self, *args, **kwargs):
        """
        execute only one step of the model
        """
        if not self.has_run:
            self.run(*args, **kwargs)
        code = '\nstep()\n'
        self._universal_run(code, *args, **kwargs)

        return self.outputs

    def stop(self, *args, **kwargs):
        """
        stop execution
        """
        pass

    def animate(self, *args, **kwargs):
        """
        run model step by step
        """
        if self._animate:
            if not self.has_run:
                self.run(*args, **kwargs)

            code = '\nanimate()\n'
            self._universal_run(code, *args, **kwargs)

            return self.outputs

    def set_code(self, code):
        """
        Set the content and parse it to get docstring, inputs and outputs info, some methods
        """
        self._initial_code = code
        # TODO define the 3 functions parse_docstring_r, parse_functions_r, get_docstring_r
        model, self.inputs_info, self.outputs_info, self.cmdline = parse_docstring_r(code)
        self._init, self._step, self._animate, self._run = parse_functions_r(code)
        self._doc = get_docstring_r(code)
        self.has_run = False
