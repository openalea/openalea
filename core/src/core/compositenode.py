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
from openalea.graph import Graph

###############################################################################
class DirectedGraphProperty(Graph):
    """ Directed graph with properties on edges and vertices """

    def __init__(self, graph=None):
        Graph.__init__( self, graph )


class DataFlow( DirectedGraphProperty ):
    """
    A DataFlow is a directed graph with properties on edges and vertices.
    Vertex properties contain nodes or node factories.
    Edge properties contain connections on ports between two nodes or node factories.
    Add the notion of ports to the edges of a Directgraph
    It is useful to exports graph mangement methods from node classes
    """

    def __init__( self, graph=None ):
        DirectedGraphProperty.__init__( self, graph )


class CompositeNodeFactory(AbstractFactory, DataFlow):
    """
    The CompositeNodeFactory is able to create CompositeNode instances
    Each node has an unique id : the element id (elt_id)
    """

    def __init__ (self, pkgmanager,  *args, **kargs):
        """
        CompositeNodeFactory accept more optional parameters :
        nin : number of inputs
        nout : number of outputs
        doc : documentation
        elt_factory : map of elements with its corresponding factory
        elt_connections : map of ( dst_id , input_port ) : ( src_id, output_port )
        elt_data : Dictionnary which contains associated data
        """

        # Init parent (name, description, category, doc, node, widget=None)
        AbstractFactory.__init__(self, *args, **kargs)
        DataFlow.__init__(self)

        # The Package Manager is needed to allocate nodefactory
        self.pkgmanager = pkgmanager

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

        # mapping between edge_id and ( input_port, output_port )
        # accessor through source_port & target_port
        self._edge_ports= {}

        # mapping between vertex_name and vertex_id
        # temp hack
        #self._vid2name= {}
        #self._name2vid= {}


        # I/O
        self.nb_input = kargs.get("nbin", 0)
        self.nb_output = kargs.get("nbout", 0)

        self.id_in= self.add_vertex()
        self.id_out= self.add_vertex()

        # Documentation
        self.doc = kargs.get('doc', "")

        name2vid= {self.id_in:self.id_in, self.id_out:self.id_out}
        self.elt_factory= {}
        self.elt_data= {}

        for ( dst_id, dst_port ), ( src_id, src_port ) in connections.iteritems():
            # Create 2 vertices if they do not exist
            
            
            # src_vid= name2vid.setdefault( src_id, self.add_vertex() )
            # dst_vid= name2vid.setdefault( dst_id, self.add_vertex() )
            # this code is not used because self.add_vertex() is evaluted even
            # if name2vid[ id  ] is defined 
            if src_id in name2vid:
                src_vid= name2vid[ src_id ]
            else: 
                src_vid= self.add_vertex()
                name2vid[ src_id ]= src_vid
            if dst_id in name2vid:
                dst_vid= name2vid[ dst_id ]
            else: 
                dst_vid= self.add_vertex()
                name2vid[ dst_id ]= dst_vid

            
            self.elt_factory.setdefault( src_vid, elt_factory[src_id] )
            self.elt_factory.setdefault( dst_vid, elt_factory[dst_id] )
            self.elt_data.setdefault( src_vid, elt_data[src_id] )
            self.elt_data.setdefault( dst_vid, elt_data[dst_id] )

            eid= self.add_edge( edge= ( src_vid, dst_vid ) )
            self._edge_ports[ eid ]= ( src_port, dst_port )


    def add_nodefactory(self, (pkg_id, factory_id), kdata = {}):
        """
        Add a node description to the factory
        @param elt_id : element id
        @param pkg_id, factory_id : factory description
        @param kdata : data dictionnary
        """
        vid= self.add_vertex()
        self.elt_factory[vid] = (pkg_id, factory_id)
        self.elt_data[vid] = kdata

        return vid


    def add_connection(self, src_id, port_src, dst_id, port_dst):
        """ Connect 2 elements :
        @param src_id : source node id
        @param port_src : source output port number
        @param dst_id : destination node id
        @param port_dst : destination input port number
        """

        # src_vid= self._name2vid.setdefault( src_id, self.add_vertex() )
        # dst_vid= self._name2vid.setdefault( dst_id, self.add_vertex() )
        # self._vid2name[ src_vid ]=src_id
        # self._vid2name[ dst_vid ]=dst_id

        eid= self.add_edge( edge= ( src_id, dst_id ) )
        self._edge_ports[ eid ]= ( port_src, port_dst )
        #self.connections[(dst_id, port_dst)] = (src_id, port_src)


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

        new_df = CompositeNode(self.nb_input, self.nb_output)
        new_df.factory = self
        new_df.__doc__ = self.doc
        new_df.set_caption(self.get_id())
        
        # Instantiate the node with each factory
        fid2id= {}
        fid2id[ self.id_in ] = new_df.id_in
        fid2id[ self.id_out ] = new_df.id_out

        for vid in self.elt_factory:
            fid2id[ vid ]= self.instantiate_id(vid, new_df, call_stack)

        # Create the connections
        for eid in self.edges():
            src_port, dst_port= self._edge_ports[ eid ]
            src_id= fid2id[ self.source( eid ) ]
            dst_id= fid2id[ self.target( eid ) ]
            new_df.connect(src_id, src_port, dst_id, dst_port)
        
        #for (( dst_id , iport), ( src_id, oport )) in self.connections.items():
        #    new_df.connect(src_id, oport, dst_id, iport)

        self.graph_modified = False

        # Set call stack to its original state
        call_stack.pop()

        new_df._factory_id_mapping( fid2id )
        return new_df


    def instantiate_id(self, elt_id, composite_node, call_stack=None):
        """
        Partial instantiation
        instantiate only elt_id in CompositeNode
        @param call_stack : a list of parent id (to avoid infinite recursion)
        """

        (package_id, factory_id) = self.elt_factory[elt_id]
        
        pkg = self.pkgmanager[package_id]
        factory = pkg.get_factory(factory_id)
        node = factory.instantiate(call_stack)
        node.internal_data = self.elt_data[elt_id].copy()
        return composite_node.add_node(node)

        
    def set_nb_input(self, v):
        self.nb_input = v

        
    def set_nb_output(self, v):
        self.nb_output = v


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

    def connections( self ):
        connect= {}
        for eid, ( src_port, dst_port ) in self._edge_ports.iteritems():
            connect[(self.target( eid ), dst_port )]=( self.source( eid ), src_port )
        return connect


