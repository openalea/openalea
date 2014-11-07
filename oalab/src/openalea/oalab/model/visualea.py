# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#                       Guillaume Baty <guillaume.baty@inria.fr>
#                       Christophe Pradal <christophe.pradal@inria.fr>
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

from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.data import Data
from openalea.core.model import Model
from openalea.core.node import Node, AbstractFactory
from openalea.core.package import Package
from openalea.core.pkgmanager import PackageManager
from openalea.oalab.model.parse import InputObj, OutputObj

import copy
import string


class VisualeaFile(Data):
    default_name = "Workflow"
    default_file_name = "workflow.wpy"
    pattern = "*.wpy"
    extension = "wpy"
    icon = ":/images/resources/openalealogo.png"
    dtype = default_name
    mimetype = "text/x-visualea"


class VisualeaModel(Model):
    default_name = "Workflow"
    default_file_name = "workflow.wpy"
    pattern = "*.wpy"
    extension = "wpy"
    icon = ":/images/resources/openalealogo.png"
    dtype = default_name
    mimetype = "text/x-visualea"

    def __init__(self, **kwargs):
        name = kwargs.get('name', 'Workflow')
        kwargs['name'] = name
        self._workflow = CompositeNodeFactory(name).instantiate()
        super(VisualeaModel, self).__init__(**kwargs)

    def get_documentation(self):
        """

        :return: docstring of current workflow
        """
        if hasattr(self._workflow, "get_tip"):
            self._doc = self._workflow.get_tip()
        return self._doc

    def repr_code(self):
        """
        :return: a string representation of model to save it on disk
        """
        name = self.name

        if name[-3:] in '.py':
            name = name[-3:]
        elif name[-4:] in '.wpy':
            name = name[-4:]
        cn = self._workflow
        cnf = CompositeNodeFactory(name)
        cn.to_factory(cnf)

        repr_wf = repr(cnf.get_writer())
        # hack to allow eval rather than exec...
        # TODO: change the writer

        repr_wf = (' = ').join(repr_wf.split(' = ')[1:])
        return repr_wf

    def eval_value(self, value):
        return value

    def _outputs(self):
        outputs = []
        for i, outobj in enumerate(self.outputs_info):
            out = self._workflow.get_output(i)
            outputs.append(out)
            self._ns[outobj.name] = out
        if len(outputs) == 0:
            return None
        elif len(outputs) == 1:
            return outputs[0]
        else:
            return outputs

    def _set_inputs(self, *args, **kwargs):
        self._ns = self.inputs_from_ns(self.inputs_info, self._ns, *args, **kwargs)
        for i, inp in enumerate(self.inputs_info):
            self._workflow.set_input(i, self._ns[inp.name])

    def run(self, *args, **kwargs):
        """
        execute entire model
        """
        self.init(*args, **kwargs)
        self._workflow.eval()
        outputs = self._outputs()
        return outputs

    def namespace(self):
        from openalea.core.service.run import namespace
        return namespace()

    def init(self, *args, **kwargs):
        """
        go back to initial step
        """
        user_ns = kwargs.pop('namespace', {})
        self._ns = user_ns
        self._ns.update(self.namespace())
        self._set_inputs(*args, **kwargs)
        return self._outputs()

    def step(self, *args, **kwargs):
        """
        execute only one step of the model
        """
        raise NotImplementedError
        self._set_inputs()
        self._workflow.eval_as_expression()
        return self._outputs()

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
        return self._workflow.eval()

    def execute(self, code=None):
        """
        In other paradigms: Execute code (str).
        Here this method does not have signification (only for "script-like" paradigm), so, it make a **run**.
        """
        return self.run()

    def set_code(self, code):
        self._initial_code = code
        if not code:
            self._workflow = CompositeNodeFactory(self.name).instantiate()
        elif isinstance(code, CompositeNodeFactory):
            # hakishhh
            # CompositeNodeFactory.instantiate_node = monkey_patch_instantiate_node
            self._workflow = code.instantiate()
        else:
            # Access to the current project
            cnf = eval(code, globals(), locals())
            # hakishhh
            CompositeNodeFactory.instantiate_node = monkey_patch_instantiate_node
