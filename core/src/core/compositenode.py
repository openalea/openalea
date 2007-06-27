# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__doc__="""
A CompositeNode is a Node that contains other nodes connected in a directed graph.
A CompositeNodeFactory instance is a factory that build CompositeNode instances.
Different instances of the same factory can coexist and can be modified in a
dataflow. 
"""


__license__= "Cecill-C"
__revision__=" $Id$ "

import string

from node import AbstractFactory, Node
from node import RecursionError, InstantiationError
from pkgmanager import PackageManager
from dataflow import DataFlow, InvalidEdge, PortError
from algo.dataflow_copy import structural_copy
from algo.dataflow_evaluation import BrutEvaluation

###############################################################################


class CompositeNodeFactory(AbstractFactory):
    """
    The CompositeNodeFactory is able to create CompositeNode instances
    Each node has an unique id : the element id (elt_id)
    """

    def __init__ (self, *args, **kargs):
        """
        CompositeNodeFactory accept more optional parameters :
        inputs : list of dict(name = '', interface='', value='')
        outputs : list of dict(name = '', interface='', value='')
        doc : documentation
        elt_factory : map of elements with its corresponding factory
        elt_connections : map of ( dst_id , input_port ) : ( src_id, output_port )
        elt_data : Dictionnary which contains associated data
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

        # Dictionnary which contains associated data
        self.elt_data =  kargs.get("elt_data", {})

        # Documentation
        self.doc = kargs.get('doc', "")
        

    def clear (self) :

        self.elt_factory.clear()
        self.connections.clear()
        self.elt_data.clear()
        

    def get_writer(self):
        """ Return the writer class """

        return PyCNFactoryWriter(self)


    def instantiate(self, call_stack=None):
        """ Create a CompositeNode instance and allocate all elements
        This function overide default implementation of NodeFactory

        @param call_stack : the list of NodeFactory id already in recursion stack
        (in order to avoid infinite loop)
        """
        
        # Test for infinite loop
        if (not call_stack) : call_stack = []
        if (self.get_id() in call_stack):
            raise RecursionError()

        call_stack.append(self.get_id())

        new_df = CompositeNode(self.inputs, self.outputs)
        new_df.factory = self
        new_df.__doc__ = self.doc
        new_df.set_caption(self.get_id())
        
        # Instantiate the node with each factory
        for vid in self.elt_factory:
            n = self.instantiate_node(vid, call_stack)
            new_df.add_node(n, vid)

        # Create the connections
        for eid,link in self.connections.iteritems() :
            (source_vid, source_port, target_vid, target_port) = link
            # Replace id for in and out nodes
            if(source_vid == '__in__') : source_vid = new_df.id_in
            if(target_vid == '__out__') : target_vid = new_df.id_out
            new_df.connect(source_vid, source_port, target_vid, target_port)

        self.graph_modified = False

        # Set call stack to its original state
        call_stack.pop()

        return new_df


    def instantiate_node(self, vid, call_stack=None):
        """
        Partial instantiation
        instantiate only elt_id in CompositeNode
        @param call_stack : a list of parent id (to avoid infinite recursion)
        """

        (package_id, factory_id) = self.elt_factory[vid]
        pkgmanager = PackageManager()
        pkg = pkgmanager[package_id]
        factory = pkg.get_factory(factory_id)
        node = factory.instantiate(call_stack)
        node.internal_data = self.elt_data[vid].copy()
        return node

        
    def instantiate_widget(self, node=None, parent=None, edit=False):
        """
        Return the corresponding widget initialised with node
        if node is None, the node is allocated
        else a composite widget composed with the node sub widget is returned

        """
        if(edit):
            from openalea.visualea.compositenode_widget import EditGraphWidget
            return EditGraphWidget(node, parent)
            
        if(node == None):  node = self.instantiate()

        from openalea.visualea.compositenode_widget import DisplayGraphWidget
        return DisplayGraphWidget(node, parent)


################################################################################

