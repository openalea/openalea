# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""Node and NodeFactory classes.

A Node is generalized functor which is embeded in a dataflow.
A Factory build Node from its description. Factories instantiate
Nodes on demand for the dataflow.
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import imp
import inspect
import os
import sys
import string
import types
from copy import copy, deepcopy
from weakref import ref, proxy

# from signature import get_parameters
import signature as sgn
from observer import Observed, AbstractListener
from actor import IActor
from metadatadict import MetaDataDict, HasAdHoc
from interface import TypeNameInterfaceMap
# Exceptions
class RecursionError (Exception):
    """todo"""
    pass


class InstantiationError(Exception):
    """todo"""
    pass


########################
# Node related classes #
########################
class AbstractNode(Observed, HasAdHoc):
    """
    An AbstractNode is the atomic entity in a dataflow.

    internal_data contains properties specified by users.
    They can be extended and the number is not fixed.
    We use a dict to distinguish these public properties to the others
    which are used for protected management.

    .. todo::
        - rename internal_data into attributes.
    """

    mimetype = "openalea/node"

    def __init__(self):
        """
        Default Constructor
        Create Internal Data dictionnary
        """
        HasAdHoc.__init__(self)
        Observed.__init__(self)

        self.__id = None
        # Internal Data (caption...)
        self.internal_data = {}
        self.factory = None

        # -- the ugly back reference --
        # !! Christophe, don't look at this one.
        # proxy to higher level structure, aka CompositeNode.
        # This is currently only used by the "wrap_method" node
        # that needs to modify the topology of the graph.
        self._composite_node = None

        # The default layout
        self.view = None
        self.user_application = None
        self.__inError = False

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id
        self.internal_data["id"] = self.__id

    def _init_internal_data(self, d):
        self.internal_data.update(d)

    # -- the ugly back reference --
    def set_compositenode(self, upper):
        self._composite_node = proxy(upper)

    def set_data(self, key, value, notify=True):
        """ Set internal node data """
        self.internal_data[key] = value
        if(notify):
            self.notify_listeners(("data_modified", key, value))

    def close(self):
        self.notify_listeners(("close", self))

    def reset(self):
        """ Reset Node """
        pass

    def reload(self):
        """ Reset Node """
        pass

    def invalidate(self):
        """ Invalidate Node """
        pass

    def set_factory(self, factory):
        """ Set the factory of the node (if any) """
        self.factory = factory

    def get_factory(self):
        """ Return the factory of the node (if any) """
        return self.factory

    def get_raise_exception(self):
        return self.__inError

    def set_raise_exception(self, val):
        self.__inError = val
        self.notify_listeners(("exception_state_changed", val))

    raise_exception = property(get_raise_exception, set_raise_exception)


class AbstractPort(dict, Observed, HasAdHoc):
    """
    The class describing the ports.
    AbstractPort is a dict for historical reason.
    """

    def __init__(self, vertex):
        dict.__init__(self)
        HasAdHoc.__init__(self)
        Observed.__init__(self)

        self.vertex = ref(vertex)
        self.__id = None

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    def copy_to(self, other):
        other.get_ad_hoc_dict().update(self.get_ad_hoc_dict())
        self.transfer_listeners(other)

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_desc(self):
        """ Gets default description """
        return self.get("desc", None)

    def get_default(self):
        """todo"""
        return self.get("value", None)

    def get_interface(self):
        """Gets the interface  """
        interf = self.get("interface", None)
        if isinstance(interf, str):
            return TypeNameInterfaceMap()[interf]
        else:
            return interf

    def get_tip(self, current_value=None):
        """ Return the tool tip """
        name = self['name']
        interface = self.get('interface', None)
        desc = self.get('desc', '')
        value = self.get('value', None)
        iname = 'Any'
        if(interface):
            try:
                iname = interface.__name__
            except AttributeError:
                try:
                    iname = interface.__class__.__name__
                except AttributeError:
                    iname = str(interface)

        # A way to avoid displaying too long strings.
        comment = str(value)
        if len(comment) > 100:
            comment = comment[:100] + ' ...'

        if current_value is None :
            return '%s(%s): %s [default=%s] ' % (name, iname, desc, comment)
        else :
            return '%s(%s): %s' % (name, iname, str(current_value))


class InputPort(AbstractPort):
    """ The class describing the input ports """

    def __init__(self, node):
        AbstractPort.__init__(self, node)

    def get_label(self):
        """Gets default label"""
        return self.get("label", self["name"])

    def is_hidden(self):
        """True if the port should not be displayed."""
        return self.get("hide", False)


