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
from openalea.core.node import Node, AbstractFactory


class Model(object):
    default_name = ""
    default_file_name = ""
    pattern = ""
    extension = ""
    icon = ""
    
    def __init__(self, name="", code="", filepath="", inputs=[], outputs=[]):
        """
        :param name: name of the model (name of the file?)
        :param code: code of the model, can be a string or an other object
        :param inputs: list of identifier of inputs that come from outside model (from world for example)
        :param outputs: list of objects to return outside model (to world for example)
        """
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
        pass

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        """
        execute model
        """
        pass

    def init(self, *args, **kwargs):
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

    @property
    def inputs(self):
        """
        List of inputs of the model.

        :use:
            >>> model.inputs = 4, 3
            >>> model.run()
        """
        return self._inputs

    @inputs.setter
    def inputs(self, *args):
        self._inputs = dict()
        if args:
            # inputs = args
            inputs = list(args)
            if len(inputs) == 1:
                if isinstance(inputs, collections.Iterable):
                    inputs = inputs[0]
                if isinstance(inputs, collections.Iterable):
                    inputs = list(inputs)
                else:
                    inputs = [inputs]
            inputs.reverse()

            if self.inputs_info:
                for input_info in self.inputs_info:
                    if len(inputs):
                        inp = inputs.pop()
                    elif input_info.default:
                        inp = eval(input_info.default)
                    else:
                        raise Exception("Model %s have inputs not setted. Please set %s ." %(self.name,input_info.name))

                    if input_info.name:
                        self._inputs[input_info.name] = inp

    @property
    def outputs(self):
        """
        Return outputs of the model after running it.

        :use:
            >>> model.run()
            >>> print model.outputs
        """
        # if len(self._outputs) == 1:
        #     return self._outputs[0]
        # else:
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


class ModelNode(Node):
    def __init__(self, model, inputs=(), outputs=()):
        super(ModelNode, self).__init__(inputs=inputs, outputs=outputs)
        self.model = model
        self.__doc__ = self.model.get_documentation()

    def __call__(self, inputs = ()):
        """ Call function. Must be overriden """
        return self.model(*inputs)


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
        model = pm.cproject.model(self.name)

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
            print [model.name for model in pm.cproject.models()]

    def instantiate_widget(self, node=None, parent=None, edit=False,
        autonomous=False):
        """ Return the corresponding widget initialised with node"""
        print "instanciate_widget"
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