################################################################################

class CompositeNode(Node, DataFlow):
    """
    The CompositeNode is a container that interconnect 
    different node instances between them in directed graph.
    """


    def __init__(self, ninput=0, noutput=0):
        """ ninput and noutput are the number of inputs and outputs """

        Node.__init__(self)
        DataFlow.__init__(self)

        # Node list indexed by its id
        self.node_id = {}

        # Dictionnary which contains tuples describing connection
        # ( dst_id , input_port ) : ( src_id, output_port )
        self.connections = {}
        self._edge_ports= {}

        # Counter for generating id
        #self.id_cpt = 1

        # graph modification status
        self.graph_modified = False

        self.id_in= self.add_vertex()
        self.id_out= self.add_vertex()

        # I/O
        self.node_id[self.id_in] = CompositeNodeInput(self, ninput)
        if(ninput>0):
            for i in range(ninput):
                self.add_input( "in%i"%(i,), interface = None, value = None)

        self.node_id[self.id_out] = CompositeNodeOutput(self, noutput)
        if(noutput>0) :
            for i in range(noutput):
                self.add_output( "out%i"%(i,), interface = None)

        # contains the mapping between the factory ids and the
        # current ids.
        self._factory_id_to_id= {}

    def _factory_id_mapping( self, mapping ):
        """
        Protected function used to set the mapping between 
        the factory and the instance self
        """
        self._factory_id_to_id= mapping

    def to_factory(self, sgfactory, listid=None, nbin=-1, nbout=-1):
        """
        Update CompositeNodeFactory to fit with the graph
        listid is a list of element to export. If None, select all id
        nbin and nbout are the number of in and out. If -1, parameters
        are discarded.
        """