class OutputPort(AbstractPort):
    """The class describing the output ports """
    def __init__(self, node):
        AbstractPort.__init__(self, node)


class Annotation(AbstractNode):
    def __init__(self):
        AbstractNode.__init__(self)

    def to_script (self):
        """Script translation of this node.
        """
        return ""

class Node(AbstractNode):
    """
    It is a callable object with typed inputs and outputs.
    Inputs and Outpus are indexed by their position or by a name (str)
    """

    @staticmethod
    def is_deprecated_event(event):
        evLen = len(event)
        conversionTxt = None
        retEvent = event
        if evLen == 2:
            if event[0] == "caption_modified":
                retEvent = "data_modified", "caption", event[1]
                conversionTxt = "('data_modified', 'caption', caption)"
        elif evLen == 3:
            if event[0] == "data_modified":
                if event[1] == "delay":
                    retEvent = "internal_state_changed", "delay", event[2]
                    conversionTxt = "('internal_state_changed', 'delay', delay)"
            elif event[0] == "internal_data_changed":
                retEvent = ('internal_state_changed', event[1], event[2])
                conversionTxt = "('internal_state_changed', 'key', value)"
        return conversionTxt, retEvent

    def __init__(self, inputs=(), outputs=()):
        """

        :param inputs: list of dict(name='X', interface=IFloat, value=0)
        :param outputs: list of dict(name='X', interface=IFloat)

        .. note::
            if IO names are not a string, they will be converted with str()
        """

        AbstractNode.__init__(self)
        self.clear_inputs()
        self.clear_outputs()
        self.set_io(inputs, outputs)

        # Node State
        self.modified = True

        # Internal Data
        self.internal_data["caption"] = '' # str(self.__class__.__name__)
        self.internal_data["lazy"] = True
        self.internal_data["block"] = False # Do not evaluate the node
        self.internal_data["priority"] = 0
        self.internal_data["hide"] = True # hide in composite node widget
        self.internal_data["port_hide_changed"] = set()
        # Add delay
        self.internal_data["delay"] = 0

        # Observed object to notify final nodes wich are continuously evaluated
        self.continuous_eval = Observed()

    def notify_listeners(self, event):
        txt, trevent = Node.is_deprecated_event(event)
        if txt:
            Observed.notify_listeners(self, trevent)
            Observed.notify_listeners(self, event)
        else:
            Observed.notify_listeners(self, event)

    def __call__(self, inputs=()):
        """ Call function. Must be overriden """
        raise NotImplementedError()

    def get_tip(self):
        return self.__doc__

    def copy_to(self, other):
        # we copy some attributes.
        self.transfer_listeners(other)
        # other.internal_data.update(self.internal_data)
        other.get_ad_hoc_dict().update(self.get_ad_hoc_dict())
        for portOld, portNew in zip(self.input_desc + self.output_desc,
                                    other.input_desc + other.output_desc):
            portOld.copy_to(portNew)

    def get_process_obj(self):
        """ Return the process obj """
        return self

    # property
    process_obj = property(get_process_obj)

    def set_factory(self, factory):
        """ Set the factory of the node (if any)
        and uptdate caption """
        self.factory = factory
        if factory:
            self.set_caption(factory.name)

    def get_input_port(self, name=None):
        """Gets port by name.

        Long description of the function functionality.

        :param name: the name of the port
        :type name: string
        :returns: Input port characterized by name
        :rtype: InputPort

        """
        index = self.map_index_in[name]
        return self.input_desc[index]

    ##############
    # Properties #
    ##############
    def get_lazy(self):
        """todo"""
        return self.internal_data.get("lazy", True)

    def set_lazy(self, data):
        """todo"""
        self.internal_data["lazy"] = data
        self.notify_listeners(("internal_data_changed", "lazy", data))

    lazy = property(get_lazy, set_lazy)

    def get_delay(self):
        """todo"""
        return self.internal_data.get("delay", 0)

    def set_delay(self, delay):
        """todo"""
        self.internal_data["delay"] = delay
        self.notify_listeners(("internal_data_changed", "delay", delay))

    delay = property(get_delay, set_delay)

    def get_block(self):
        """todo"""
        return self.internal_data.get("block", False)

    def set_block(self, data):
        """todo"""
        self.internal_data["block"] = data
        self.notify_listeners(("internal_data_changed", "blocked", data))

    block = property(get_block, set_block)

    def get_user_application(self):
        """todo"""
        return self.internal_data.get("user_application", False)

    def set_user_application(self, data):
        """todo"""
        self.internal_data["user_application"] = data
        self.notify_listeners(("internal_data_changed", "user_application", data))

    user_application = property(get_user_application, set_user_application)

    def set_caption(self, newcaption):
        """ Define the node caption """
        self.internal_data['caption'] = newcaption
        self.notify_listeners(("caption_modified", newcaption))

    def get_caption(self):
        """ Return the node caption """
        return self.internal_data.get('caption', "")

    caption = property(get_caption, set_caption)

    def is_port_hidden(self, index_key):
        """ Return the hidden state of a port """
        index = self.map_index_in[index_key]
        s = self.input_desc[index].is_hidden() # get('hide', False)
        changed = self.internal_data["port_hide_changed"]

        c = index in changed

        if(index in changed):
            return not s
        else:
            return s

    def set_port_hidden(self, index_key, state):
        """
        Set the hidden state of a port.

        :param index_key: the input port index.
        :param state: a boolean value.
        """
        index = self.map_index_in[index_key]
        s = self.input_desc[index].is_hidden() # get('hide', False)

        changed = self.internal_data["port_hide_changed"]

        if (s != state):
            changed.add(index)
            self.input_desc[index].get_ad_hoc_dict().set_metadata("hide", state)
            self.notify_listeners(("hiddenPortChange",))
        elif(index in changed):
            changed.remove(index)
            self.input_desc[index].get_ad_hoc_dict().set_metadata("hide", state)
            self.notify_listeners(("hiddenPortChange",))


    # Status
    def unvalidate_input(self, index_key, notify=True):
        """
        Unvalidate node and notify listeners.

        This method is called when the input value has changed.
        """
        self.modified = True
        index = self.map_index_in[index_key]
        if(notify):
            self.notify_listeners(("input_modified", index))
            self.continuous_eval.notify_listeners(("node_modified",))

    # Declarations
    def set_io(self, inputs, outputs):
        """
        Define the number of inputs and outputs

        :param inputs: list of dict(name='X', interface=IFloat, value=0)
        :param outputs: list of dict(name='X', interface=IFloat)
        """

        # # Values
        if(inputs is None or len(inputs) != len(self.inputs)):
            self.clear_inputs()
            if inputs:
                for d in inputs:
                    self.add_input(**d)

        if(outputs is None or len(outputs) != len(self.outputs)):
            self.clear_outputs()
            if outputs:
                for d in outputs:
                    self.add_output(**d)

        # to_script
        self._to_script_func = None

    def clear_inputs(self):
        # Values
        self.inputs = []
        # Description (list of dict (name=, interface=, ...))
        self.input_desc = []
        # translation of name to id or id to id (identity)...
        self.map_index_in = {}
        # Input states : "connected", "hidden"
        self.input_states = []
        self.notify_listeners(("cleared_input_ports",))

    def clear_outputs(self):
        # Values
        self.outputs = []
        # Description (list of dict (name=, interface=, ...))
        self.output_desc = []
        # translation of name to id or id to id (identity)...
        self.map_index_out = {}
        self.notify_listeners(("cleared_output_ports",))


    def add_input(self, **kargs):
        """ Create an input port """

        # Get parameters
        name = str(kargs['name'])
        interface = kargs.get('interface', None)

        # default value
        if(interface and not kargs.has_key('value')):
            if isinstance(interface, str):
                # Create mapping between interface name and interface class
                from openalea.core.interface import TypeNameInterfaceMap
                interface = TypeNameInterfaceMap()[interface]
                kargs['interface'] = interface

            value = interface.default()
        else:
            value = kargs.get('value', None)

        value = copy(value)

        name = str(name) # force to have a string
        self.inputs.append(None)

        port = InputPort(self)
        port.update(kargs)
        self.input_desc.append(port)

        self.input_states.append(None)
        index = len(self.inputs) - 1
        self.map_index_in[name] = index
        self.map_index_in[index] = index
        port.set_id(index)

        self.set_input(name, value, False)
        port.get_ad_hoc_dict().set_metadata("hide",
                                            kargs.get("hide", False))
        self.notify_listeners(("input_port_added", port))
        return port

    def add_output(self, **kargs):
        """ Create an output port """

        # Get parameters
        name = str(kargs['name'])
        self.outputs.append(None)

        port = OutputPort(self)
        port.update(kargs)
        self.output_desc.append(port)
        index = len(self.outputs) - 1
        self.map_index_out[name] = index
        self.map_index_out[index] = index
        port.set_id(index)
        self.notify_listeners(("output_port_added", port))
        return port

    # I/O Functions

    def set_input(self, key, val=None, notify=True):
        """
        Define the input value for the specified index/key
        """
        index = self.map_index_in[key]

        changed = True
        if(self.lazy):
            # Test if the inputs has changed
            try:
                changed = (cmp(self.inputs[index], val) != 0)
            except:
                pass

        if(changed):
            self.inputs[index] = val
            self.unvalidate_input(index, notify)

    def set_output(self, key, val):
        """
        Define the input value for the specified index/key
        """

        index = self.map_index_out[key]
        self.outputs[index] = val
        self.notify_listeners(("output_modified", key, val))

    def output(self, key):
        return self.get_output(key)

    def get_input(self, index_key):
        """ Return the input value for the specified index/key """
        index = self.map_index_in[index_key]
        return self.inputs[index]

    def get_output(self, index_key):
        """ Return the output for the specified index/key """
        index = self.map_index_out[index_key]
        return self.outputs[index]

    def get_input_state(self, index_key):
        index = self.map_index_in[index_key]
        return self.input_states[index]

    def set_input_state(self, index_key, state):
        """ Set the state of the input index/key (state is a string) """

        index = self.map_index_in[index_key]
        self.input_states[index] = state
        self.unvalidate_input(index)

    def get_nb_input(self):
        """ Return the nb of input ports """
        return len(self.inputs)

    def get_nb_output(self):
        """ Return the nb of output ports """
        return len(self.outputs)

    # Functions used by the node evaluator

    def eval(self):
        """
        Evaluate the node by calling __call__
        Return True if the node needs a reevaluation
        and a timed delay if the node needs a reevaluation at a later time.
        """
        # lazy evaluation
        if self.block and self.get_nb_output() != 0 and self.output(0) is not None:
            return False
        if (self.delay == 0 and self.lazy) and not self.modified:
            return False

        self.notify_listeners(("start_eval",))

        # Run the node
        outlist = self.__call__(self.inputs)

        # Copy outputs
        # only one output
        if len(self.outputs) == 1:
            try:
                if hasattr(outlist, "__getitem__") and len(outlist) == 1:
                    self.outputs[0] = outlist[0]
                else:
                    self.outputs[0] = outlist
            except TypeError:
                self.outputs[0] = outlist

            self.output_desc[0].notify_listeners(("tooltip_modified",))

        else: # multi output
            if(not isinstance(outlist, tuple) and
               not isinstance(outlist, list)):
                outlist = (outlist,)

            for i in range(min(len(outlist), len(self.outputs))):
                self.output_desc[i].notify_listeners(("tooltip_modified",))
                self.outputs[i] = outlist[i]

        # Set State
        self.modified = False
        self.notify_listeners(("stop_eval",))

        if self.delay == 0:
            return False
        return self.delay

    def __getstate__(self):
        """ Pickle function : remove not saved data"""

        odict = self.__dict__.copy()
        odict.update(AbstractNode.__getstate__(self))

        odict['modified'] = True


        outputs = range(len(self.outputs))
        for i in range(self.get_nb_output()):
            try:
                outputs[i] = copy(self.outputs[i])
            except:
                outputs[i] = None
        odict['outputs'] = outputs

        inputs = range(self.get_nb_input())
        for i in range(self.get_nb_input()):
            try:
                inputs[i] = copy(self.inputs[i])
            except:
                inputs[i] = None
        odict['inputs'] = inputs

        in_ports = []
        out_ports = []

        for i, port in enumerate(self.input_desc):
            port.vertex = None
            in_ports.append(copy(port))
            port.vertex = ref(self)

        for i, port in enumerate(self.output_desc):
            port.vertex = None
            out_ports.append(copy(port))
            port.vertex = ref(self)

        odict['input_desc'] = in_ports
        odict['output_desc'] = out_ports

        return odict

    def __setstate__(self, dict):
        self.__dict__.update(dict)

        for port in self.input_desc:
            port.vertex = ref(self)
        for port in self.output_desc:
            port.vertex = ref(self)

    def reload(self):
        """ Reset ports """
        for i in range(self.get_nb_output()):
            self.outputs[i] = None

        i = self.get_nb_input()
        for i in xrange(i):
            # if(not connected or self.input_states[i] is "connected"):
            self.set_input(i, self.input_desc[i].get('value', None))

        if(i > 0):
            self.invalidate()

    def reset(self):
        """ Reset ports """
        for i in range(self.get_nb_output()):
            self.outputs[i] = None

        i = self.get_nb_input()

        if(i > 0):
            self.invalidate()

    def invalidate(self):
        """ Invalidate node """

        self.modified = True
        self.notify_listeners(("input_modified", -1))

        self.continuous_eval.notify_listeners(("node_modified", self))

