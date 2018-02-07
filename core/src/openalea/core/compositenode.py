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
##############################################################################
"""A CompositeNode is a Node that contains other nodes connected in a directed
graph. A CompositeNodeFactory instance is a factory that build CompositeNode
instances. Different instances of the same factory can coexist and can be
modified in a dataflow.
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import string
import pprint
import copy

from openalea.core.node import AbstractFactory, AbstractPort, Node
from openalea.core.node import RecursionError
from openalea.core.pkgmanager import PackageManager, protected, UnknownPackageError
from openalea.core.package import UnknownNodeError
from openalea.core.dataflow import DataFlow, InvalidEdge, PortError
from openalea.core.settings import Settings
from openalea.core.metadatadict import MetaDataDict
import logger

quantify = False

class IncompatibleNodeError(Exception):
    """todo"""
    pass


class CompositeNodeFactory(AbstractFactory):

    mimetype = "openalea/compositenodefactory"

    """
    The CompositeNodeFactory is able to create CompositeNode instances
    Each node has an unique id : the element id (elt_id)
    """

    def __init__(self, *args, **kargs):
        """
        CompositeNodeFactory accept more optional parameters:

        - inputs: list of dict(name = '', interface='', value='')
        - outputs: list of dict(name = '', interface='', value='')
        - doc: documentation
        - elt_factory: map of elements with its corresponding factory
        - elt_connections: map of ( dst_id , input_port ):(src_id,output_port)
        - elt_data: Dictionary containing associated data
        - elt_value: Dictionary containing Lists of 2-uples (port, value)
        """
        # Init parent (name, description, category, doc, node, widget=None)
        AbstractFactory.__init__(self, *args, **kargs)
        # A CompositeNode is composed by a set of element indexed by an elt_id
        # Each element is associated to NodeFactory
        # Each element will generate an node instance in the real CompositeNode

        # Dict mapping elt_id with its corresponding factory
        # the factory is identified by its unique id (package_id, factory_id)
        self.elt_factory = kargs.get("elt_factory", {})

        # Dictionnary which contains tuples describing connection
        # ( source_vid , source_port ) : ( target_vid, target_port )
        self.connections = kargs.get("elt_connections", {})

        self.elt_data = kargs.get("elt_data", {})
        self.elt_value = kargs.get("elt_value", {})
        self.elt_ad_hoc = kargs.get("elt_ad_hoc", {})
        from openalea.core.algo.dataflow_evaluation import DefaultEvaluation
        self.eval_algo = kargs.get("eval_algo", DefaultEvaluation.__name__)

        # Documentation
        self.doc = kargs.get('doc', "")
        self.__doc__ = self.doc

    def is_composite_node(self):
        return True

    def get_documentation(self):
        return self.__doc__

    def clear(self):
        """todo"""
        self.elt_factory.clear()
        self.connections.clear()
        self.elt_data.clear()
        self.elt_value.clear()

    def copy(self, **args):
        """
        Copy factory.

        :param path: new search path
        :param replace_pkg: old and new package names.

        When replace package is set, change the package id for all the
        elt factories.
        """

        ret = AbstractFactory.copy(self, **args)

        # Replace old pkg name to new pkg name
        (old_pkg, new_pkg) = args['replace_pkg']

        for k, v in ret.elt_factory.iteritems():
            pkg_id, factory_id = v

            if(pkg_id == old_pkg.get_id()):
                pkg_id = new_pkg.get_id()
                ret.elt_factory[k] = pkg_id, factory_id

        return ret

    def get_writer(self):
        """ Return the writer class """

        return PyCNFactoryWriter(self)

    def instantiate(self, call_stack=None):
        """ Create a CompositeNode instance and allocate all elements
        This function overide default implementation of NodeFactory

        :param call_stack: the list of NodeFactory id already in recursion stack (in order to avoid infinite loop)

        """

        # Test for infinite loop
        if (not call_stack):
            call_stack = []
        if (self.get_id() in call_stack):
            raise RecursionError()

        call_stack.append(self.get_id())

        new_df = CompositeNode(self.inputs, self.outputs)
        new_df.factory = self
        new_df.__doc__ = self.doc
        new_df.set_caption(self.get_id())
        new_df.eval_algo = self.eval_algo

        cont_eval = set() # continuous evaluated nodes

        # Instantiate the node with each factory
        for vid in self.elt_factory:
            try:
                node = self.instantiate_node(vid, call_stack)

                # Manage continuous eval
                if(node.user_application):
                    cont_eval.add(vid)

            except (UnknownNodeError, UnknownPackageError):

                print "WARNING : The graph is not fully operational "
                (pkg, fact) = self.elt_factory[vid]
                print "-> Cannot find '%s:%s'" % (pkg, fact)
                node = self.create_fake_node(vid)
                node.raise_exception = True
                node.notify_listeners(('data_modified', None, None ))

            new_df.add_node(node, vid, False)

        # Set IO internal data
        try:
            self.load_ad_hoc_data(new_df.node(new_df.id_in),
                                  copy.deepcopy(self.elt_data["__in__"]),
                                  copy.deepcopy(self.elt_ad_hoc.get("__in__", None)))
            self.load_ad_hoc_data(new_df.node(new_df.id_out),
                                  copy.deepcopy(self.elt_data["__out__"]),
                                  copy.deepcopy(self.elt_ad_hoc.get("__out__", None)))
        except:
            pass

        # Create the connections
        for eid, link in self.connections.iteritems():
            (source_vid, source_port, target_vid, target_port) = link

            # Replace id for in and out nodes
            if(source_vid == '__in__'):
                source_vid = new_df.id_in
            if(target_vid == '__out__'):
                target_vid = new_df.id_out

            new_df.connect(source_vid, source_port, target_vid, target_port)

        # Set continuous evaluation
        for vid in cont_eval:
             new_df.set_continuous_eval(vid, True)

        # Set call stack to its original state
        call_stack.pop()

        # Properties
        new_df.lazy = self.lazy
        new_df.graph_modified = False # Graph is not modifyied

        return new_df

    def create_fake_node(self, vid):
        """ Return an empty node with the correct number of inputs
        and output """

        # Count in and out needed
        ins = 0
        outs = 0

        for eid, link in self.connections.iteritems():
            (source_vid, source_port, target_vid, target_port) = link

            if(source_vid == vid):
                outs = max(outs, source_port)
            elif(target_vid == vid):
                ins = max(ins, target_port)

        node = Node()

        attributes = copy.deepcopy(self.elt_data[vid])
        ad_hoc     = copy.deepcopy(self.elt_ad_hoc.get(vid, None))
        self.load_ad_hoc_data(node, attributes, ad_hoc)

        # copy node input data if any
        values = copy.deepcopy(self.elt_value.get(vid, ()))

        for p in range(ins+1):
            port = node.add_input(name="In"+str(p))

        for p in range(outs+1):
            port = node.add_output(name="Out"+str(p))

        for vs in values:
            try:
                #the two first elements are the historical
                #values : port Id and port value
                #beyond that are extensions added by gengraph:
                #the ad_hoc_dict representation is third.
                port, v = vs[:2]
                node.set_input(port, eval(v))
                if(len(vs)>2):
                    d = MetaDataDict(vs[2])
                    node.input_desc[port].get_ad_hoc_dict().update(d)
            except:
                continue


        return node

    def paste(self, cnode, data_modifiers=[], call_stack=None, meta=False):
        """ Paste to an existing CompositeNode instance

        :param cnode: composite node instance
        :param data_modifiers: list of 2-uple (key, function) to apply
            to internal data (for instance to move the node)
        :param call_stack: the list of NodeFactory id already in recursion
            stack (in order to avoid infinite loop)

        :returns: the list of created id

        """

        # map to convert id
        idmap = {}

        # Instantiate the node with each factory
        for vid in self.elt_factory:
            n = self.instantiate_node(vid, call_stack)

            # Apply modifiers (if callable)
            for (key, func) in data_modifiers:
                try:
                    if(callable(func)):
                        if(meta):
                            func(n)
                        else:
                            n.internal_data[key] = func(n.internal_data[key])
                    else:
                        n.internal_data[key] = func
                except:
                    pass

            newid = cnode.add_node(n, None)
            idmap[vid] = newid

        # Create the connections
        for eid, link in self.connections.iteritems():
            (source_vid, source_port, target_vid, target_port) = link

            # convert id
            source_vid = idmap[source_vid]
            target_vid = idmap[target_vid]

            cnode.connect(source_vid, source_port, target_vid, target_port)

        return idmap.values()

    def load_ad_hoc_data(self, node, elt_data, elt_ad_hoc=None):
        if elt_ad_hoc and len(elt_ad_hoc):
            #reading 0.8+ files.
            d = MetaDataDict(dict=elt_ad_hoc)
            node.get_ad_hoc_dict().update(d)
        else:
            #extracting ad hoc data from old files.
            #we parse the Node class' __ad_hoc_from_old_map__
            #which defines conversions between new ad_hoc_dict keywords
            #and old internal_data keywords.
            #These dictionnaries are used to extend ad_hoc_dict of a node with the
            #data that views expect. See node.initialise_standard_metadata() for an example.
            if hasattr(node, "__ad_hoc_from_old_map__"):
                for newKey, oldKeys in node.__ad_hoc_from_old_map__.iteritems():
                    data = [] #list that stores the new values
                    _type, default = node.__ad_hoc_slots__.get(newKey)
                    for key in oldKeys:
                        data.append(elt_data.pop(key, None))
                    if len(data) == 1 : data = data[0]
                    if data is None or (isinstance(data, list) and None in data): #?
                        data = default
                    if data is None : continue
                    node.get_ad_hoc_dict().set_metadata(newKey, _type(data))

        #finally put the internal data (elt_data) where it has always been expected.
        node._init_internal_data(elt_data)
#        node.internal_data.update(elt_data)

    def instantiate_node(self, vid, call_stack=None):
        """ Partial instantiation

        instantiate only elt_id in CompositeNode

        :param call_stack: a list of parent id (to avoid infinite recursion)
        """
        (package_id, factory_id) = self.elt_factory[vid]
        pkgmanager = PackageManager()
        pkg = pkgmanager[package_id]
        try:
            factory = pkg.get_factory(factory_id)
        except UnknownNodeError, e:
            # Bug when both package_id and protected(package_id) exist
            pkg = pkgmanager[protected(package_id)]
            factory = pkg.get_factory(factory_id)


        node = factory.instantiate(call_stack)

        attributes = copy.deepcopy(self.elt_data[vid])
        ad_hoc     = copy.deepcopy(self.elt_ad_hoc.get(vid, None))
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

    #########################################################
    # This shouldn't be here, it is related to visual stuff #
    #########################################################
    def instantiate_widget(self, node=None, parent=None, \
            edit=False, autonomous=False):
        """
        Return the corresponding widget initialised with node

        If node is None, the node is allocated else a composite
        widget composed with the node sub widget is returned.

        """
        if(edit):
            from openalea.visualea.dataflowview import GraphicalGraph
            return GraphicalGraph(node).create_view(parent)

        if(node == None):
            node = self.instantiate()

        from openalea.visualea.compositenode_widget import DisplayGraphWidget
        return DisplayGraphWidget(node, parent, autonomous)


class CompositeNode(Node, DataFlow):
    """
    The CompositeNode is a container that interconnect
    different node instances between them in directed graph.
    """

    mimetype = "openalea/compositenode"

    def __init__(self, inputs=(), outputs=()):
        """ Inputs and outputs are list of
        dict(name='', interface='', value='') """

        DataFlow.__init__(self)

        self.id_in = None
        self.id_out = None
        Node.__init__(self, inputs, outputs)
        # graph modification status
        self.graph_modified = False
        self.evaluating = False
        self.eval_algo = None

    def copy_to(self, other):
        raise NotImplementedError

    def close(self):
        for vid in set(self.vertices()):
            node = self.actor(vid)
            node.close()
        Node.close(self)

    def reset(self):
        """ Reset nodes """

        Node.reset(self)

        for vid in set(self.vertices()):
            node = self.actor(vid)
            node.reset()

    def invalidate(self):
        """ Invalidate nodes """

        Node.invalidate(self)

        for vid in set(self.vertices()):
            node = self.actor(vid)
            node.invalidate()

    def set_io(self, inputs, outputs):
        """
        Define inputs and outputs

        Inputs and outputs are list of dict(name='', interface='', value='')
        """

        # I/O ports
        # Remove node if nb of input has changed
        if(self.id_in is not None
           and len(inputs) != self.node(self.id_in).get_nb_output()):
            self.remove_node(self.id_in)
            self.id_in = None

        if(self.id_out is not None
           and len(outputs) != self.node(self.id_out).get_nb_input()):
            self.remove_node(self.id_out)
            self.id_out = None

        # Create new io node if necessary
        if(self.id_in is None):
            self.id_in = self.add_node(CompositeNodeInput(inputs))
        else:
            self.node(self.id_in).set_io((), inputs)

        if(self.id_out is None):
            self.id_out = self.add_node(CompositeNodeOutput(outputs))
        else:
            self.node(self.id_out).set_io(outputs, ())

        Node.set_io(self, inputs, outputs)

    def set_input(self, index_key, val=None, *args):
        """ Copy val into input node output ports """
        self.node(self.id_in).set_input(index_key, val)

    def get_input(self, index_key):
        """ Return the composite node input"""
        return self.node(self.id_in).get_input(index_key)

    def get_output(self, index_key):
        """ Retrieve values from output node input ports """

        return self.node(self.id_out).get_output(index_key)

    def set_output(self, index_key, val):
        """ Set a value to an output """

        return self.node(self.id_out).set_output(index_key, val)

    def get_eval_algo(self):
        """ Return the evaluation algo instance """
        try:
            algo_str = self.eval_algo

            algo_str = algo_str.strip('"');
            algo_str = algo_str.strip("'")


            # import module
            baseimp = "algo.dataflow_evaluation"
            module = __import__(baseimp, globals(), locals(), [algo_str])
            classobj = module.__dict__[algo_str]
            return classobj(self)

        except Exception, e:
            from  openalea.core.algo.dataflow_evaluation import DefaultEvaluation
            return DefaultEvaluation(self)

        return self.eval_algo

    def eval_as_expression(self, vtx_id=None, step=False):
        """
        Evaluate a vtx_id

        if node_id is None, then all the nodes without sons are evaluated
        """
        import time
        t0 = time.time()
        if(self.evaluating):
            return
        if(vtx_id != None):
            self.node(vtx_id).modified = True
        algo = self.get_eval_algo()

        try:
            self.evaluating = True
            algo.eval(vtx_id,step=step)
        finally:
            self.evaluating = False
        t1 = time.time()
        if quantify:
            logger.info('Evaluation time: %s'%(t1-t0))
            print 'Evaluation time: %s'%(t1-t0)
    # Functions used by the node evaluator

    def eval(self, *args, **kwds):
        """
        Evaluate the graph

        Return True if the node need a reevaluation (like generator)
        """
        self.__call__()

        self.modified = False
        self.notify_listeners(("status_modified", self.modified))

        return False

    def __call__(self, inputs=()):
        """
        Evaluate the graph
        """

        if(self.id_out and self.get_nb_output()>0):
            self.eval_as_expression(self.id_out)
        else:
            self.eval_as_expression(None)

        return ()

    def to_script (self) :
        """Translate the dataflow into a python script.
        """
        from algo.dataflow_evaluation import ToScriptEvaluation
        algo = ToScriptEvaluation(self)
        return algo.eval()

    def node(self, vid):
        """ Convenience function """
        return self.actor(vid)

    def compute_external_io(self, vertex_selection, new_vid):
        """
        Return the list of input and output edges to connect the composite
        node.
        """

        ins, in_edges = \
            self._compute_inout_connection(vertex_selection, is_input=True)
        outs, out_edges = \
            self._compute_inout_connection(vertex_selection, is_input=False)

        in_edges = \
            self._compute_outside_connection(vertex_selection, in_edges,
                new_vid, is_input=True)
        out_edges = \
            self._compute_outside_connection(vertex_selection, out_edges,
                new_vid, is_input=False)

        return in_edges + out_edges

    def _compute_outside_connection(self, vertex_selection, new_connections,
                                    new_vid, is_input = True):
        """
        Return external connections of a composite node with input and output
        ports.

        :param vertex_selection: a sorted set of node.
        """
        connections = []
        selected_port = {}
        if is_input:
            ports = self.in_ports
            get_vertex_io = self.source
            get_my_vertex = self.target
        else:
            ports = self.out_ports
            get_vertex_io = self.target
            get_my_vertex = self.source

        # For each selected vertices
        for vid in vertex_selection:
            for pid in ports(vid):
                connected_edges = self.connected_edges(pid)

                for e in connected_edges:
                    s = get_vertex_io(e)
                    if s not in vertex_selection:
                        pname = self.local_id(pid)
                        selected_port.setdefault((vid, pname), []).append(e)

        for edge in new_connections:
            if is_input:
                if(edge[0] != '__in__'):
                    continue
                target_id, target_port = edge[2:]
                if (target_id, target_port) in selected_port:
                    target_edges = selected_port[(target_id, target_port)]
                    for e in target_edges:
                        vid = self.source(e)
                        port_id = self.local_id(self.source_port(e))
                        connections.append((vid, port_id, new_vid, edge[1]))
            else:
                if(edge[2] != '__out__'):
                    continue

                source_id, source_port = edge[0:2]
                if (source_id, source_port) in selected_port:
                    source_edges = selected_port[(source_id, source_port)]
                    for e in source_edges:
                        vid = self.target(e)
                        port_id = self.local_id(self.target_port(e))
                        connections.append((new_vid, edge[3], vid, port_id))

        return connections

    def _compute_inout_connection(self, vertex_selection, is_input=True):
        """ Return internal connections of a composite node with input or
        output port.

            - vertex_selection is a sorted set of node.
            - is_input is a boolean indicated if connection have to be
                created with input or output ports.
        """
        nodes = []
        connections = []

        # just to select unique name
        name_port = []

        if is_input:
            ports = self.in_ports
            get_vertex_io = self.source
            io_desc = lambda n: n.input_desc
        else:
            ports = self.out_ports
            get_vertex_io = self.target
            io_desc = lambda n: n.output_desc

        # For each input port
        for vid in vertex_selection:
            for pid in ports(vid):
                connected_edges = list(self.connected_edges(pid))

                is_io = False
                for e in connected_edges:
                    s = get_vertex_io(e)
                    if s not in vertex_selection:
                        is_io = True

                if connected_edges:
                    if not is_io:
                        continue

                pname = self.local_id(pid)
                n = self.node(vid)
                desc = dict(io_desc(n)[pname])

                caption= '(%s)' % (n.get_caption())
                count = ''
                name = desc['name']

                while name + str(count) + caption in name_port:
                    if count:
                        count += 1
                    else:
                        count = 1

                desc['name'] = name + str(count) + caption
                name_port.append(desc['name'])

                if is_input:
                    # set default value on cn input port
                    if n.inputs[pname]:
                        v = n.inputs[pname]

                        try:
                            eval(repr(v))
                            desc['value'] = v
                        except:
                            pass

                    if 'value' not in desc:
                        if 'interface' in desc and desc['interface']:
                            desc['value'] = desc['interface'].default()

                    connections.append(('__in__', len(nodes), vid, pname))
                else: # output
                    connections.append((vid, pname, '__out__', len(nodes)))

                nodes.append(desc)

        return (nodes, connections)

    def compute_io(self, v_list=None):
        """
        Return (inputs, outputs, connections)

        representing the free port of node
        v_list is a vertex id list
        """


        ins, in_edges = self._compute_inout_connection(v_list, is_input=True)
        outs, out_edges = \
            self._compute_inout_connection(v_list, is_input=False)
        connections = in_edges + out_edges

        return (ins, outs, connections)

    def to_factory(self, sgfactory, listid = None, auto_io=False):
        """
        Update CompositeNodeFactory to fit with the graph

        listid is a list of element to export. If None, select all id.
        if auto_io is true :  inputs and outputs are connected to the free
        ports
        """

        # Clear the factory
        sgfactory.clear()

        # Properties
        sgfactory.lazy = self.lazy
        sgfactory.eval_algo = self.eval_algo
        #print self.eval_algo
        # I / O
        if(auto_io):
            (ins, outs, sup_connect) = self.compute_io(listid)
            sgfactory.inputs = ins
            sgfactory.outputs = outs
        else:
            sgfactory.inputs = [dict(val) for val in self.input_desc]
            sgfactory.outputs = [dict(val) for val in self.output_desc]
            sup_connect = []

        if listid is None:
            listid = set(self.vertices())

        # Copy Connections
        for eid in self.edges():

            src = self.source(eid)
            tgt = self.target(eid)

            if((src not in listid) or (tgt not in listid)):
                continue
            if(src == self.id_in):
                src = '__in__'
            if(tgt == self.id_out):
                tgt = '__out__'

            source_port = self.local_id(self.source_port(eid))
            target_port = self.local_id(self.target_port(eid))
            sgfactory.connections[id(eid)] = \
                (src, source_port, tgt, target_port)

        # Add supplementary connections
        for e in sup_connect:
            sgfactory.connections[id(e)] = e

        # Copy node
        for vid in listid:

            node = self.actor(vid)
            kdata = node.internal_data

            # Do not copy In and Out
            if(vid == self.id_in):
                vid = "__in__"
            elif(vid == self.id_out):
                vid = "__out__"
            else:
                pkg_id = node.factory.package.get_id()
                factory_id = node.factory.get_id()
                sgfactory.elt_factory[vid] = (pkg_id, factory_id)

            # Copy internal data
            sgfactory.elt_data[vid] = copy.deepcopy(kdata)
            # Forward compatibility for versions earlier than 0.8.0
            # We do the exact opposite than in load_ad_hoc_data, have a look there.
            if hasattr(node, "__ad_hoc_from_old_map__"):
                for newKey, oldKeys in node.__ad_hoc_from_old_map__.iteritems():
                    if len(oldKeys)==0: continue
                    data = node.get_ad_hoc_dict().get_metadata(newKey)
                    for pos, newKey in enumerate(oldKeys):
                        sgfactory.elt_data[vid][newKey] = data[pos] if isinstance(data, list) else data

            # Copy ad_hoc data
            sgfactory.elt_ad_hoc[vid] = copy.deepcopy(node.get_ad_hoc_dict())

            # Copy value
            if(not node.get_nb_input()):
                sgfactory.elt_value[vid] = []
            else:
                sgfactory.elt_value[vid] = \
                    [(port, repr(node.get_input(port))) for port
                        in xrange(len(node.inputs))
                        if node.input_states[port] is not "connected"]

        self.graph_modified = False

        # Set node factory if all node have been exported
        if(listid is None):
            self.factory = sgfactory

    def add_node(self, node, vid = None, modify=True):
        """
        Add a node in the Graph with a particular id
        if id is None, autogenrate one

        :param node: the node instance
        :param vid: element id

        :return: the id
        """
        vid = self.add_vertex(vid)

        # -- NOOOOOO THE UGLY BACK REFERENCE --
        node.set_compositenode(self)

        node.set_id(vid)
        for local_pid in xrange(node.get_nb_input()):
            self.add_in_port(vid, local_pid)

        for local_pid in xrange(node.get_nb_output()):
            self.add_out_port(vid, local_pid)

        self.set_actor(vid, node)
        self.notify_vertex_addition(node, vid)

        #self.id_cpt += 1
        if(modify):
            self.notify_listeners(("graph_modified", ))
            self.graph_modified = True

        return vid

    def notify_vertex_addition(self, vertex, vid=None):
        vtype = "vertex"
        doNotify = True
        if(vertex.__class__.__dict__.has_key("__graphitem__")): vtype = "annotation"
        elif isinstance(vertex, CompositeNodeOutput):
            vtype = "outNode"
            doNotify = True if len(vertex.input_desc) else False
        elif isinstance(vertex, CompositeNodeInput) :
            vtype = "inNode"
            doNotify = True if len(vertex.output_desc) else False
        else: pass
        if doNotify:
            self.notify_listeners(("vertex_added", (vtype, vertex)))

    def notify_vertex_removal(self, vertex):
        vtype = "vertex"
        doNotify = True
        if(vertex.__class__.__dict__.has_key("__graphitem__")): vtype = "annotation"
        elif isinstance(vertex, CompositeNodeOutput): vtype = "outNode"
        elif isinstance(vertex, CompositeNodeInput) : vtype = "inNode"
        else: pass
        self.notify_listeners(("vertex_removed", (vtype, vertex)))

    def remove_node(self, vtx_id):
        """
        remove a node from the graph
        :param vtx_id: element id
        """
        node = self.node(vtx_id)
        if vtx_id == self.id_in : self.id_in = None
        elif vtx_id == self.id_out : self.id_out = None
        self.remove_vertex(vtx_id)
        node.close()
        self.notify_vertex_removal(node)
        self.notify_listeners(("graph_modified", ))
        self.graph_modified = True

    def remove_edge(self, eid):
        target = self.target(eid)
        try:
            port = self.port(target)
        except PortError:
            port = None
        DataFlow.remove_edge(self, eid)
        if port:
            self.actor(port._vid).set_input_state(port._local_pid, "disconnected")
        self.notify_listeners(("edge_removed", ("default",eid) ))


    def simulate_destruction_notifications(self):
        """emits messages as if we were adding elements to
        the composite node"""
        Node.simulate_destruction_notifications(self)

        ids = self.vertices()
        for eltid in ids:
            node = self.node(eltid)
            self.notify_vertex_removal(node)

        for eid in self.edges():
            (src_id, dst_id) = self.source(eid), self.target(eid)
            etype=None
            src_port_id = self.local_id(self.source_port(eid))
            dst_port_id = self.local_id(self.target_port(eid))

            nodeSrc = self.node(src_id)
            nodeDst = self.node(dst_id)
            src_port = nodeSrc.output_desc[src_port_id]
            dst_port = nodeDst.input_desc[dst_port_id]

            #don't notify if the edge is connected to the input or
            #output nodes.
            # if(src_id == self.id_in or dst_id == self.id_out):
                # continue

            edgedata = "default", eid
            self.notify_listeners(("edge_removed", edgedata))

    def connect(self, src_id, port_src, dst_id, port_dst):
        """ Connect 2 elements

        :param src_id: source node id
        :param port_src: source output port number
        :param dst_id: destination node id
        :param port_dst: destination input port number
        """

        try:
            source_pid = self.out_port(src_id, port_src)
            target_pid = self.in_port(dst_id, port_dst)
            eid = DataFlow.connect(self, source_pid, target_pid)
        except:
            logger.error("Enable to create the edge %s %d %d %d %d"%( self.factory.name,  src_id, port_src, dst_id, port_dst))
            return

        self.actor(dst_id).set_input_state(port_dst, "connected")
        self.notify_listeners(("connection_modified", ))
        self.graph_modified = True

        self.update_eval_listeners(src_id)
        nodeSrc = self.node(src_id)
        nodeDst = self.node(dst_id)
        src_port = nodeSrc.output_desc[port_src]
        dst_port = nodeDst.input_desc[port_dst]

        edgedata = "default", eid, src_port, dst_port
        #connected ports cannot be hidden:
        #nodeSrc.set_port_hidden(port_src, False)
        nodeDst.set_port_hidden(port_dst, False)
        self.notify_listeners(("edge_added", edgedata))

    def disconnect(self, src_id, port_src, dst_id, port_dst):
        """ Deconnect 2 elements

        :param src_id: source node id
        :param port_src: source output port number
        :param dst_id: destination node id
        :param port_dst: destination input port number
        """

        source_pid = self.out_port(src_id, port_src)
        target_pid = self.in_port(dst_id, port_dst)

        for eid in self.connected_edges(source_pid):

            if self.target_port(eid) == target_pid:
                self.notify_listeners(("edge_removed", ("default",eid)))
                self.remove_edge(eid)
                self.actor(dst_id).set_input_state(port_dst, "disconnected")
                self.notify_listeners(("connection_modified", ))
                self.graph_modified = True

                self.update_eval_listeners(src_id)
                return

        raise InvalidEdge("Edge not found")

    def replace_node(self, vid, newnode):
        """ Replace the node vid by newnode """

        oldnode = self.actor(vid)
        caption = newnode.caption
        newnode._init_internal_data(oldnode.internal_data)
        # newnode.internal_data.update(oldnode.internal_data)
        newnode.caption = caption

        if(oldnode.get_nb_input() != newnode.get_nb_input() or
            oldnode.get_nb_output() != newnode.get_nb_output()):
            raise IncompatibleNodeError()

        self.set_actor(vid, newnode)

    # Continuous eval functions

    def set_continuous_eval(self, vid, state=True):
        """ set vid as a continuous evaluated node """

        node = self.actor(vid)

        if(not node.user_application and not state):
            return

        # Remove previous listener
        if(node.user_application and hasattr(node, 'continuous_listener')):
            listener = node.continuous_listener
            node.continuous_listener = None
            if listener:
                del listener

        node.user_application = state

        if(state):
            listener = ContinuousEvalListener(self, vid)
            node.continuous_listener = listener

            # Add node as observed in all parent node
            for v in self.get_all_parent_nodes(vid):
                n = self.actor(v)
                n.continuous_eval.register_listener(listener)

    def update_eval_listeners(self, vid):
        """ Update continuous evaluation listener for node vid """

        src_node = self.node(vid)
        src_node.continuous_eval.listeners.clear()

        # For each output
        for pid in self.out_ports(vid):

            # For each connected node
            for npid in self.connected_ports(pid):
                dst_id = self.vertex(npid)

                dst_node = self.node(dst_id)
                listeners = dst_node.continuous_eval.listeners
                src_node.continuous_eval.listeners.update(listeners)

from openalea.core.observer import AbstractListener


class ContinuousEvalListener(AbstractListener):
    """ When notified this listener reexecute a dataflow on a particular vid)
    """

    def __init__(self, dataflow, vid):
        """ dataflow, vid : dataflow.eval_as_expression(vid)"""
        AbstractListener.__init__(self)
        self.dataflow = dataflow
        self.vid = vid

    def notify(self, sender, event):
        """ Notification """
        self.dataflow.eval_as_expression(self.vid)


class CompositeNodeInput(Node):
    """Dummy node to represent the composite node inputs"""

    def __init__(self, inputs):
        """
        inputs : list of dict(name='', interface='', value'',...)
        """

        Node.__init__(self, outputs=inputs)
        self.internal_data['caption'] = "In"

    def set_input(self, input_pid, val=None, *args):
        """ Define input value """
        index = self.map_index_out[input_pid]
        self.outputs[index] = val

    def get_input(self, input_pid):
        """ Return the input value """
        index = self.map_index_out[input_pid]
        return self.outputs[index]

    def eval(self):
        return False

    def to_script (self):
        return ""


class CompositeNodeOutput(Node):
    """Dummy node to represent the composite node outputs"""

    def __init__(self, outputs):
        """
        outputs : list of dict(name='', interface='', value'',...)
        """
        Node.__init__(self, inputs=outputs)
        self.internal_data['caption'] = "Out"

    def get_output(self, output_pid):
        """ Return Output value """

        index = self.map_index_in[output_pid]
        return self.inputs[index]

    def set_output(self, output_pid, val):
        """ Define output """

        index = self.map_index_in[output_pid]
        self.inputs[index] = val

    def eval(self):
        return False

    def to_script (self):
        return ""


class PyCNFactoryWriter(object):
    """ CompositeNodeFactory python Writer """

    sgfactory_template = """

