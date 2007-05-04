# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
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


class CompositeNodeFactory(AbstractFactory, DataFlow):
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
        DataFlow.__init__(self)
        # A CompositeNode is composed by a set of element indexed by an elt_id
        # Each element is associated to NodeFactory
        # Each element will generate an node instance in the real CompositeNode

        # Dict mapping elt_id with its corresponding factory
        # the factory is identified by its unique id (package_id, factory_id)
        elt_factory = kargs.get("elt_factory", {})

        # Dictionnary which contains tuples describing connection
        # ( dst_id , input_port ) : ( src_id, output_port )
        connections = kargs.get("elt_connections", {})

        # Dictionnary which contains associated data
        elt_data =  kargs.get("elt_data", {})

        # I/O
        self.id_in=None
        self.id_out=None
        self.initialise_connector_nodes()
        #construction par recopie
        #a abandonner au profit d'une methode
        for vid,factory_info in elt_factory.iteritems() :
            ins,outs,factory=factory_info
            data=elt_data.get(vid,{})
            dum=self.add_vertex(vid)
            for local_pid in ins :
                self.add_in_port(vid,local_pid)
            for local_pid in outs :
                self.add_out_port(vid,local_pid)
            self.set_actor(vid,(factory[0],factory[1],data))
        for ( dst_id, dst_port ), ( src_id, src_port ) in connections.iteritems():
            #creation des ports si necessaire
            spid=self.out_port(src_id,src_port)
            tpid=self.in_port(dst_id,dst_port)
            self.connect(spid,tpid)

        # Documentation
        self.doc = kargs.get('doc', "")


    def initialise_connector_nodes (self, vid_in=None, vid_out=None) :
        if self.id_in is not None :
            self.remove_vertex(self.id_in)
        self.id_in=self.add_vertex(vid_in)
        for local_pid in xrange(len(self.inputs)) :
            self.add_out_port(self.id_in,local_pid)
        
        if self.id_out is not None :
            self.remove_vertex(self.id_out)
        self.id_out=self.add_vertex(vid_out)
        for local_pid in xrange(len(self.outputs)) :
            self.add_in_port(self.id_out,local_pid)

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
        if ( self.get_id() in call_stack ):
            raise RecursionError()

        call_stack.append(self.get_id())
        new_df = CompositeNode(self.inputs, self.outputs,self.id_in,self.id_out)
        new_df.factory = self
        new_df.__doc__ = self.doc
        new_df.set_caption(self.get_id())
        
        # Instantiate the node with each factory
        for vid in (vid for vid in self.vertices() if vid not in [self.id_in,self.id_out]):
            new_df.add_node(self.instantiate_node(vid,call_stack),vid)

        # Create the connections
        for eid in self.edges() :
            DataFlow.connect(new_df,self.source_port(eid),self.target_port(eid))

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

        package_id,factory_id,data=self.actor(vid)
        pkgmanager = PackageManager()
        pkg = pkgmanager[package_id]
        factory = pkg.get_factory(factory_id)
        node = factory.instantiate(call_stack)
        node.internal_data = data.copy()
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

    ##################################################
    #
    #		backward compatibility
    #
    ##################################################
    def elt_factory (self) :
        ret={}
        for vid in (vid for vid in self.vertices() if vid not in (self.id_in,self.id_out)) :
            ins=tuple(self.port(pid).local_pid for pid in self.in_ports(vid))
            outs=tuple(self.port(pid).local_pid for pid in self.out_ports(vid))
            factory=(self.actor(vid)[0],self.actor(vid)[1])
            ret[vid]=(ins,outs,factory)
        return ret

    def elt_data (self) :
        return dict( (vid,self.actor(vid)[2]) for vid in self.vertices() \
                                                     if vid not in (self.id_in,self.id_out) )

    def connections( self ):
        connect= {}
        for eid in self.edges() :
            connect[(self.target( eid ), self.port(self.target_port(eid)).local_pid )] \
                          =( self.source( eid ), self.port(self.source_port(eid)).local_pid )
        return connect

        


################################################################################