# X     @property
# X     def outputs(self):
# X         return [self.output(i) for i in range(self.get_nb_output())]

    def to_script (self):
        """Script translation of this node.
        """
        if self._to_script_func is None :
            return "#node %s do not define any scripting\n" % self.factory.name
        else :
            return self._to_script_func(self.inputs, self.outputs)


class FuncNode(Node):
    """ Node with external function or function """

    def __init__(self, inputs, outputs, func):
        """
        :param inputs: list of dict(name='X', interface=IFloat, value=0)
        :param outputs: list of dict(name='X', interface=IFloat)
        :param func: A function
        """

        Node.__init__(self, inputs, outputs)
        self.func = func
        self.__doc__ = func.__doc__

    def __call__(self, inputs=()):
        """ Call function. Must be overriden """
        if(self.func):
            return self.func(*inputs)

    def get_process_obj(self):
        """ Return the process obj """

        return self.func

    process_obj = property(get_process_obj)


class AbstractFactory(Observed):
    """
    Abstract Factory is Factory base class
    """

    mimetype = "openalea/nodefactory"

    def __init__(self,
                 name,
                 description='',
                 category='',
                 inputs=(),
                 outputs=(),
                 lazy=True,
                 delay=0,
                 view=None,
                 alias=None,
                 authors=None,
                 **kargs):
        """
        Create a factory.

        :param name: user name for the node (must be unique) (String)
        :param description: description of the node (String)
        :param category: category of the node (String)
        :param inputs: inputs description
        :param outputs: outputs description, value=0
        :param lazy: enable lazy evaluation (default = False)
        :param view: custom view (default = None)
        :param alias: list of alias name
        :param authors: authors of the node. If Node, it should be replaced by the package authors.

        .. note:: inputs and outputs parameters are list of dictionnary such

        inputs = (dict(name='x', interface=IInt, value=0,)
        outputs = (dict(name='y', interface=IInt)
        """
        Observed.__init__(self)

        # Factory info
        self.name = name
        self.description = description
        self.category = category

        self.__pkg__ = None
        self.__pkg_id__ = None

        self.inputs = inputs
        self.outputs = outputs

        self.lazy = lazy
        self.view = view
        self.delay = delay
        self.alias = alias
        self.authors = authors
    # Package property

    def set_pkg(self, port):
        """
        An openalea package contains factories.
        The factory has a link to this package (weakref).
        The package id is the name of the package when the package is the
        Python object.
        """
        if(not port):
            self.__pkg__ = None
            self.__pkg_id = None
        else:
            self.__pkg__ = ref(port)
            self.__pkg_id__ = port.get_id()

        return port

    def get_pkg(self):
        """todo"""
        if(self.__pkg__):
            port = self.__pkg__()
        else:
            port = None
        # Test if pkg has been reloaded
        # In this case the weakref is not valid anymore
        if(not port and self.__pkg_id__):
            from openalea.core.pkgmanager import PackageManager
            port = self.set_pkg(PackageManager()[self.__pkg_id__])
        return port

    package = property(get_pkg, set_pkg)

    def is_valid(self):
        """
        Return True if the factory is valid
        else raise an exception
        """
        return True

    def get_id(self):
        """ Returns the node factory Id """
        return self.name

    def get_documentation(self):
        return ""

    def get_python_name(self):
        """
        Returns a valid python variable as name.
        This is used to store the factory into a python list (i.e. __all__).
        """

        name = self.name

        if(not name.isalnum()):
            name = '_%s' % (id(self))
        return name

    def get_authors(self):
        """returns node authors

        if no authors is found within the node, then it takes the authors field
        found in its package.
        """
        if self.authors == None or self.authors == '':
            authors = self.package.metainfo['authors'] + ' (wralea authors)'
        else:
            authors = self.authors
        return authors

    def get_tip(self, asRst=False):
        """ Return the node description

        if no authors is found within the node, then it takes the authors field
        found in its package.
        """


        if not asRst:
            return "<b>Name:</b> %s<br/>" % (self.name,) + \
                   "<b>Category:</b> %s<br/>" % (self.category,) + \
                   "<b>Package:</b> %s<br/>" % (self.package.name,) + \
                   "<b>Authors:</b> %s<br/>" % (self.get_authors(),) + \
                   "<b>Description:</b> %s<br/>" % (self.description,)
        else:
            return "**Name:** %s\n\n" % (self.name,) + \
                   "**Category:** %s\n\n" % (self.category,) + \
                   "**Package:** %s\n\n" % (self.package.name,) + \
                   "**Authors:** %s\n\n" % (self.get_authors(),) + \
                   "**Description:** %s\n\n" % (self.description,)

    def instantiate(self, call_stack=[]):
        """ Return a node instance

        :param call_stack: the list of NodeFactory id already in call stack
            (in order to avoir infinite recursion)
        """
        raise NotImplementedError()

    def instantiate_widget(self, node=None, parent=None, edit=False,
        autonomous=False):
        """ Return the corresponding widget initialised with node"""
        raise NotImplementedError()

    def get_writer(self):
        """ Return the writer class """
        raise NotImplementedError()

    def copy(self, **args):
        """ Copy factory """

        # Disable package before copy
        pkg = self.package
        self.package = None

        ret = deepcopy(self)
        self.packageg = pkg

        old_pkg, new_pkg = args['replace_pkg']

        ret.package = new_pkg
        return ret

    def clean_files(self):
        """ Remove files depending of factory """
        pass

    def is_data(self):
        return False

    def is_node(self):
        return False

    def is_composite_node(self):
        return False

    def __getstate__(self):
        odict = self.__dict__.copy() # copy the dict since we change it
        odict['__pkg__'] = None # remove weakref reference
        return odict

    def __setstate__(self, dict):
        self.__dict__.update(dict)
        self.get_pkg()


