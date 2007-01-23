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

        # Dictionnary which contains 2-uple (x,y) mapped by elt_id
        self.elt_position = {}

        # Dictionnary which contains the caption of each element
        self.elt_caption = {}

        # Counter for generating id
        self.id_cpt = 1

        # I/O
        self.num_input = 0
        self.num_output = 0
        self.elt_position['in'] = ( 20,5 )
        self.elt_position['out'] = ( 20,250 )
        self.elt_caption['in'] = "Inputs"
        self.elt_caption['out'] = "Outputs"

        # Documentation
        try:
            self.doc = kargs['doc']
        except:
            self.doc = ""


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

        new_df = SubGraph(self.num_input, self.num_output)
        new_df.factory = self
        new_df.__doc__ = self.doc
        
        # Instantiate the node with each factory
        for elt_id in self.elt_factory.keys():

            self.instantiate_id(elt_id, new_df)

        # Create the connections
        for (dst_id, input_port) in self.connections:

            (src_id, output_port) = self.connections[ (dst_id, input_port) ]
            
            dst_node = new_df.node_id[dst_id]
            src_node = new_df.node_id[src_id]
            new_df.connect(src_node, output_port, dst_node, input_port)

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
        subgraph.add_node(elt_id, node)



    def remove_element(self, elt_id):
        """
        Delete an element and its connection
        @param elt_id : the element id identifying the node

        """

        try:
            del(self.elt_factory[elt_id])
            del(self.elt_position[elt_id])
            del(self.elt_caption[elt_id])
        except:
            return
        
        key_list = []
        # Delete the connection
        for (dst_id, input_port) in self.connections:

            (src_id, output_port) = self.connections[ (dst_id, input_port) ]
            
            if(src_id == elt_id or dst_id == elt_id ):
                key_list.append( (dst_id, input_port) )

        for k in key_list:
            del(self.connections[k])

        self.notify_listeners()


    def add_nodefactory(self, package_id, nodefactory_id, pos = None, caption = None):
        """
        Add an element to the SubGraph
        @param package_id : the package id owning the nodefactory
        @param nodefactory_id : the nodefactory id
        @param pos : (x,y) position
        @param caption : a short description of the node purpose

        @return : the subgraph element ID ( elt_id )
        """

        id = "%s_%i"%(nodefactory_id, self.id_cpt)
        self.id_cpt += 1

        self.elt_factory[id] = (package_id, nodefactory_id)
        self.elt_position[id] = pos

        self.elt_caption[id] = caption

        self.notify_listeners()
        
        return id


    def connect(self, elt_id_src, port_src, elt_id_dst, port_dst):
        """ Connect 2 elements :
        @param elt_id_src : source element id
        @param port_src : source output port number
        @param elt_id_dst : destination element id
        @param port_dst : destination input port number
        """
        
        self.connections[ (elt_id_dst, port_dst) ] = (elt_id_src, port_src)
        self.notify_listeners()


    def disconnect(self, elt_id_src, port_src, elt_id_dst, port_dst):
        """
        Disconnect 2 elements :
        @param elt_id_src : source element id
        @param port_src : source output port number
        @param elt_id_dst : destination element id
        @param port_dst : destination input port number
        """

        try:
            del(self.connections[ (elt_id_dst, port_dst) ])
        except:
            return
        self.notify_listeners()

        
    def get_position(self, elt_id):
        """ Return the position of the element elt_id in a 2 uple (x,y)"""
        return self.elt_position[elt_id]


    def move_element(self, elt_id, position):
        """ Move an element to a new position, position is 2 uples (x,y) """

        self.elt_position[elt_id] = position
        self.notify_listeners()


    def get_caption(self, elt_id):
        """ Return the description of an element """
        return self.elt_caption[elt_id]
        

    def set_caption(self, elt_id, desc):
        """ Set the description of an element """
        self.elt_caption[elt_id] = desc
        self.notify_listeners()
        

    def set_numinput(self, v):
        self.num_input = v

        
    def set_numoutput(self, v):
        self.num_output = v


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



