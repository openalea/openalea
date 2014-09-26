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

from copy import copy
from openalea.core.data import Data
import string
from openalea.core.node import Node, AbstractFactory


class Model(Data):
    default_name = ""
    default_file_name = "filename.ext"
    pattern = "*.ext"
    extension = "ext"
    icon = ":/images/resources/logo.png"
    mimetype = "text/"

    CACHE = 0
    NO_CACHE = 1

    def __init__(self, **kwargs):
        if 'code' in kwargs and 'content' in kwargs:
            raise ValueError('Use content keyword only')
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
        self._doc = ''
        self.ns = dict()

        self._cache_mode = self.CACHE
        self._metadata = {'mtime':0, 'size':0}

        # If path doesn't exists, that means all content is in memory (passed in constructor for example)
        # So we need to parse it
        if not self.exists():
            self.parse()


    #################
    # REVIEW REQUIRED
    #################


    def get_documentation(self):
        self.read()
        return self._doc

    def repr_code(self):
        return self.read()


    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __str__(self):
        return str(self.filename)

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
        from openalea.core.service.ipython import get_interpreter
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
        from openalea.core.service.ipython import get_interpreter
        from openalea.core.control.manager import control_dict
        from openalea.core.project import ProjectManager
        interpreter = get_interpreter()

        # Add project namespace inside namespace
        pm = ProjectManager()
        if pm.cproject:
            self.ns.update(pm.cproject.ns)

        # Add controls inside namespace
        controls = control_dict()
        if controls:
            self.ns.update(controls)

        if interpreter:
            self.ns.update(interpreter.user_ns)

        # Add inputs inside namespace
        if self.inputs:
            self.ns.update(self.inputs)
        return self.ns

    def execute_in_namespace(self, code, namespace={}):
        """
        Execute code in an isolate namespace

        :param code: text code to execute
        :param namespace: dict namespace where code will be executed

        :return: namespace in which execution was done
        """
        from openalea.core.service.ipython import get_interpreter
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

    def clear_cache(self):
        self._mtime = 0

    def set_cache_mode(self, cache_mode=None):
        if cache_mode is None:
            self._cache_mode = self.CACHE
        else:
            self._cache_mode = cache_mode

    def _has_changed(self):
        if self._cache_mode == self.NO_CACHE:
            return True
        if self.path.getmtime() > self._metadata['mtime']:
            return True
        if self._metadata['size'] != self.path.size:
            return True
        return False

    def read(self):
        # If path exists and content has changed since last read,
        # update Model.content and parse it
        if self.exists():
            if self._has_changed():
                with open(self.path, 'rb') as f:
                    self._content = f.read()
                    self._metadata['mtime'] = self.path.getmtime()
                    self._metadata['size'] = self.path.size
                    self.parse()
        return self._content

    def _set_content(self, content):
        self._content = content
        self.parse()

    def parse(self):
        pass

    content = property(fset=_set_content)
    code = property(fget=read)


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
        # from openalea.core.project.manager import ProjectManager
        # pm = ProjectManager()
        # model = pm.cproject.get_model(self.model.name)
        # if model:
        #     self.set_model(model)

        # reset inputs and outputs
        # super(ModelNode, self).reload()


class ModelFactory(AbstractFactory):
    def __init__(self,
                 name,
                 lazy=True,
                 delay=0,
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
        from openalea.core.project.manager import ProjectManager

        pm = ProjectManager()
        model = pm.cproject.get_model(self.name)
        if model is None:
            print "error loading model ", self.name
            print "Available models are ", pm.cproject.model.keys()

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
            model.read()
            self.inputs = signature(model.inputs_info)
            self.outputs = signature(model.outputs_info, out=True)
            if not self.outputs:
                self.outputs = (dict(name="out", interface=None),)

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
            print "We can't instanciate node from project %s because we don't have model %s" % (pm.cproject.name, self.name)
            print "We only have models : "
            print pm.cproject.model.keys()

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
            from openalea.oalab.model.parse import prepare_inputs
            self.inputs = prepare_inputs(self.inputs_info, name=self.filename, *args, **kwargs)
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
        from openalea.oalab.model.parse import parse_docstring, get_docstring, parse_functions
        content = self._content
        model, self.inputs_info, self.outputs_info = parse_docstring(content)
        self._init, self._step, self._animate, self._run = parse_functions(content)
        self._doc = get_docstring(content)