def Alias(factory, name):
    """ Create a alias for factory """
    if(factory.alias is None):
        factory.alias = [name]
    else:
        factory.alias.append(name)


class NodeFactory(AbstractFactory):
    """
    A Node factory is able to create nodes on demand,
    and their associated widgets.
    """

    def __init__(self,
                 name,
                 description='',
                 category='',
                 inputs=None,
                 outputs=None,
                 nodemodule='',
                 nodeclass=None,
                 widgetmodule=None,
                 widgetclass=None,
                 search_path=None,
                 authors=None,
                 **kargs):
        """Create a node factory.

        :param name: user name for the node (must be unique) (String)
        :param description: description of the node (String)
        :param category: category of the node (String)
        :param inputs: inputs description
        :param outputs: outputs description
        :param nodemodule: python module to import for node (String)
        :param nodeclass:  node class name to be created (String)
        :param widgetmodule: python module to import for widget (String)
        :param widgetclass: widget class name (String)
        :param search_path: list of directories where to search for
            module

        :note: inputs and outputs parameters are list of dictionnary such

        inputs = (dict(name='x', interface=IInt, value=0,)
        outputs = (dict(name='y', interface=IInt)
        """
        AbstractFactory.__init__(self, name, description, category,
                                 inputs, outputs, authors=authors, **kargs)

        # Factory info
        self.nodemodule_name = nodemodule
        self.nodeclass_name = nodeclass
        self.widgetmodule_name = widgetmodule
        self.widgetclass_name = widgetclass

        self.toscriptclass_name = kargs.get("toscriptclass_name", None)

        # Cache
        self.nodeclass = None
        self.src_cache = None

        # Module path, value=0
        self.nodemodule_path = None
        if(not search_path):
            self.search_path = []
        else:
            self.search_path = search_path

        self.module_cache = None

        # Context directory
        # inspect.stack()[1][1] is the caller python module
        caller_dir = os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
        if(not caller_dir in self.search_path):
            self.search_path.append(caller_dir)


    def is_node(self):
        return True

    def get_python_name(self):
        """ Return a python valid name """

        module_name = self.nodemodule_name
        module_name = module_name.replace('.','_')
        return "%s_%s" % (self.nodemodule_name, self.nodeclass_name)

    def __getstate__(self):
        """ Pickle function """
        odict = self.__dict__.copy()
        odict['nodemodule_path'] = None
        odict['nodemodule'] = None
        odict['nodeclass'] = None
        odict['module_cache'] = None
        odict['__pkg__'] = None # remove weakref reference

        return odict

    def __setstate__(self, dict):
        self.__dict__.update(dict)
        self.get_pkg()

    def copy(self, **args):
        """ Copy factory
        :param path: new search path
        """

        ret = AbstractFactory.copy(self, **args)
        ret.search_path = [args['path']]
        return ret

    def get_classobj(self):
        module = self.get_node_module()
        classobj = module.__dict__.get(self.nodeclass_name, None)
        return classobj

    def get_documentation(self):
        return self.get_classobj().__doc__

    def instantiate(self, call_stack=[]):
        """
        Returns a node instance.
        :param call_stack: the list of NodeFactory id already in call stack
        (in order to avoir infinite recursion)
        """

        # The module contains the node implementation.
        module = self.get_node_module()
        classobj = module.__dict__.get(self.nodeclass_name, None)

        if classobj is None:
            raise Exception("Cannot instantiate '" + \
                self.nodeclass_name + "' from " + str(module))

        # If class is not a Node, embed object in a Node class
        if(not hasattr(classobj, 'mro') or not AbstractNode in classobj.mro()):

            # Check inputs and outputs
            if(self.inputs is None):
                sign = sgn.Signature(classobj)
                self.inputs = sign.get_parameters()
            if(self.outputs is None):
                self.outputs = (dict(name="out", interface=None),)


            # Check and Instantiate if we have a functor class
            if((type(classobj) == types.TypeType)
               or (type(classobj) == types.ClassType)):

                _classobj = classobj()
                if callable(_classobj):
                    classobj = _classobj

            node = FuncNode(self.inputs, self.outputs, classobj)

        # Class inherits from Node
        else:
            try:
                node = classobj(self.inputs, self.outputs)
            except TypeError, e:
                node = classobj()

        # Properties
        try:
            node.factory = self
            node.lazy = self.lazy
            if(not node.caption):
                node.set_caption(self.name)

            node.delay = self.delay
        except:
            pass

        # to script
        if self.toscriptclass_name is not None :
            node._to_script_func = module.__dict__.get(self.toscriptclass_name, None)

        return node

    def instantiate_widget(self, node=None, parent=None,
                            edit=False, autonomous=False):
        """ Return the corresponding widget initialised with node """

        # Code Editor
        if(edit):
            from openalea.visualea.code_editor import get_editor
            w = get_editor()(parent)
            try:
                w.edit_module(self.get_node_module(), self.nodeclass_name)
            except Exception, e:
                # Unable to load the module
                # Try to retrieve the file and open the file in an editor
                src_path = self.get_node_file()
                print "instantiate widget exception:", e
                if src_path:
                    w.edit_file(src_path)
            return w

        # Node Widget
        if(node == None):
            node = self.instantiate()

        modulename = self.widgetmodule_name
        if(not modulename):
            modulename = self.nodemodule_name

        # if no widget declared, we create a default one
        if(not modulename or not self.widgetclass_name):

            from openalea.visualea.node_widget import DefaultNodeWidget
            return DefaultNodeWidget(node, parent, autonomous)

        else:
            # load module
            (file, pathname, desc) = imp.find_module(modulename,
                self.search_path + sys.path)

            sys.path.append(os.path.dirname(pathname))
            module = imp.load_module(modulename, file, pathname, desc)
            sys.path.pop()

            if(file):
                file.close()

            widgetclass = module.__dict__[self.widgetclass_name]
            return widgetclass(node, parent)

    def get_writer(self):
        """ Return the writer class """

        return PyNodeFactoryWriter(self)

    def get_node_module(self):
        """
        Return the python module object (if available)
        Raise an Import Error if no module is associated
        """
        LOCAL_IMPORT = False

        if not self.nodemodule_name:
            self.nodemodule_name = '__builtin__'

        # Test if the module is already in sys.modules
        if (self.nodemodule_path and
            self.module_cache and
            not hasattr(self.module_cache, 'oa_invalidate')):
            return self.module_cache

        sav_path = sys.path
        sys.path = self.search_path + sav_path
        # print 'SEARCH PATH ', self.search_path
        try:
            # load module

            # Delete the module from the sys.modules if another local exists and
            # has the same name
            if LOCAL_IMPORT:
                if self.nodemodule_name in sys.modules:
                    del sys.modules[self.nodemodule_name]
            __import__(self.nodemodule_name)
            nodemodule = sys.modules[self.nodemodule_name]
            try:
                self.nodemodule_path = inspect.getsourcefile(nodemodule)
            except TypeError, type_error:
                self.nodemodule_path = None
                print type_error

            self.module_cache = nodemodule
            sys.path = sav_path
            return nodemodule

        except ImportError, import_error:
            sys.path = sav_path
            print self.nodemodule_name
            raise import_error
        else:
            sys.path = sav_path

    def get_node_file(self):
        """
        Return the path of the python module.

        """

        if self.nodemodule_path or self.module_cache:
            return self.nodemodule_path
        elif self.nodemodule_name:
            self.get_node_module()
            return self.nodemodule_path


    def get_node_src(self, cache=True):
        """
        Return a string containing the node src
        Return None if src is not available
        If cache is False, return the source on the disk
        """

        # Return cached source if any
        if(self.src_cache and cache):
            return self.src_cache

        module = self.get_node_module()

        import linecache
        # get the code
        linecache.checkcache(self.nodemodule_path)
        cl = module.__dict__[self.nodeclass_name]
        return inspect.getsource(cl)

    def apply_new_src(self, newsrc):
        """
        Execute new src and store the source into the factory.
        """
        module = self.get_node_module()

        # Run src
        exec newsrc in module.__dict__

        # save the current newsrc
        self.src_cache = newsrc

    def save_new_src(self, newsrc):
        """
        Execute the new source and replace the text into the old file
        containing the source.
        """
        module = self.get_node_module()
        nodesrc = self.get_node_src(cache=False)

        # Run src
        exec newsrc in module.__dict__

        # get the module code
        import inspect
        modulesrc = inspect.getsource(module)

        # Pass if no modications
        if(nodesrc == newsrc):
            return

        # replace old code with new one
        modulesrc = modulesrc.replace(nodesrc, newsrc)


        # write file
        myfile = open(self.nodemodule_path, 'w')
        myfile.write(modulesrc)
        myfile.close()

        # reload module
        if(self.module_cache):
            self.module_cache.invalidate_oa = True

        self.src_cache = None
        m = self.get_node_module()
        # reload(m)
        # Recompile
        # import py_compile
        # py_compile.compile(self.nodemodule_path)