class SubGraph(Node):
    """
    The SubGraph is a container that interconnect different node between them
    Each node is referenced by its id which is the same id as in the subgraph factory
    """

    def __init__(self, ninput=0, noutput=0):
        """ ninput and noutput are the number of inputs and outputs """

        Node.__init__(self)

        # Node list indexed by its id
        self.node_id = {}

        # Dictionnary which contains tuples describing connection
        # ( dst_node , input_port ) : ( src_node, output_port )
        
        self.connections = {}

        # I/O
        if(ninput>0):
            self.inputs = [None]*ninput
            self.input_types = self.inputs[:]
            self.node_id['in'] = SubgraphInput(self, ninput)

        if(noutput>0) :
            self.outputs = [None]*noutput
            self.output_types = self.outputs[:]
            self.node_id['out'] = SubgraphOutput(self, noutput)


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
        
        for (src_node, outport) in self.connections.values():
            with_output.add(src_node)

        for n in self.node_id.values():
            if(not n in with_output):
                result.append(n)

        return result

    
    def eval_as_expression(self, node=None):
        """
        Evaluate a node
        if node is None, then all the nodes without sons are evaluated
        """

        # dict to keep trace of evaluated node
        self.evaluated={}

        # get all the base nodes
        if(node == None):
            l = self.get_base_nodes()

            for n in l:
                self.eval_node(n)
        else:
            self.eval_node(node)


    def eval_node(self, node):
        """
        Evaluate a particular Node
        Do not call directly this function, use instead eval_as expression

        """

        # evaluate the node inputs
        for iport in range(node.get_nb_input()):
            try:
                (node_src, port_src)=self.connections[(node, iport)]

                # test if the node has already be evaluated
                if( not self.evaluated.has_key(node_src) ):
                    self.eval_node(node_src)

                v = node_src.get_output(port_src)
                node.set_input(iport, v)
                
            except KeyError :
                #node.set_input(iport, None)
                pass
            except Exception, e:
                print e
                raise


        # evaluate the node itself
        node.eval()
        
        self.evaluated[node]=True
        

    def __call__(self, inputs=()):
        """ Main evaluation function"""

        self.eval_as_expression()

        return ()


    def add_node(self, elt_id, node):
        """
        Add a node in the SubGraph
        @param elt_id : element id
        @param node : the node instance
        """
        
        self.node_id[elt_id] = node
        return


    def remove_node(self, elt_id):
        """
        remove a node from the SubGraph
        @param elt_id : element id
        """
        
        del self.node_id[elt_id]
        return


    def remove_node_by_id(self, elt_id):
        """
        Remove a node identified by elt_id
        """

        node = self.node_id[elt_id]
        del(self.node_id[elt_id])

        for ((node_dst, port_dst), (node_src, port_src)) in self.connections.items():
            if(node_dst == node or node_src == node):
                del(self.connections[(node_dst, port_dst)])
                


    def connect(self, node_src, port_src, node_dst, port_dst):
        """ Connect 2 elements :
        @param node_src : source node 
        @param port_src : source output port number
        @param node_dst : destination node
        @param port_dst : destination input port number
        """

        self.connections[ (node_dst, port_dst) ] = (node_src, port_src)

        node_dst.set_input_state(port_dst, "connected")

    
    def connect_by_id(self, src_id, port_src, dst_id, port_dst):
        """ Connect 2 elements :
        @param src_id : source node id
        @param port_src : source output port number
        @param dst_id : destination node id
        @param port_dst : destination input port number
        """
        
        node_dst = self.node_id[dst_id]
        node_src = self.node_id[src_id]
        self.connections[ (node_dst, port_dst) ] = (node_src, port_src)

        node_dst.set_input_state(port_dst, "connected")



    def disconnect(self, node_src, port_src, node_dst, port_dst):
        """ Disconnect 2 elements :
        @param node_src : source node
        @param port_src : source output port number
        @param node_dst : destination node
        @param port_dst : destination input port number
        """

        try:
            del(self.connections[ (elt_id_dst, port_dst) ])
        except:
            return

        node_dst.set_input_state(port_dst, "disconnected")

        

    def disconnect_by_id(self, src_id, port_src, dst_id, port_dst):
        """ Deconnect 2 elements :
        @param src_id : source node id
        @param port_src : source output port number
        @param dst_id : destination node id
        @param port_dst : destination input port number
        """

        try:
            node_dst = self.node_id[dst_id]
            node_src = self.node_id[src_id]
            del(self.connections[ (node_dst, port_dst) ])
        except:
            return

        node_dst.set_input_state(port_dst, "disconnected")




class SubgraphInput(Node):
    """
    Define a dummy node to represent subgraph input
    """

    def __init__(self, subgraph, size):
        """
        Subgraph is the owner of the object
        Size is the number of port
        """

        Node.__init__(self)
        self.subgraph = subgraph
        self.outputs = [None]*size

    def get_output(self, index):
        """ Redirect call """

        return self.subgraph.get_input(index)
        
    def __call__(self, inputs=()):
        return ()


class SubgraphOutput(Node):
    """
    Define a dummy node to represent subgraph output
    """

    def __init__(self, subgraph, size):
        """
        Subgraph is the owner of the object
        Size is the number of port
        """
        Node.__init__(self)
        self.subgraph = subgraph
        self.inputs = [None]*size


    def set_input(self, index, val):
        """ Redirect call """
        self.subgraph.set_output(index, val)

        
    def __call__(self, inputs=()):
        return ()

    