$NAME = CompositeNodeFactory(name=$PNAME,
                             description=$DESCRIPTION,
                             category=$CATEGORY,
                             doc=$DOC,
                             inputs=$INPUTS,
                             outputs=$OUTPUTS,
                             elt_factory=$ELT_FACTORY,
                             elt_connections=$ELT_CONNECTIONS,
                             elt_data=$ELT_DATA,
                             elt_value=$ELT_VALUE,
                             elt_ad_hoc=$ELT_AD_HOC,
                             lazy=$LAZY,
                             eval_algo=$EVALALGO,
                             )

"""

    def __init__(self, factory):
        self.factory = factory

    def pprint_repr(self, obj, indent=3):
        """ Pretty print repr """
        return pprint.pformat(obj, indent=indent)

    def __repr__(self):
        """ Return the python string representation """

        f = self.factory
        fstr = string.Template(self.sgfactory_template)

        name = f.get_python_name()
        name = name.replace('.', '_')
        result = fstr.safe_substitute(NAME=name,
                                      PNAME=self.pprint_repr(f.name),
                                      DESCRIPTION=self.pprint_repr(f.description),
                                      CATEGORY=self.pprint_repr(f.category),
                                      DOC=self.pprint_repr(f.doc),
                                      INPUTS=self.pprint_repr(f.inputs),
                                      OUTPUTS=self.pprint_repr(f.outputs),
                                      ELT_FACTORY=self.pprint_repr(f.elt_factory),
                                      ELT_CONNECTIONS=self.pprint_repr(f.connections),
                                      ELT_DATA=self.pprint_repr(f.elt_data),
                                      ELT_VALUE=self.pprint_repr(f.elt_value),
                                      ELT_AD_HOC=self.pprint_repr(f.elt_ad_hoc),
                                      LAZY=self.pprint_repr(f.lazy),
                                      EVALALGO=self.pprint_repr(f.eval_algo),
                                      )
        return result

import json
class JSONCNFactoryWriter(PyCNFactoryWriter):

    def __repr__(self):
        f = self.factory

        minx = min(f.elt_ad_hoc.itervalues(), key=lambda x: x["position"][0])["position"][0]
        miny = min(f.elt_ad_hoc.itervalues(), key=lambda x: x["position"][1])["position"][1]

        print minx, miny

        for elt in f.elt_ad_hoc.itervalues():
            elt["position"][0] -= minx
            elt["position"][1] -= miny

        d = dict(type="CompositeNodeFactory",
                 name=f.name,
                 description=f.description,
                 category=f.category,
                 doc=f.doc,
                 #inputs=f.inputs,
                 #outputs=f.outputs,
                 #elt_factory=f.elt_factory,
                 elt_connections=list(f.connections.itervalues()),
                 #elt_data=f.elt_data,
                 #elt_value=f.elt_value,
                 elt_ad_hoc=f.elt_ad_hoc,
                 lazy=f.lazy,
                 eval_algo=f.eval_algo,
                 )
        return json.dumps(d)
