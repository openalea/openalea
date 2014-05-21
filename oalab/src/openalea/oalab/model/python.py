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
from openalea.oalab.model.model import Model
from openalea.oalab.model.parse import parse_docstring, get_docstring, parse_functions


class PythonModel(Model):
    default_name = "Python"
    default_file_name = "script.py"
    pattern = "*.py"
    extension = "py"
    icon = ":/images/resources/Python-logo.png"

    def __init__(self, name="script.py", code="", inputs=[], outputs=[]):
        self._step = False
        self._animate = False
        self._init = False
        self._run = False
        super(PythonModel, self).__init__(name=name, code=code, inputs=inputs, outputs=outputs)
        self.code = code  # use it to force to parse doc, functions, inputs and outputs

    def repr_code(self):
        """
        :return: a string representation of model to save it on disk
        """
        return self.code

    def run_code(self, code, *args, **kwargs):
        """
        execute subpart of a model (only code *code*)
        """
        interpreter = self._set_interpreter(**kwargs)

        if interpreter:
            # run
            return interpreter.run_cell(code)

        # else:
        #     # TODO do better
        #     cc = compile(code, 'temp', 'exec')
        #     result = dict()
        #     eval(cc, globals(), result)
        #     self.set_output_from_ns(result)
        #     return self.outputs

    def run(self, *args, **kwargs):
        """
        execute model thanks to interpreter
        """
        if args:
            self.inputs = args

        interpreter = self._set_interpreter(**kwargs)

        # if interpreter:
        user_ns = interpreter.user_ns

        # put inputs inside namespace
        if self.inputs:
            user_ns.update(self.inputs)

        # run
        interpreter.run_cell(self.code)

        self.set_output_from_ns(user_ns)

        return self.outputs

        # else:
        #     # TODO do better
        #     cc = compile(self.code, 'temp', 'exec')
        #     result = dict()
        #     eval(cc, globals(), result)
        #     self.set_output_from_ns(result)
        #     return self.outputs

    def init(self, *args, **kwargs):
        """
        go back to initial step
        """
        if self._init:
            if args:
                self.inputs = args

            interpreter = self._set_interpreter(**kwargs)

            if interpreter:
                user_ns = interpreter.user_ns

                # put inputs inside namespace
                if self.inputs:
                    user_ns.update(self.inputs)

                code = self.code + """

init()
"""
                interpreter.run_cell(code)

                self.set_output_from_ns(user_ns)

                return self.outputs

    def step(self, *args, **kwargs):
        """
        execute only one step of the model
        """
        if self._step:
            if args:
                self.inputs = args

            interpreter = self._set_interpreter(**kwargs)
            user_ns = interpreter.user_ns
            # put inputs inside namespace
            if self.inputs:
                user_ns.update(self.inputs)

            code = self.code + """

step()
"""
            # run
            interpreter.run_cell(code)
            self.set_output_from_ns(user_ns)

            return self.outputs

    def stop(self, *args, **kwargs):
        """
        stop execution
        """
        # TODO : to implement
        pass

    def animate(self, *args, **kwargs):
        """
        run model step by step
        """
        if self._animate:
            if args:
                self.inputs = args

            interpreter = self._set_interpreter(**kwargs)

            user_ns = interpreter.user_ns

            # put inputs inside namespace
            if self.inputs:
                user_ns.update(self.inputs)

            code = self.code + """

animate()
"""
            # run
            interpreter.run_cell(code)

            self.set_output_from_ns(user_ns)

            return self.outputs

    def _set_interpreter(self, **kwargs):
        if not "interpreter" in kwargs:
            try:
                from IPython.core.getipython import get_ipython
                interpreter = get_ipython()
            except NameError:
                interpreter = None
                #raise("No interpreter is available to run model %s" % str(self))
        else:
            interpreter = kwargs["interpreter"]
        return interpreter

    def set_output_from_ns(self, namespace):
        # get outputs from namespace
        if self.outputs_info:
            self.outputs = []
            if len(self.outputs_info) > 0:
                for outp in self.outputs_info:
                    if outp.name in namespace:
                        # print "outp.name: ", outp.name
                        # print "namespace[outp.name]: ", namespace[outp.name]
                        # print "self.outputs: ", self.outputs
                        self.outputs.append(namespace[outp.name])

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code=""):
        self._code = code
        model, self.inputs_info, self.outputs_info = parse_docstring(code)
        self._init, self._step, self._animate, self._run = parse_functions(code)
        self._doc = get_docstring(self._code)