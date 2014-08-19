
from openalea.vpltk.datamodel.model import Model
from openalea.oalab.model.parse import parse_docstring, get_docstring, parse_functions, prepare_inputs

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
    mimetype = "text/x-python"

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def get_documentation(self):
        """
        :return: a string with the documentation of the model
        """
        self.read()
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
            self.inputs = prepare_inputs(self.inputs_info, *args, **kwargs)
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

    def parse(self):
        content = self.content
        model, self.inputs_info, self.outputs_info = parse_docstring(content)
        self._init, self._step, self._animate, self._run = parse_functions(content)
        self._doc = get_docstring(content)