# Class Factory:
Factory = NodeFactory


class PyNodeFactoryWriter(object):
    """ NodeFactory python Writer """

    nodefactory_template = """

$NAME = Factory(name=$PNAME,
                authors=$AUTHORS,
                description=$DESCRIPTION,
                category=$CATEGORY,
                nodemodule=$NODEMODULE,
                nodeclass=$NODECLASS,
                inputs=$LISTIN,
                outputs=$LISTOUT,
                widgetmodule=$WIDGETMODULE,
                widgetclass=$WIDGETCLASS,
               )

"""

    def __init__(self, factory):
        self.factory = factory

    def __repr__(self):
        """ Return the python string representation """
        f = self.factory
        fstr = string.Template(self.nodefactory_template)
        
        name = f.get_python_name()
        name = name.replace('.', '_')
        result = fstr.safe_substitute(NAME=name,
                                      AUTHORS=repr(f.get_authors()),
                                      PNAME=repr(f.name),
                                      DESCRIPTION=repr(f.description),
                                      CATEGORY=repr(f.category),
                                      NODEMODULE=repr(f.nodemodule_name),
                                      NODECLASS=repr(f.nodeclass_name),
                                      LISTIN=repr(f.inputs),
                                      LISTOUT=repr(f.outputs),
                                      WIDGETMODULE=repr(f.widgetmodule_name),
                                      WIDGETCLASS=repr(f.widgetclass_name),)
        return result

