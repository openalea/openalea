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
from openalea.oalab.model.parse import parse_string


class PythonModel(Model):
    default_name = "Python"
    default_file_name = "script.py"
    pattern = "*.py"
    extension = "py"
    icon = ":/images/resources/Python-logo.png"

    def __init__(self, name="script.py", code="", inputs=[], outputs=[]):
        super(PythonModel, self).__init__(name=name, code=code, inputs=inputs, outputs=outputs)
        self._step = None
        self._animate = None
        self._init = None
        model, inputs, outputs = parse_string(self.code)
        self.inputs_info = inputs
        self.outputs_info = outputs

    def repr_code(self):
        """
        :return: a string representation of model to save it on disk
        """
        return self.code

    def run(self, *args, **kwargs):
        """
        execute model thanks to interpreter
        """
        interpreter = self._set_interpreter(**kwargs)
        user_ns = interpreter.user_ns

        if args:
            self.inputs = args

        # put inputs inside namespace
        if self.inputs:
            user_ns.update(self.inputs)

        # run
        result = interpreter.run_cell(self.code)

        # get outputs from namespace
        if self.outputs_info:
            self.outputs = []
            if len(self.outputs_info) > 0:
                for outp in self.outputs_info:
                    if outp.name in user_ns:
                        self.outputs.append(user_ns[outp.name])

        ## Hack to store methods init, step and animate
        self._init = user_ns.get("init")
        if not callable(self._init):
            self._init = None

        self._step = user_ns.get("step")
        if not callable(self._step):
            self._step = None

        self._animate = user_ns.get("animate")
        if not callable(self._animate):
            self._animate = None
            if self._step:
                def animate():
                    for i in range(5):
                        self._step()
                self._animate = animate
        return result

    def reset(self, *args, **kwargs):
        """
        go back to initial step
        """
        # TODO : get function from the current widget
        if self._init:
            return self._init()

    def step(self, *args, **kwargs):
        """
        execute only one step of the model
        """
        # TODO : get function from the current widget
        if self._step:
            return self._step()

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
        # TODO : get function from the current widget
        if self._animate:
            return self._animate()

    def _set_interpreter(self, **kwargs):
        if not "interpreter" in kwargs:
            try:
                interpreter = get_ipython()
            except NameError:
                raise("No interpreter is available to run model %s" % str(self))
        else:
            interpreter = kwargs["interpreter"]
        return interpreter