#        sgfactory.elt_factory = {}
#        sgfactory.elt_data = {}

        if(nbin<0) : nbin = self.get_nb_input()
        if(nbout<0) : nbout = self.get_nb_output()

        # TODO : compositeNode should not access directly to CompositeNodeFactory members
        # this should be refactored
        sgfactory.set_nb_input(nbin)
        sgfactory.set_nb_output(nbout)

        
        # Create node if necessary
        sgvid= {} # mapping between vid and sgvid used to rebuild edges
        for vid in self.vertices():
            if(vid == self.id_in or vid == self.id_out) : 
                continue
            if(listid != None and (not vid in listid)): 
                continue
            
            node = self.node_id[vid]
            kdata = node.internal_data
            pkg_id = node.factory.package.get_id()
            factory_id = node.factory.get_id()

            sgvid[ vid ] = sgfactory.add_nodefactory((pkg_id, factory_id), kdata)
            

        # Create connections
        edges= set() # filtering vid that should not be included in factory
        for vid in sgvid :
            def valid_edge( eid ):
                return self.source( eid ) in sgvid and self.target( eid ) in sgvid
            edges.update( filter(  valid_edge, self.edges(vid) ) )

        # rebuilding edges with the good edges 
        for eid in edges:
            src_sgvid= sgvid[ self.source( eid ) ]
            dst_sgvid= sgvid[ self.target( eid ) ]
            src_port, dst_port= self._edge_ports[ eid ]
            sgeid= sgfactory.add_connection( src_sgvid, src_port, dst_sgvid, dst_port )

        self.graph_modified = False


    def get_ids(self):
        """ Return the list of element id """
        #TODO: deprecated
        vids= set( self.vertices() )
        if self.factory.nb_input == 0: 
            vids.remove( self.id_in )
        if self.factory.nb_output == 0:
            vids.remove( self.id_out )
        return vids


    def get_nodes(self):
        """ Return the list of the subnodes """
        return self.node_id.values()


    def get_node_by_id(self, id):
        """ Return the node instance with its id """

        return self.node_id[id]


    def get_base_nodes(self):
        """ Return all the node ids without connected output """

        return filter( lambda x: self.nb_out_edges( x )==0, self.vertices() )

    
    def eval_as_expression(self, vtx_id=None):
        """
        Evaluate a vtx_id
        if node_id is None, then all the nodes without sons are evaluated
        """

        # dict to keep trace of evaluated node
        self.evaluated = set()

        # get all the base nodes
        if(vtx_id == None):
            for node in self.node_id.values():
                node.modified= True

            outputs = self.get_base_nodes()

            for vid in outputs:
                self.eval_node(vid)
        else:
            self.node_id[ vtx_id ].modified= True
            self.eval_node(vtx_id)


    def eval_node(self, vtx_id):
        """
        Evaluate a particular Node identified by vtx_id
        Do not call directly this function, use instead eval_as expression
        Return True if the node has been executed
        """
        assert vtx_id in self

        node = self.node_id[vtx_id]

        # evaluate the node inputs
        for in_eid in self.in_edges( vtx_id ):
            port_src, port_dst= self._edge_ports[ in_eid ]
            vid_src= self.source( in_eid )

            if vid_src not in self.evaluated:
                self.eval_node(vid_src)
                self.evaluated.add( vid_src )
            
            node_src = self.node_id[vid_src]
            v = node_src.get_output(port_src)
            node.set_input(port_dst, v)

        # evaluate the node itself
        return node.eval()

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


    def add_node(self, node, vtx_id = None):
        """
        Add a node in the Graph with a particular id
        if id is None, autogenrate one
        
        @param node : the node instance
        @param elt_id : element id

        @param return the id
        """
        
        vid= vtx_id
        if ( vtx_id not in self ) or ( not vtx_id ):
            vid= self.add_vertex( vtx_id )

        self.node_id[vid] = node
        
        #self.id_cpt += 1
        self.notify_listeners(("graph_modified",))
        self.graph_modified = True

        return vid        


    def remove_node(self, vtx_id):
        """
        remove a node from the graph
        @param elt_id : element id
        """
        
        del self.node_id[vtx_id]
        for id in self.neighbors( vtx_id ):
            del self._edge_ports[ id ]
        self.remove_vertex( vtx_id )

        self.notify_listeners(("graph_modified",))
        self.graph_modified = True

               

    def connect(self, src_id, port_src, dst_id, port_dst):
        """ Connect 2 elements :
        @param src_id : source node id
        @param port_src : source output port number
        @param dst_id : destination node id
        @param port_dst : destination input port number
        """

        if self.has_vertex( src_id ) and self.has_vertex( dst_id ):
            eid = self.add_edge( ( src_id, dst_id ) )
            self._edge_ports[eid] = ( port_src, port_dst )
            #self.connections[(dst_id, port_dst)] = (src_id, port_src)

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
            eid_src = set ( self.out_edges( src_id ) )
            eid_dst = set ( self.in_edges ( dst_id ) ) 
            common_eid= eid_src.intersection( eid_dst )
            assert len( common_eid )
            for id in common_eid:
                if ( port_src, port_dst == self.source( id ), self.target( id ) ):
                    eid= id
                    break
            self.remove_edge( eid )
            del self._edge_ports[ eid ]
            # del(self.connections[ (dst_id, port_dst) ])
        except:
            return

        node_dst = self.node_id[dst_id]
        node_dst.set_input_state(port_dst, "disconnected")
        self.notify_listeners(("connection_modified",))
        self.graph_modified = True

    def factory_id_to_id( self, factory_id ):
        """ 
        Returns the current id of a node corresponding to the factory_id that creates it.
        """
        
        return self._factory_id_to_id[factory_id]