# Utility functions
def gen_port_list(size):
    """ Generate a list of port description """
    mylist = []
    for i in range(size):
        mylist.append(dict(name='t' + str(i), interface=None, value=i))
    return mylist


def initialise_standard_metadata():
    """Declares the standard keys used by the Node structures. Called at the end of this file"""
    # we declare what are the node model ad hoc data we require:
    AbstractNode.extend_ad_hoc_slots("position", list, [0, 0], "posx", "posy")
    Node.extend_ad_hoc_slots("userColor", list, None, "user_color")
    Node.extend_ad_hoc_slots("useUserColor", bool, True, "use_user_color",)
    Annotation.extend_ad_hoc_slots("text", str, "", "txt")
#    Annotation.extend_ad_hoc_slots("htmlText", str, None)
    Annotation.extend_ad_hoc_slots("textColor", list, None)
    Annotation.extend_ad_hoc_slots("rectP2", tuple, (-1, -1))
    Annotation.extend_ad_hoc_slots("color", list, None)
    Annotation.extend_ad_hoc_slots("visualStyle", int, None)
    # we declare what are the node model ad hoc data we require:
    AbstractPort.extend_ad_hoc_slots("hide" , bool, False)
    AbstractPort.extend_ad_hoc_slots("connectorPosition", list, [0, 0])


initialise_standard_metadata()
