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

    def run(self, *args, **kwargs):
        """
        execute model thanks to interpreter
        """
        if args:
            self.inputs = args

        interpreter = self._set_interpreter(**kwargs)

        user_ns = interpreter.user_ns

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

    def reset(self, *args, **kwargs):
        """
        go back to initial step
        """
        pass

    def step(self, *args, **kwargs):
        """
        execute only one step of the model
        """
        pass

    def stop(self, *args, **kwargs):
        """
        stop execution
        """
        pass

    def animate(self, *args, **kwargs):
        """
        run model step by step
        """
        pass

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
                        self.outputs.append(namespace[outp.name])