class CompositeNode(Node, DataFlow):
    """
    The CompositeNode is a container that interconnect 
    different node instances between them in directed graph.
    """


    def __init__(self, inputs=(), outputs=()):
        """ Inputs and outputs are list of dict(name='', interface='', value='') """

        DataFlow.__init__(self)

        self.id_in = None
        self.id_out = None
        
        Node.__init__(self, inputs, outputs)
     
        # graph modification status
        self.graph_modified = False


    def set_io(self, inputs, outputs):
        """
        Define inputs and outputs
        Inputs and outputs are list of dict(name='', interface='', value='') 
        """

        #I/O ports
        if(self.id_in is None):
            self.id_in = self.add_node(CompositeNodeInput(inputs))
        if(self.id_out is None):
            self.id_out = self.add_node(CompositeNodeOutput(outputs))

        Node.set_io(self, inputs, outputs)

        self.node(self.id_in).set_io((), inputs)
        self.node(self.id_out).set_io(outputs, ())
        


    #######################################################
    #
    #		vision du composite node as a node
    #		pour bien faire il faudrait aussi reimplementer add_input et add_output
    #
    #######################################################
    def set_input (self, index_key, val=None) :
        """ Copy val into input node output ports """

        self.node(self.id_in).set_input(index_key, val)
        

    def get_output (self, index_key) :
        """ Retrieve values from output node input ports """
        return self.node(self.id_out).get_output(index_key)
    

    def eval_as_expression(self, vtx_id=None):
        """
        Evaluate a vtx_id
        if node_id is None, then all the nodes without sons are evaluated
        """

        if(vtx_id != None) : self.node(vtx_id).modified = True
        algo = BrutEvaluation(self)
        algo.eval()


    # Functions used by the node evaluator
    def eval(self):
        """
        Evaluate the graph
        Return True if the node has been calculated
        """

        self.eval_as_expression()
        
        self.modified = False
        self.notify_listeners( ("status_modified",self.modified) )
        
        return True


    def __call__(self, inputs=()):
        """
        Evaluate the graph
        Return True if the node has been calculated
        """

        self.eval_as_expression()
        return ()


    #######################################################
    #
    #		CompositeNode as a dataflow
    #
    #######################################################
    def node (self, vid) :
        return self.actor(vid)


    def to_factory(self, sgfactory, listid = None):
        """
        Update CompositeNodeFactory to fit with the graph
        listid is a list of element to export. If None, select all id
        nbin and nbout are the number of in and out. If -1, parameters
        are discarded.
        """
        
        # Clear the factory
        sgfactory.clear()
        # I / O
        sgfactory.inputs = [dict(val) for val in self.input_desc]
        sgfactory.outputs = [dict(val) for val in self.output_desc]

        if(listid is None): listid = set(self.vertices())

        # Copy Connections
        for eid in self.edges() :

            src = self.source(eid)
            tgt = self.target(eid)

            if((src not in listid) or (tgt not in listid)) : continue
            if(src == self.id_in) : src = '__in__'
            if(tgt == self.id_out) : tgt = '__out__'
            
            source_port = self.local_id(self.source_port(eid))
            target_port = self.local_id(self.target_port(eid))
            sgfactory.connections[eid] = (src, source_port, tgt, target_port)


        # Do not copy In and Out
        if(self.id_in in listid): listid.remove(self.id_in)
        if(self.id_out in listid): listid.remove(self.id_out)

        # Copy node
        for vid in listid:
            
            node = self.actor(vid)
            kdata = node.internal_data

            pkg_id = node.factory.package.get_id()
            factory_id = node.factory.get_id()

            sgfactory.elt_factory[vid] = (pkg_id, factory_id)
            sgfactory.elt_data[vid] = kdata
            

        self.graph_modified = False


    def add_node(self, node, vid = None):
        """
        Add a node in the Graph with a particular id
        if id is None, autogenrate one
        
        @param node : the node instance
        @param vtx_id : element id

        @param return the id
        """
        vid = self.add_vertex( vid )
        
        for local_pid in xrange(node.get_nb_input()) :
            self.add_in_port(vid, local_pid)
            
        for local_pid in xrange(node.get_nb_output()) :
            self.add_out_port(vid, local_pid)
            
        self.set_actor(vid, node)
        #self.id_cpt += 1
        self.notify_listeners(("graph_modified",))
        self.graph_modified = True

        return vid
    

    def remove_node(self, vtx_id):
        """
        remove a node from the graph
        @param vtx_id : element id
        """

        if(vtx_id == self.id_in or vtx_id == self.id_out): return
        self.remove_vertex(vtx_id)

        self.notify_listeners(("graph_modified",))
        self.graph_modified = True
               

    def connect(self, src_id, port_src, dst_id, port_dst):
        """ Connect 2 elements :
        @param src_id : source node id
        @param port_src : source output port number
        @param dst_id : destination node id
        @param port_dst : destination input port number
        """
        
        source_pid = self.out_port(src_id, port_src)
        target_pid = self.in_port(dst_id, port_dst)
        DataFlow.connect(self, source_pid, target_pid)
        
        self.actor(dst_id).set_input_state(port_dst, "connected")
        self.notify_listeners(("connection_modified",))
        self.graph_modified = True


    def disconnect(self, src_id, port_src, dst_id, port_dst):
        """ Deconnect 2 elements :
        @param src_id : source node id
        @param port_src : source output port number
        @param dst_id : destination node id
        @param port_dst : destination input port number
        """

        source_pid = self.out_port(src_id, port_src)
        target_pid = self.in_port(dst_id, port_dst)
        for eid in self.connected_edges(source_pid) :
            if self.target_port(eid) == target_pid :
                DataFlow.disconnect(self,eid)
                self.actor(dst_id).set_input_state(port_dst, "disconnected")
                self.notify_listeners(("connection_modified",))
                self.graph_modified = True
                return
            
        raise InvalidEdge("Edge not found")



