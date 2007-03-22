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
This module defines the subgraph classes 
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


from copy import copy

from core import NodeFactory, Node
from core import RecursionError, InstantiationError

###############################################################################

class SubGraphFactory(NodeFactory):
    """
    The SubGraphFactory is able to create Subgraph instances
    Each node has an unique id : the element id (elt_id)
    """
    
    def __init__ (self, pkgmanager,  *args, **kargs):

        # Init parent (name, description, category, doc, node, widget=None)
        NodeFactory.__init__(self, *args, **kargs)


        # The Package Manager is needed to allocate nodefactory
        self.pkgmanager = pkgmanager

        # A SubGraph is composed by a set of element indexed by an elt_id
        # Each element is associated to NodeFactory
        # Each element will generate an node instance in the real SubGraph

        # Dict mapping elt_id with its corresponding factory
        # the factory is identified by its unique id (package_id, factory_id)
        self.elt_factory = {}

        # Dictionnary which contains tuples describing connection
        # ( dst_id , input_port ) : ( src_id, output_port )
        self.connections = {}

        # Dictionnary which contains dictionnary2-uple (x,y) mapped by elt_id
        self.elt_data = {}

        # I/O
        self.nb_input = 0
        self.nb_output = 0

        # Documentation
        try:
            self.doc = kargs['doc']
        except:
            self.doc = ""


    def add_nodefactory(self, elt_id, (pkg_id, factory_id), kdata = {}):
        """
        Add a node description to the factory
        @param elt_id : element id
        @param pkg_id, factory_id : factory description
        @param kdata : data dictionnary
        """

        self.elt_factory[elt_id] = (pkg_id, factory_id)
        self.elt_data[elt_id] = kdata

        return elt_id


    def add_connection(self, src_id, port_src, dst_id, port_dst):
        """ Connect 2 elements :
        @param src_id : source node id
        @param port_src : source output port number
        @param dst_id : destination node id
        @param port_dst : destination input port number
        """

        self.connections[(dst_id, port_dst)] = (src_id, port_src)


    def get_xmlwriter(self):
        """ Return an instance of a xml writer """

        from pkgreader import SubGraphFactoryXmlWriter
        return SubGraphFactoryXmlWriter(self)


    def instantiate(self, call_stack=None):
        """ Create a SubGraph instance and allocate all elements
        This function overide default implementation of NodeFactory

        @param call_stack : the list of NodeFactory id already in recursion stack
        (in order to avoid infinite loop)
        """
        
        # Test for infinite loop
        if (not call_stack) : call_stack = []
        if ( self.get_id() in call_stack ):
            raise RecursionError()

        call_stack.append(self.get_id())

        new_df = SubGraph(self.nb_input, self.nb_output)
        new_df.factory = self
        new_df.__doc__ = self.doc
        
        # Instantiate the node with each factory
        for elt_id in self.elt_factory.keys():
            self.instantiate_id(elt_id, new_df, call_stack)

        # Create the connections
        for (( dst_id , iport), ( src_id, oport )) in self.connections.items():
            #new_df.connections = self.connections.copy()
            new_df.connect(src_id, oport, dst_id, iport)

        self.graph_modified = False

        # Set call stack to its original state
        call_stack.pop()
        
        return new_df


    def instantiate_id(self, elt_id, subgraph, call_stack=None):
        """
        Partial instantiation
        instantiate only elt_id in subgraph
        @param call_stack : a list of parent id (to avoid infinite recursion)
        """

        if(subgraph.node_id.has_key(elt_id)) :
            return

        (package_id, factory_id) = self.elt_factory[elt_id]
        
        pkg = self.pkgmanager[package_id]
        factory = pkg.get_factory(factory_id)

        node = factory.instantiate(call_stack)
        node.internal_data = self.elt_data[elt_id].copy()
        subgraph.add_node(node, elt_id)

        
    def set_nb_input(self, v):
        self.nb_input = v

        
    def set_nb_output(self, v):
        self.nb_output = v


    def instantiate_widget(self, node, parent, edit = False):
        """
        Return the corresponding widget initialised with node
        if node is None, the node is allocated
        if edit is True, return an  EditSubgraphWidget 
        else a composite widget composed with the node sub widget is returned

        """

        if(node == None):
                node = self.instantiate()
        try:
            if(edit):
                from openalea.visualea.subgraph_widget import EditSubGraphWidget
                return EditSubGraphWidget(node, parent)
            
            else:
                from openalea.visualea.subgraph_widget import DisplaySubGraphWidget
                return DisplaySubGraphWidget(node, parent)
            
        except ImportError:
            raise InstantiationError()



