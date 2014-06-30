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

    def __init__(self, name="script.py", code="", filepath="", inputs=[], outputs=[]):
        self._step = False
        self._animate = False
        self._init = False
        self._run = False
        super(PythonModel, self).__init__(name=name, code=code, filepath=filepath, inputs=inputs, outputs=outputs)
        self.code = code # use it to force to parse doc, functions, inputs and outputs
        self.ns = dict()
        self._interpreter = None

    def get_documentation(self):
        """
        :return: a string with the documentation of the model
        """
        if self._doc:
            return self._doc
        else:
            return """
<H1><IMG SRC=%s
 ALT="icon"
 HEIGHT=25
 WIDTH=25
 TITLE="Python logo">Python</H1>

more informations: http://www.python.org/
""" % str(self.icon)

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
            self.execute(code, *args, **kwargs)
#             return interpreter.run_cell(code)

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
        self.inputs = args

        interpreter = self._set_interpreter(**kwargs)

        # if interpreter:
        user_ns = interpreter.user_ns

        user_ns.update(self.ns)

        # put inputs inside namespace
        if self.inputs:
            user_ns.update(self.inputs)

        # run
#         interpreter.shell.run_cell(self.code)
        self.execute(self.code, user_ns, *args, **kwargs)

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
            self.inputs = args

            interpreter = self._set_interpreter(**kwargs)

            if interpreter:
                user_ns = interpreter.user_ns

                user_ns.update(self.ns)

                # put inputs inside namespace
                if self.inputs:
                    user_ns.update(self.inputs)

                code = self.code + """

init()
"""
                self.execute(code, user_ns, *args, **kwargs)

                self.set_output_from_ns(user_ns)

                return self.outputs

    def step(self, *args, **kwargs):
        """
        execute only one step of the model
        """
        if self._step:
            self.inputs = args

            interpreter = self._set_interpreter(**kwargs)
            user_ns = interpreter.user_ns

            user_ns.update(self.ns)

            # put inputs inside namespace
            if self.inputs:
                user_ns.update(self.inputs)

            code = self.code + """

step()
"""
            # run
            self.execute(code, user_ns, *args, **kwargs)
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
            self.inputs = args

            interpreter = self._set_interpreter(**kwargs)

            user_ns = interpreter.user_ns

            user_ns.update(self.ns)

            # put inputs inside namespace
            if self.inputs:
                user_ns.update(self.inputs)

            code = self.code + """

animate()
"""
            # run
            self.execute(code, user_ns, *args, **kwargs)

            self.set_output_from_ns(user_ns)

            return self.outputs

    def _set_interpreter(self, **kwargs):
        if not "interpreter" in kwargs:
            if not hasattr(self, "_interpreter"):
                try:
                    from IPython.core.getipython import get_ipython
                    self._interpreter = get_ipython()
                except NameError:
                    self._interpreter = None
                    raise("No interpreter is available to run model %s" % str(self))
            elif self._interpreter is None:
                try:
                    from IPython.core.getipython import get_ipython
                    self._interpreter = get_ipython()
                except NameError:
                    self._interpreter = None
                    raise("No interpreter is available to run model %s" % str(self))
        else:
            self._interpreter = kwargs["interpreter"]
        return self._interpreter

    def set_output_from_ns(self, namespace):
        # get outputs from namespace
        if self.outputs_info:
            self.outputs = []
            if len(self.outputs_info) > 0:
                for outp in self.outputs_info:
                    if outp.name in namespace:
                        self.outputs.append(namespace[outp.name])

    def execute(self, code, ns=None, *args, **kwargs):
        from openalea.oalab.session.session import Session
        session = Session()
        if session.debug:
            if ns is None:
                ns = {}
            exec code in ns, ns
        else:
            interpreter = kwargs["interpreter"]
            interpreter.run_cell(code)

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code=""):
        self._code = code
        model, self.inputs_info, self.outputs_info = parse_docstring(code)
        self._init, self._step, self._animate, self._run = parse_functions(code)
        self._doc = get_docstring(self._code)

