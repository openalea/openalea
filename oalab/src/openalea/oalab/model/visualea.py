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
from openalea.vpltk.datamodel.model import Model, ModelFactory
from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.pkgmanager import PackageManager
import copy


class VisualeaModel(Model):
    default_name = "Workflow"
    default_file_name = "workflow.wpy"
    pattern = "*.wpy"
    extension = "wpy"
    icon = ":/images/resources/openalealogo.png"
    mimetype = "text/x-visualea"

    def __init__(self, **kwargs):
        super(VisualeaModel, self).__init__(**kwargs)

    def load(self):
        self.content = self.read()
        code = self.content
        if (code is None) or (code is ""):
            self._workflow = CompositeNodeFactory(self.filename).instantiate()
        elif isinstance(code, CompositeNodeFactory):
            # hakishhh
            #CompositeNodeFactory.instantiate_node = monkey_patch_instantiate_node
            self._workflow = code.instantiate()
        else:
            # Access to the current project
            cnf = eval(code, globals(), locals())
            # hakishhh
            # CompositeNodeFactory.instantiate_node = monkey_patch_instantiate_node
#             raise IOError(cnf)
            self._workflow = cnf.instantiate()

    def read(self):
        if self.exists():
            with open(self.path, 'r') as f:
                return f.read()
        else:
            return self._content

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

    def run(self, *args, **kwargs):
        """
        execute entire model
        """
        return self._workflow.eval()

    def init(self, *args, **kwargs):
        """
        go back to initial step
        """
        return self._workflow.reset()

    def step(self, *args, **kwargs):
        """
        execute only one step of the model
        """
        return self._workflow.eval_as_expression(step=True)

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

    def _get_content(self):
        return self._content

    def _set_content(self, content=""):
        """
        Set the content and parse it to get docstring, inputs and outputs info, some methods
        """
        self._content = content

    content = property(fget=_get_content, fset=_set_content)
    code = property(fget=_get_content, fset=_set_content)

def monkey_patch_instantiate_node(self, vid, call_stack=None):
    (package_id, factory_id) = self.elt_factory[vid]
    print package_id, factory_id
    
    # my temporary patch
    if package_id in (None, ":projectmanager.current"):
        factory = ModelFactory(factory_id)
    else:
        pkgmanager = PackageManager()
        pkg = pkgmanager[package_id]
        factory = pkg.get_factory(factory_id)
    
    print factory
    node = factory.instantiate(call_stack)

    attributes = copy.deepcopy(self.elt_data[vid])
    ad_hoc = copy.deepcopy(self.elt_ad_hoc.get(vid, None))
    self.load_ad_hoc_data(node, attributes, ad_hoc)

    # copy node input data if any
    values = copy.deepcopy(self.elt_value.get(vid, ()))

    for vs in values:
        try:
            #the two first elements are the historical
            #values : port Id and port value
            #the values beyond are not used.
            port, v = vs[:2]
            node.set_input(port, eval(v))
            node.input_desc[port].get_ad_hoc_dict().set_metadata("hide",
                                                                 node.is_port_hidden(port))
        except:
            continue

    return node

CompositeNodeFactory.instantiate_node = monkey_patch_instantiate_node
