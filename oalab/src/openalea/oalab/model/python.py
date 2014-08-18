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


DEFAULT_DOC = """
<H1><IMG SRC=%s
 ALT="icon"
 HEIGHT=25
 WIDTH=25
 TITLE="Python logo">Python</H1>

more informations: http://www.python.org/
"""

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

    def get_documentation(self):
        """
        :return: a string with the documentation of the model
        """
        if self._doc:
            return self._doc
        else:
            return DEFAULT_DOC % str(self.icon)

    def repr_code(self):
        """
        :return: a string representation of model to save it on disk
        """
        return self.code

    def _run_code(self, code, *args, **kwargs):
        if code:
            # Set inputs
            self.inputs = args, kwargs
            # Prepare namespace
            self._prepare_namespace()
            # Run inside namespace
            user_ns = self.execute_in_namespace(code, namespace=self.ns)
            self.ns.update(user_ns)
            # Set outputs after execution
            self._set_output_from_ns(self.ns)
            return self.outputs

    def run(self, *args, **kwargs):
        """
        execute entire model

        :return: outputs of the model
        """
        return self._run_code(self.code, *args, **kwargs)

    def init(self, *args, **kwargs):
        """
        go back to initial step
        """
        return self._run_code(self._init, *args, **kwargs)

    def step(self, *args, **kwargs):
        """
        execute only one step of the model
        """
        return self._run_code(self._step, *args, **kwargs)

    def animate(self, *args, **kwargs):
        """
        run model step by step
        """
        return self._run_code(self._animate, *args, **kwargs)

    def stop(self, *args, **kwargs):
        """
        stop execution
        """
        # TODO : to implement
        pass

    def _get_content(self):
        return self._content

    def _set_content(self, content=""):
        """
        Set the content and parse it to get docstring, inputs and outputs info, some methods
        """
        self._content = content
        model, self.inputs_info, self.outputs_info = parse_docstring(content)
        self._init, self._step, self._animate, self._run = parse_functions(content)
        self._doc = get_docstring(content)

    content = property(fget=_get_content, fset=_set_content)
    code = property(fget=_get_content, fset=_set_content)