class CompositeNodeInput(Node):
    """Dummy node to represent the composite node inputs"""

    def __init__(self, graph, size):
        """
        Graph is the owner of the object
        Size is the number of port
        """

        Node.__init__(self)
        self.graph = graph
        for i in range(size):
            self.add_output("out%i"%(i,), interface = None)

        self.internal_data['posx'] = 20
        self.internal_data['posy'] = 5


    def get_output(self, index):
        """ Redirect call """

        return self.graph.get_input(index)
        

    def eval(self):
        return True



class CompositeNodeOutput(Node):
    """Dummy node to represent the composite node outputs"""

    def __init__(self, graph, size):
        """
        Graph is the owner of the object
        Size is the number of port
        """
        Node.__init__(self)
        self.graph = graph
        
        for i in range(size):
            self.add_input("in%i"%(i,), interface = None, value = None)

        self.internal_data['posx'] = 20
        self.internal_data['posy'] = 250
        

    def set_input(self, index, val):
        """ Redirect call """

        self.graph.set_output(index, val)

        
    def eval(self):
        #the node must be always calculated
        return True


################################################################################

class PyCNFactoryWriter(object):
    """ CompositeNodeFactory python Writer """

    sgfactory_template = """

    nf = CompositeNodeFactory(pkgmanager,
                              name="$NAME", 
                              description="$DESCRIPTION", 
                              category="$CATEGORY",
                              doc="$DOC",
                              nin=$NIN,
                              nout=$NOUT,
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
        result = fstr.safe_substitute(NAME=f.name,
                                      DESCRIPTION=f.description,
                                      CATEGORY=f.category,
                                      DOC=f.doc,
                                      NIN=f.nb_input,
                                      NOUT=f.nb_output,
                                      ELT_FACTORY=repr(f.elt_factory),
                                      ELT_CONNECTIONS=repr(f.connections()),
                                      ELT_DATA=repr(f.elt_data),
                                      )
        return result





    
