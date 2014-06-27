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
        self.has_run = False

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

    def r_options(self, namespace):
        cmd = self.cmdline
        print self.inputs_info
        l = self.inputs_info
        input_names = [input.split(',')[0].split('=')[0] for input in l]
        input_names= [name for name in input_names if name in namespace]
        #input_values = [input.split('=')[1] for input in l]

        if input_names:
            cmd+= ' -i %s'%(','.join(input_names))

        l = self.outputs_info
        output_names = [input.split(',')[0].split('=')[0] for input in l]
        if output_names:
            cmd+= ' -o %s'%(','.join(output_names))

        print cmd

        return cmd

    def _universal_run(self,code, *args, **kwargs):
        """ This method is used by others...
        """
        if args:
            self.inputs = args

        interpreter = self._set_interpreter(**kwargs)

        user_ns = interpreter.user_ns
        user_ns.update(self.ns)

        # put inputs inside namespace
        if self.inputs:
            user_ns.update(self.inputs)

        cmdline = self.r_options(user_ns)
        shell = interpreter.shell
        if not self.has_run:
            shell.run_line_magic('load_ext','rmagic')
        shell.run_cell_magic('R', cmdline, code)
       
        self.set_output_from_ns(user_ns)


    def run_code(self, code, *args, **kwargs):
        """
        execute subpart of a model (only code *code*)
        """
        interpreter = self._set_interpreter(**kwargs)
        shell = interpreter.shell
        cmdline = self.r_options()
        if not self.has_run:
            shell.run_line_magic('load_ext','rmagic')
        shell.run_cell_magic('R', cmdline, code)

    def run(self, *args, **kwargs):
        """
        execute model thanks to interpreter
        """
        # TODO: check if we can do by an other way for inputs, outputs (ex %%R -i inputs, -o outputs)

        self._universal_run(self.code,*args,**kwargs)
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
            self._universal_run(code,*args,**kwargs)
            return self.outputs

    def step(self, *args, **kwargs):
        """
        execute only one step of the model
        """
        if not self.has_run:
            self.run(*args, **kwargs)
        code = '\nstep()\n'
        self._universal_run(code,*args,**kwargs)

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
            self._universal_run(code,*args,**kwargs)

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
        model, self.inputs_info, self.outputs_info, self.cmdline = parse_docstring_r(code)
        self._init, self._step, self._animate, self._run = parse_functions_r(code)
        self._doc = get_docstring_r(self._code)
        self.has_run = False