class CompositeNode(Node, DataFlow):
    """
    The CompositeNode is a container that interconnect 
    different node instances between them in directed graph.
    """


    def __init__(self, inputs=(), outputs=(), id_in=None, id_out=None):
        """ inputs and outputs are list of dict(name='', interface='', value='') """

        Node.__init__(self, inputs, outputs)
        DataFlow.__init__(self)

        # graph modification status
        self.graph_modified = False

        #I/O ports
        self.id_in= self.add_node(CompositeNodeInput(inputs),id_in)
        self.id_out= self.add_node(CompositeNodeOutput(outputs),id_out)
    #######################################################
    #
    #		vision du composite node as a node
    #		pour bien faire il faudrait aussi reimplementer add_input et add_output
    #
    #######################################################
    def set_input (self, index_key, val=None, value_list=None) :
        """
        copy val into input node output ports
        """
        self.node(self.id_in).set_input(index_key,val,value_list)

    def get_output (self, index_key) :
        """
        retrieve values from output node input ports
        """
        return self.node(self.id_out).get_output(index_key)

    def eval_as_expression(self, vtx_id=None):
        """
        Evaluate a vtx_id
        if node_id is None, then all the nodes without sons are evaluated
        """

        # dict to keep trace of evaluated node
        algo=BrutEvaluation(self)
        algo.eval()

    # Functions used by the node evaluator
    def eval(self):
        """
        Evaluate the graph
        Return True if the node has been calculated
        """

        self.eval_as_expression()
        return True


    def __call__(self, inputs=()):
        """
        Evaluate the graph
        """

        self.eval_as_expression()
        return ()

    #######################################################
    #
    #		vision du composite node as a dataflow
    #
    #######################################################
    def node (self, vid) :
        return self.actor(vid)

    def to_factory(self, sgfactory):
        """
        Update CompositeNodeFactory to fit with the graph
        listid is a list of element to export. If None, select all id
        nbin and nbout are the number of in and out. If -1, parameters
        are discarded.
        """
        # Clear the graph factory
        sgfactory.clear()
        sgfactory.inputs = [dict(val) for val in self.input_desc]
        sgfactory.outputs = [dict(val) for val in self.output_desc]
        sgfactory.id_in=self.id_in
        sgfactory.id_out=self.id_out
        structural_copy(self,sgfactory)
        for vid in (vid for vid in self.vertices() if vid not in [self.id_in,self.id_out]):
            node = self.actor(vid)
            kdata = node.internal_data
            pkg_id = node.factory.package.get_id()
            factory_id = node.factory.get_id()
            sgfactory.set_actor(vid, (pkg_id,factory_id,kdata) )

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
            self.add_in_port(vid,local_pid)
        for local_pid in xrange(node.get_nb_output()) :
            self.add_out_port(vid,local_pid)
        self.set_actor(vid,node)
        #self.id_cpt += 1
        self.notify_listeners(("graph_modified",))
        self.graph_modified = True

        return vid        

    def remove_node(self, vtx_id):
        """
        remove a node from the graph
        @param vtx_id : element id
        """
        
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
        source_pid=self.out_port(src_id,port_src)
        target_pid=self.in_port(dst_id,port_dst)
        DataFlow.connect(self,source_pid,target_pid)
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

        source_pid=self.out_port(src_id,port_src)
        target_pid=self.in_port(dst_id,port_dst)
        for eid in self.connected_edges(source_pid) :
            if self.target_port(eid)==target_pid :
                DataFlow.disconnect(self,eid)
                self.actor(dst_id).set_input_state(port_dst, "disconnected")
                self.notify_listeners(("connection_modified",))
                self.graph_modified = True
                return
        raise InvalidEdge("edge not found")


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

    def set_input (self, input_pid, val=None, value_list=None) :
        if val is None :
            if len(value_list)>1 :
                raise NotImplementedError
            val=value_list[0]
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

    def get_output (self, output_pid) :
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
                                      ELT_FACTORY=repr(f.elt_factory()),
                                      ELT_CONNECTIONS=repr(f.connections()),
                                      ELT_DATA=repr(f.elt_data()),
                                      )
        return result





    
