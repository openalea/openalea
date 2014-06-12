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
from openalea.oalab.model.parse import parse_docstring_r, get_docstring_r, parse_functions_r


class RModel(Model):
    default_name = "R"
    default_file_name = "script.r"
    pattern = "*.r"
    extension = "r"
    icon = ":/images/resources/RLogo.png"

    def __init__(self, name="script.r", code="", filepath="", inputs=[], outputs=[]):
        super(RModel, self).__init__(name=name, code=code, filepath=filepath, inputs=inputs, outputs=outputs)
        self._step = None
        self._animate = None
        self._init = None
        self.ns = dict()
        self.code = code  # use it to force to parse doc, functions, inputs and outputs
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
 TITLE="R logo">R language</H1>

more informations: http://www.r-project.org/
"""%str(self.icon)

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

    def run(self, *args, **kwargs):
        """
        execute model thanks to interpreter
        """
        # TODO: check if we can do by an other way for inputs, outputs (ex %%R -i inputs, -o outputs)
        if args:
            self.inputs = args

        interpreter = self._set_interpreter(**kwargs)

        user_ns = interpreter.user_ns
        user_ns.update(self.ns)

        # put inputs inside namespace
        if self.inputs:
            user_ns.update(self.inputs)

        # run
        code = """%load_ext rmagic
%%R

""" + self.code
        interpreter.run_cell(code)

        self.set_output_from_ns(user_ns)

        return self.outputs

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
                # TODO: check if *init* function can be call like that *init()*. Else, change it.
                code = """%load_ext rmagic
%%R

""" + self.code + """

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
            self.inputs = args

            interpreter = self._set_interpreter(**kwargs)
            user_ns = interpreter.user_ns

            user_ns.update(self.ns)

            # put inputs inside namespace
            if self.inputs:
                user_ns.update(self.inputs)
            # TODO: check if *step* function can be call like that *step()*. Else, change it.
            code = """%load_ext rmagic
%%R

""" + self.code + """

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
            # TODO: check if *animate* function can be call like that *animate()*. Else, change it.
            code = """%load_ext rmagic
%%R

""" + self.code + """

animate()
"""
            # run
            interpreter.run_cell(code)

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

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code=""):
        self._code = code
        # TODO define the 3 functions parse_docstring_r, parse_functions_r, get_docstring_r
        # model, self.inputs_info, self.outputs_info = parse_docstring_r(code)
        # self._init, self._step, self._animate, self._run = parse_functions_r(code)
        # self._doc = get_docstring_r(self._code)