class CompositeNodeInput(Node):
    """Dummy node to represent the composite node inputs"""

    def __init__(self, inputs):
        """
        inputs : list of dict(name='', interface='', value'',...)
        """

        Node.__init__(self)
        
        for d in inputs:
            self.add_output(**d)

        self.internal_data['posx'] = 20
        self.internal_data['posy'] = 5
        self.internal_data['caption'] = "In"


    def set_input (self, input_pid, val=None) :
        """ Define input value """
        self.outputs[input_pid]=val
        

    def eval(self):
        return True



class CompositeNodeOutput(Node):
    """Dummy node to represent the composite node outputs"""

    def __init__(self, outputs):
        """
        outputs : list of dict(name='', interface='', value'',...)
        """
        Node.__init__(self)
        
        for d in outputs:
            self.add_input(**d)

        self.internal_data['posx'] = 20
        self.internal_data['posy'] = 250
        self.internal_data['caption'] = "Out"


    def get_output(self, output_pid) :
        """ Return Output value """
        return self.inputs[output_pid]
    

    def eval(self):
        return True


################################################################################

class PyCNFactoryWriter(object):
    """ CompositeNodeFactory python Writer """

    sgfactory_template = """

    nf = CompositeNodeFactory(name=$NAME, 
                              description=$DESCRIPTION, 
                              category=$CATEGORY,
                              doc=$DOC,
                              inputs=$INPUTS,
                              outputs=$OUTPUTS,
                              elt_factory=$ELT_FACTORY,
                              elt_connections=$ELT_CONNECTIONS,
                              elt_data=$ELT_DATA,
                              )

    pkg.add_factory(nf)
"""

    def __init__(self, factory):
        self.factory = factory
        

    def __repr__(self):
        """ Return the python string representation """
        f = self.factory
        fstr = string.Template(self.sgfactory_template)
        result = fstr.safe_substitute(NAME=repr(f.name),
                                      DESCRIPTION=repr(f.description),
                                      CATEGORY=repr(f.category),
                                      DOC=repr(f.doc),
                                      INPUTS=repr(f.inputs),
                                      OUTPUTS=repr(f.outputs),
                                      ELT_FACTORY=repr(f.elt_factory),
                                      ELT_CONNECTIONS=repr(f.connections),
                                      ELT_DATA=repr(f.elt_data),
                                      )
        return result





    
