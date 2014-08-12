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
import collections
import string
from copy import copy
from openalea.core.node import Node, AbstractFactory
from openalea.vpltk.project.project import remove_extension
from openalea.core.path import path as Path


class Data(object):
    def __init__(self, name, path, dtype, **kwargs):
        """
        Classical use : *path* exists. Nothing is loaded in memory.
        Use :meth:`~Data.read` to get content
        """
        # TODO: document args
        self.name = name
        self.path = Path(path)
        self.dtype = dtype
        self._content = kwargs['content'] if 'content' in kwargs else None

    # def write(self, content):
    #     raise NotImplementedError

    def save(self):
        if self._content is not None:
            with open(self.path, 'wb') as f:
                f.write(self._content)
            self._content = None

    def read(self):
        if self.exists():
            with open(self.path, 'rb') as f:
                return f.read()
        else:
            return self._content

    def exists(self):
        return self.path.exists()

    @property
    def filename(self):
        return self.path.name

    @property
    def doc(self):
        pass

# class Model(Data):
#
#     @property
#     def code(self):
#         return self.read()


class Model(Data):
    default_dtype = "model"
    default_name = ""
    default_file_name = ""
    pattern = ""
    extension = ""
    icon = ""
    
    def __init__(self, name="", code="", filepath="", inputs=[], outputs=[]):
        """
        :param name: name of the model (name of the file?)
        :param code: code of the model, can be a string or an other object
        :param filepath: path to save the model on disk
        :param inputs: list of identifier of inputs that come from outside model (from world for example)
        :param outputs: list of objects to return outside model (to world for example)
        """
        name = remove_extension(name)
        self.name = name
        self.filepath = filepath
        self.inputs_info = inputs
        self.outputs_info = outputs
        self._inputs = []
        self._outputs = []
        self._code = ""
        self.code = code
        self._doc = ""

    def get_documentation(self):
        """
        :return: a string with the documentation of the model
        """
        return self._doc

    def repr_code(self):
        """
        :return: a string representation of model to save it on disk
        """
        raise NotImplementedError

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

    def input_defaults(self):
        return dict((x.name, eval(x.default)) for x in self.inputs_info if x.default)
        
    @property
    def inputs(self):
        """
        List of inputs of the model.

        :use:
            >>> model.inputs = 4, 3
            >>> rvalue = model.run()
        """
        return self._inputs

    @inputs.setter
    def inputs(self, *args):
        # TODO: refactor with types.FunctionType
        self._inputs = dict()
        if self.inputs_info:
            args, kwargs = args[0]
            not_set_inputs_info = copy(self.inputs_info) # Use it to know what we have to set and what is yet set

            # Set positional arguments
            if args:
                inputs = list(args)
                if len(inputs) == 1:
                    if isinstance(inputs, collections.Iterable):
                        inputs = inputs[0]
                    elif isinstance(inputs, collections.Iterable):
                        inputs = list(inputs)
                    inputs = [inputs]
                inputs.reverse()

                if self.inputs_info:
                    for input_info in self.inputs_info:
                        if len(inputs):
                            default_value = inputs.pop()
                            if input_info.name:
                                self._inputs[input_info.name] = default_value
                            not_set_inputs_info.remove(input_info)
                        else:
                            break

            # Set non-positional arguments
            if kwargs:
                if len(not_set_inputs_info):
                    not_set_inputs_info_dict = dict((inp.name, inp) for inp in not_set_inputs_info)
                    for name in kwargs:
                        value = kwargs[name]
                        if name in not_set_inputs_info_dict.keys():
                            self._inputs[name] = value
                            not_set_inputs_info.remove(not_set_inputs_info_dict[name])
                            del not_set_inputs_info_dict[name]
                        else:
                            print "We can not put ", name, "inside inputs of model", self.name, "because such an input is not declared in the model."

            # Fill others with defaults
            if len(not_set_inputs_info):
                for input_info in copy(not_set_inputs_info):
                    if input_info.default:
                        default_value = eval(input_info.default)
                        self._inputs[input_info.name] = default_value
                        not_set_inputs_info.remove(input_info)

            # If one argument is missing, raise
            if len(not_set_inputs_info):
                raise Exception("Model %s have inputs not set. Please set %s." % (self.name, [inp.name for inp in not_set_inputs_info]))

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

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code=""):
        self._code = code

    def abspath(self, parentdir):
        """ Returns absolute path of a model.

        parentdir is the path of the parent directory like projectdir/model

        """
        pd = Path(parentdir)
        filename = self.name+'.'+self.extension
        return (pd/filename).abspath()

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