################################################################################

class SubGraph(Node):
    """ The SubGraph is a container that interconnect \
    different node instances between them. """

    def __init__(self, ninput=0, noutput=0):
        """ ninput and noutput are the number of inputs and outputs """

        Node.__init__(self)

        # Node list indexed by its id
        self.node_id = {}

        # Dictionnary which contains tuples describing connection
        # ( dst_id , input_port ) : ( src_id, output_port )
        self.connections = {}

        # Counter for generating id
        self.id_cpt = 1

        # subgraph modification status
        self.graph_modified = False

        # I/O
        if(ninput>0):
            self.node_id['in'] = SubgraphInput(self, ninput)
            for i in range(ninput):
                self.add_input( "in%i"%(i,), interface = None, value = None)

        if(noutput>0) :
            self.node_id['out'] = SubgraphOutput(self, noutput)
            for i in range(noutput):
                self.add_output( "out%i"%(i,), interface = None)


    def to_factory(self, sgfactory):
        """
        Update subgraph factory to fit with the subgraph
        """

        sgfactory.elt_factory = {}
        sgfactory.elt_data = {}

        sgfactory.set_nb_input( self.get_nb_input())
        sgfactory.set_nb_output( self.get_nb_output())
            
        
        # Create node if necessary
        for nid in self.node_id.keys():
            if(nid == 'in' or nid == 'out') : continue
            
            node = self.node_id[nid]
            kdata = node.internal_data
            pkg_id = node.factory.package.get_id()
            factory_id = node.factory.get_id()

            sgfactory.add_nodefactory(nid, (pkg_id, factory_id), kdata)


        # Create connections
        sgfactory.connections = self.connections

        self.graph_modified = False
            

    def get_ids(self):
        """ Return the list of element id """
        return self.node_id.keys()


    def get_nodes(self):
        """ Return the list of the subnodes """
        return self.node_id.values()


    def get_node_by_id(self, id):
        """ Return the node instance with its id """

        return self.node_id[id]


    def get_base_nodes(self):
        """ Return all the nodes without connected output """

        with_output = set()
        result = []
        
        for (src_id, outport) in self.connections.values():
            with_output.add(src_id)

        for nid in self.node_id.keys():
            if(not nid in with_output):
                result.append(nid)

        return result

    
    def eval_as_expression(self, node_id=None):
        """
        Evaluate a node_id
        if node_id is None, then all the nodes without sons are evaluated
        """

        # dict to keep trace of evaluated node
        self.evaluated = set()

        # get all the base nodes
        if(node_id == None):
            l = self.get_base_nodes()

            for nid in l:
                self.eval_node(nid)
        else:
            self.eval_node(node_id)


    def eval_node(self, elt_id):
        """
        Evaluate a particular Node identified by elt_id
        Do not call directly this function, use instead eval_as expression
        Return True if the node has been executed
        """

        try:
            node = self.node_id[elt_id]
        except:
            raise

        # evaluate the node inputs
        for iport in range(node.get_nb_input()):
            try:
                (id_src, port_src)=self.connections[(elt_id, iport)]

                # test if the node has already be evaluated
                if(not id_src in  self.evaluated):
                    # Recursive evaluation
                    self.evaluated.add(id_src)
                    self.eval_node(id_src)

                # copy the data
                node_src = self.node_id[id_src]
                
                v = node_src.get_output(port_src)
                node.set_input(iport, copy(v))
                
            except KeyError :
                pass
            except Exception, e:
                print e
                raise

        # evaluate the node itself
        return node.eval()
        
                
    # Functions used by the node evaluator
    def eval(self):
        """
        Evaluate the subgraph
        Return True if the node has been calculated
        """

        self.eval_as_expression()
        return True


    def __call__(self, inputs=()):
        """
        Evaluate the subgraph
        """

        self.eval_as_expression()
        return ()


    def add_node(self, node, elt_id = None):
        """
        Add a node in the SubGraph with a particular id
        if id is None, autogenrate one
        
        @param node : the node instance
        @param elt_id : element id

        @param return the id
        """

        if(not elt_id):
            elt_id = "%s_%i"%(node.factory.get_id(), self.id_cpt)

        self.node_id[elt_id] = node
        
        self.id_cpt += 1
        self.notify_listeners(("subgraph_modified",))
        self.graph_modified = True

        return elt_id        


    def remove_node(self, elt_id):
        """
        remove a node from the SubGraph
        @param elt_id : element id
        """
        
        del self.node_id[elt_id]

        for ((id_dst, port_dst), (id_src, port_src)) in self.connections.items():
            if(id_dst == elt_id or id_src == id):
                del(self.connections[(id_dst, port_dst)])

        self.notify_listeners(("subgraph_modified",))
        self.graph_modified = True

               

    def connect(self, src_id, port_src, dst_id, port_dst):
        """ Connect 2 elements :
        @param src_id : source node id
        @param port_src : source output port number
        @param dst_id : destination node id
        @param port_dst : destination input port number
        """

        if(self.node_id.has_key(src_id) and
           self.node_id.has_key(dst_id)):
            
            self.connections[(dst_id, port_dst)] = (src_id, port_src)

            node_dst = self.node_id[dst_id]
            node_dst.set_input_state(port_dst, "connected")
            self.notify_listeners(("connection_modified",))
            self.graph_modified = True


    def disconnect(self, src_id, port_src, dst_id, port_dst):
        """ Deconnect 2 elements :
        @param src_id : source node id
        @param port_src : source output port number
        @param dst_id : destination node id
        @param port_dst : destination input port number
        """

        try:
            del(self.connections[ (dst_id, port_dst) ])
        except:
            return

        node_dst = self.node_id[dst_id]
        node_dst.set_input_state(port_dst, "disconnected")
        self.notify_listeners(("connection_modified",))
        self.graph_modified = True



class SubgraphInput(Node):
    """Dummy node to represent subgraph inputs"""

    def __init__(self, subgraph, size):
        """
        Subgraph is the owner of the object
        Size is the number of port
        """

        Node.__init__(self)
        self.subgraph = subgraph
        for i in range(size):
            self.add_output("out%i"%(i,), interface = None)

        self.internal_data['posx'] = 20
        self.internal_data['posy'] = 5


    def get_output(self, index):
        """ Redirect call """

        return self.subgraph.get_input(index)
        

    def eval(self):
        return True



class SubgraphOutput(Node):
    """Dummy node to represent subgraph outputs"""

    def __init__(self, subgraph, size):
        """
        Subgraph is the owner of the object
        Size is the number of port
        """
        Node.__init__(self)
        self.subgraph = subgraph
        
        for i in range(size):
            self.add_input("in%i"%(i,), interface = None, value = None)

        self.internal_data['posx'] = 20
        self.internal_data['posy'] = 250
        

    def set_input(self, index, val):
        """ Redirect call """

        self.subgraph.set_output(index, val)

        
    def eval(self):
        #the node must be always calculated
        return True

    