#             raise IOError(cnf)
            self._workflow = cnf.instantiate()

    @property
    def inputs_info(self):
        inputs = []
        for inp in self._workflow.input_desc:
            inpobj = InputObj()
            inpobj.name = inp.get('name', None)
            inpobj.interface = inp.get('interface', None)
            inpobj.default = inp.get('value', None)
            inputs.append(inpobj)
        return inputs

    @inputs_info.setter
    def inputs_info(self, inputs):
        self._workflow.clear_inputs()
        for inp in inputs:
            self._workflow.add_input(name=inp.name, value=inp.default, interface=inp.interface)

    @property
    def outputs_info(self):
        outputs = []
        for out in self._workflow.output_desc:
            outobj = OutputObj()
            outobj.name = out.get('name', None)
            outobj.interface = out.get('interface', None)
            outobj.default = out.get('value', None)
            outputs.append(outobj)
        return outputs

    @outputs_info.setter
    def outputs_info(self, outputs):
        self._workflow.clear_outputs()
        for out in outputs:
            self._workflow.add_output(name=out.name, value=out.default, interface=out.interface)


class ModelNode(Node):

    def __init__(self, model, inputs=(), outputs=()):
        super(ModelNode, self).__init__(inputs=inputs, outputs=outputs)
        self.set_model(model)

    def set_model(self, model):
        self.model = model
        self.__doc__ = self.model.get_documentation()

    def __call__(self, inputs=()):
        """ Call function. Must be overriden """
        from openalea.core.service.run import namespace
        return self.model(*inputs, namespace=namespace())


class ModelNodeFactory(AbstractFactory):

    def __init__(self,
                 name,
                 lazy=True,
                 delay=0,
                 alias=None,
                 **kargs):
        super(ModelNodeFactory, self).__init__(name, **kargs)
        self.delay = delay
        self.alias = alias
        self._model = None

    def get_id(self):
        return str(self.name)

    @property
    def package(self):
        class fake_package(Package):

            def get_id(self):
                return ":projectmanager.current"

            def reload(self):
                pass
                # print 2, "package reload"
        return fake_package(self.name, {'authors': ''})

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
        from openalea.core.service.run import get_model
        model = get_model(self.name)

        if model is None:
            print "error loading model ", self.name
            # print "Available models are ", pm.cproject.model.keys()

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
            # model.read()
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
            from openalea.core.project.manager import ProjectManager
            pm = ProjectManager()
            print "We can't instantiate node from project %s because we don't have model %s" % (pm.cproject.name, self.name)
            print "We only have models : "
            print ", ".join(pm.cproject.model.keys())

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


def monkey_patch_instantiate_node(self, vid, call_stack=None):
    (package_id, factory_id) = self.elt_factory[vid]
    # my temporary patch
    if package_id in (None, ":projectmanager.current"):
        factory = ModelNodeFactory(factory_id)
    else:
        pkgmanager = PackageManager()
        pkg = pkgmanager[package_id]
        factory = pkg.get_factory(factory_id)

    node = factory.instantiate(call_stack)
    if node is None:
        node = self.create_fake_node(vid)
        return node

    attributes = copy.deepcopy(self.elt_data[vid])
    ad_hoc = copy.deepcopy(self.elt_ad_hoc.get(vid, None))
    self.load_ad_hoc_data(node, attributes, ad_hoc)

    # copy node input data if any
    values = copy.deepcopy(self.elt_value.get(vid, ()))

    for vs in values:
        try:
            # the two first elements are the historical
            # values : port Id and port value
            # the values beyond are not used.
            port, v = vs[:2]
            node.set_input(port, eval(v))
            node.input_desc[port].get_ad_hoc_dict().set_metadata("hide",
                                                                 node.is_port_hidden(port))
        except:
            continue

    return node


CompositeNodeFactory.instantiate_node = monkey_patch_instantiate_node