class ModelNode(Node):
    def __init__(self, model, inputs=(), outputs=()):
        super(ModelNode, self).__init__(inputs=inputs, outputs=outputs)
        self.set_model(model)

    def set_model(self, model):
        self.model = model
        self.__doc__ = self.model.get_documentation()

    def __call__(self, inputs=()):
        """ Call function. Must be overriden """
        return self.model(*inputs)

    # def reload(self):
    #     node = self.factory.instanciate()


        # # set model
        # from openalea.vpltk.project.manager import ProjectManager
        # pm = ProjectManager()
        # model = pm.cproject.get_model(self.model.name)
        # if model:
        #     self.set_model(model)

        # reset inputs and outputs
        # super(ModelNode, self).reload()


class ModelFactory(AbstractFactory):
    def __init__(self,
                 name,
                 lazy = True,
                 delay = 0,
                 alias=None,
                 **kargs):
        super(ModelFactory, self).__init__(name, **kargs)
        self.delay = delay
        self.alias = alias
        self._model = None

    def get_id(self):
        return str(self.name)

    @property
    def package(self):
        class fake_package(object):
            def get_id(self):
                return ":projectmanager.current"
            def reload(self):
                pass
                # print 2, "package reload"
        return fake_package()

    def get_classobj(self):
        module = self.get_node_module()
        classobj = module.__dict__.get(self.nodeclass_name, None)
        return classobj

    def get_documentation(self):
        if self._model is None:
            self.instantiate()

        return self._model.get_documentation()

    def instantiate(self, call_stack=[]):
        """
        Returns a node instance.
        :param call_stack: the list of NodeFactory id already in call stack
        (in order to avoir infinite recursion)
        """
        from openalea.vpltk.project.manager import ProjectManager

        pm = ProjectManager()
        model = pm.cproject.get_model(self.name)
        if model is None:
            print "error loading model ", self.name
            print "Available models are ", pm.cproject.list_models()

        # TODO
        def signature(args_info, out=False):
            args = []
            if args_info:
                for arg in args_info:
                    d = {}
                    d['name'] = arg.name
                    if arg.interface:
                        d['interface'] = arg.interface
                    if not out and arg.default is not None:
                        d['value'] = arg.default
                    if d:
                        args.append(d)
            return args

        # If class is not a Node, embed object in a Node class
        if model:

            self.inputs = signature(model.inputs_info)
            self.outputs = signature(model.outputs_info, out=True)
            if not self.outputs:
                self.outputs = (dict(name="out", interface=None), )

            node = ModelNode(model, self.inputs, self.outputs)

            # Properties
            try:
                node.factory = self
                node.lazy = self.lazy
                if(not node.caption):
                    node.set_caption(self.name)

                node.delay = self.delay
            except:
                pass

            return node

        else:
            print "We can't instanciate node from project %s because we don't have model %s" %(pm.cproject.name,self.name)
            print "We only have models : "
            print pm.cproject.list_models()

    def instantiate_widget(self, node=None, parent=None, edit=False,
        autonomous=False):
        """ Return the corresponding widget initialised with node"""
        pass
        # TODO: open corresponding model

    def get_writer(self):
        """ Return the writer class """
        return PyModelNodeFactoryWriter(self)


class PyModelNodeFactoryWriter(object):
    """ NodeFactory python Writer """

    nodefactory_template = """

$NAME = ModelFactory(name=$PNAME,
                inputs=$LISTIN,
                outputs=$LISTOUT,
               )

"""

    def __init__(self, factory):
        self.factory = factory

    def __repr__(self):
        """ Return the python string representation """
        f = self.factory
        fstr = string.Template(self.nodefactory_template)

        result = fstr.safe_substitute(NAME=repr(f.name),
                                      LISTIN=repr(f.inputs),
                                      LISTOUT=repr(f.outputs),)
        return result


