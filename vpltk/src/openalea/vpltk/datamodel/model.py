
from copy import copy
from openalea.vpltk.datamodel.data import Data

class Model(Data):
    def __init__(self, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = 'model'
        # Backward compatibility with model
        if 'code' in kwargs and 'content' not in kwargs:
            kwargs['content'] = kwargs.pop('code')
        if 'name' in kwargs and 'filename' not in kwargs and 'path' not in kwargs:
            kwargs['filename'] = kwargs.pop('name')
        if 'filepath' in kwargs and 'path' not in kwargs:
            kwargs['path'] = kwargs.pop('filepath')

        Data.__init__(self, **kwargs)

        self._step = False
        self._animate = False
        self._init = False
        self._run = False

        self.inputs_info = kwargs['inputs'] if 'inputs' in kwargs else []
        self.outputs_info = kwargs['outputs'] if 'outputs' in kwargs else []

        self.inputs = {}
        self.outputs = []
        self.doc = ''
        self.ns = dict()


    #################
    # REVIEW REQUIRED
    #################


    def get_documentation(self):
        return self.doc

    def repr_code(self):
        return self.read()


    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __str__(self):
        return "Instance of model " + str(type(self)) + " named " + str(self.name)

    def run(self, *args, **kwargs):
        """
        execute model
        """
        raise NotImplementedError

    def init(self, *args, **kwargs):
        """
        go back to initial step
        """
        raise NotImplementedError

    def step(self, *args, **kwargs):
        """
        execute only one step of the model
        """
        raise NotImplementedError

    def stop(self, *args, **kwargs):
        """
        stop execution
        """
        raise NotImplementedError

    def animate(self, *args, **kwargs):
        """
        run model step by step
        """
        raise NotImplementedError

    def execute(self, code):
        """
        Execute code (str) in current interpreter
        """
        from openalea.oalab.service.ipython import get_interpreter
        interpreter = get_interpreter()
        return interpreter.runcode(code)

    def _set_output_from_ns(self, namespace):
        """
        Get outputs from namespace and set them inside self.outputs

        :param namespace: dict where the model will search the outputs
        """
        if self.outputs_info:
            self.outputs = []
            if len(self.outputs_info) > 0:
                for outp in self.outputs_info:
                    if outp.name in namespace:
                        self.outputs.append(namespace[outp.name])

    @property
    def outputs(self):
        """
        Return outputs of the model after running it.

        :use:
            >>> outputs = model.run()
            >>> outputs == model.outputs
            True
        """
        if self.outputs_info and self._outputs:
            if len(self.outputs_info) == 1 and len(self._outputs) == 1:
                return self._outputs[0]
        return self._outputs

    @outputs.setter
    def outputs(self, outputs=[]):
        self._outputs = outputs

    def _prepare_namespace(self):
        """
        :return: the current namespace updated with interpreter namespace and inputs
        """
        from openalea.oalab.service.ipython import get_interpreter
        interpreter = get_interpreter()

        if interpreter:
            self.ns.update(interpreter.user_ns)

        if self.inputs:
            self.ns.update(self.inputs) # Add inputs inside namespace
        return self.ns

    def execute_in_namespace(self, code, namespace={}):
        """
        Execute code in an isolate namespace

        :param code: text code to execute
        :param namespace: dict namespace where code will be executed

        :return: namespace in which execution was done
        """
        from openalea.oalab.service.ipython import get_interpreter
        interpreter = get_interpreter()
        # Save current namespace
        old_namespace = copy(interpreter.user_ns)
        # Clear current namespace
        interpreter.user_ns.clear()
        # Set namespace with new one
        interpreter.user_ns.update(namespace)
        # Execute code in new namespace
        self.execute(code)
        # Get just modified namespace
        namespace = copy(interpreter.user_ns)
        # Restore previous namespace
        interpreter.user_ns.clear()
        interpreter.user_ns.update(old_namespace)
        return namespace
