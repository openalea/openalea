# -*- python -*-
#
#       OpenAlea.SoftwareBus: OpenAlea software bus
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

__doc__="""
This module defines all the base class for the OpenAlea Kernel (Node, Package...)
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

###############################################################################


# Exceptions

class UnknownNodeError (Exception):
    pass


class RecursionError (Exception):
    pass

class InstantiationError(Exception):
    pass

###############################################################################



class Node(object):
    """
    Base class for all Nodes.
    A Node is a callable object with typed inputs and outputs.
    """

    def __init__(self):

        # Effective values

        self.input_values = []
        self.output_values = []

        # Default values

        self.input_defaults = []
        self.output_defaults = []

        # Types
        
        self.input_types = []
        self.output_types = []
        

    def __call__(self):
        """ Call function. Must be overriden """
        
        raise RuntimeError('Node function not implemented.')


    # Functions used by the node implementation

    def get_input(self, index):
        """
        Return an input port value
        Retun default value if not set
        """

        ret=self.input_values[index]
        if ( ret == None ):
            return self.input_defaults[index]

        
        return ret
        

    def set_output(self, index, val):
        """
        Set the specified output port
        """

        self.output_values[index] = val


    def define_inputs(self, typelist):
        """
        Create the input ports

        @param : typelist is a list of interface objects
        The size of the list define the numbre of inputs.
        Use None if there is no type restriction
        """

        self.input_types = typelist[:]
        self.input_values = [None] * len( typelist )
        self.input_defaults = [None] * len( typelist )

    def set_default_input(self, index, value):
        """
        Define the default value for an input port.
        Port must before be created with define_inputs
        """

        self.input_defaults[index] = value

    def define_outputs(self, typelist):
        """
        Create the input ports

        @param : typelist is a list of interface objects
        The size of the list define the numbre of inputs.
        Use None if there is no type restriction
        """

        self.output_types = typelist[:]
        self.output_values = [None] * len( typelist )



    # Functions used by the evaluator
    def eval(self):
        """ Evaluate the node """

        inlist=[]
        # generate input value list ( with defaults )
        for i in range(len(self.input_values)):
            inlist.append(self.get_input(i))

        outlist = self.__call__(inlist)

        for i in range( min ( len(outlist), len(self.output_values))):
            self.output_values[i]=outlist[i]
        
    
    def get_in_type(self, index):

        return self.input_types[index]
    
    def get_out_type(self, index):
        
        return self.output_types[index]


    def set_input(self, index, val):

        self.input_values[index] = val

    def get_output(self, index):

        return self.output_values[index]

    def get_nb_input(self):
        return len(self.input_values)
    


###############################################################################




class NodeFactory:
    """
    A Node factory is able to create node on demand, and their associated widget.
    """

    mimetype = "openalea/nodefactory"

    def __init__(self, name,
                 desc='', doc='',
                 cat='Default',
                 module='',
                 nodeclass=None,
                 widgetclass=None):
	"""
	Create a node factory.
	
	 >>> n= NodeFactory('MyNode', 'This is my node', 'Data',
                            'from data import mynode, mywidget',
                             'mynode', 'mywidget')

	:Parameters:
	  - `name` : user name for the node (must be unique)
	  - `desc` : description of the node
          - `doc` : node description
	  - `cat` : category of the node
          - `module` : 'python module to import'
	  - `nodeclass` :  node class name to be created
	  - `widgetclass` : widget class name
	
	  - `name` : String
	  - `desc` : String
	  - `cat` : String
          - `module` : String
	  - `nodeclass` : String
	  - `widgetclass` : String
	"""

        self.name = name
        self.description = desc
        self.doc = doc
        self.category = cat
        self.module = module
        self.nodeclass_name = nodeclass
        self.widgetclass_name = widgetclass
        

    def get_id(self):
        """ Return the node factory Id """
        return self.name

    def get_tip(self):
        """ Return the node description """

        return "Name : %s\n"%(self.name,) +\
               "Cat  : %s\n"%(self.category,) +\
               "Desc : %s\n"%(self.description,) + \
               "Doc  : %s\n"%(self.doc,)

    def get_xmlwriter(self):
        """ Return an instance of a xml writer """

        from pkgreader import NodeFactoryXmlWriter
        return NodeFactoryXmlWriter(self)
        

    def instantiate(self, call_stack=[]):
        """ Return a node instance
        @param call_stack : the list of NodeFactory id already in call stack
        (in order to avoir infinite recursion)
        """

        if(self.module):
            exec("from %s import %s as tmpclass" %(self.module,self.nodeclass_name))
        
            return tmpclass()
        
        raise InstantiationError()
    

    def instantiate_widget(self, node, parent=None):
        """ Return the corresponding widget initialised with node """

        if(self.module and self.self.widgetclass_name):
            exec("from %s import %s as widgetclass" %(self.module, self.widgetclass_name))

            return widgetclass(node, self, parent)
        
        else:
            try:
                # if no widget declared, we create a default one
                from visualea.node_widget import NodeWidget
                return NodeWidget(node, self, parent)
            
            except ImportError:
                raise InstantiationError()



###############################################################################

        

class Package(dict):
    """
    A Package is a dictionnary of node factory.
    Each node factory is able to generate node and their widget

    Meta informations are associated with a package.
    """

    mimetype = "openalea/package"


    def __init__(self, name, metainfo) :
	"""
        Create a Package

        @param name : a unique string that will be used as an unique identifier for the package
        @param metainfo : a dictionnary for metainformation. Attended keys are :
            license : a string ex GPL, LGPL, Cecill, Cecill-C
            version : a string
            authors : a string
            institutes : a string
            description : a string for the package description
            publication : optional string for publications
            
	"""

        dict.__init__(self)
        
        self.name = name
        self.metainfo = metainfo

        # association between node name and node factory
        #self.__node_factories = {}


    def get_id(self):
        """ Return the package id """
        return self.name

    def get_tip(self):
        """ Return the package description """

        str= "Package : %s\n"%(self.name,)
        try: str+= "Description : %s\n"%(self.metainfo['description'],)
        except : pass
        try: str+= "Institutes : %s\n"%(self.metainfo['institutes'],)
        except : pass 

        return str


    def get_metainfo(self, key):
        """Return a meta information. See the standard key the __init__ function documentation"""

        return self.metainfo[key]


    def add_nodefactory(self, nodefactory):
        """ Add to the package a node factory """
        self[ nodefactory.name ] = nodefactory


    def get_node_names(self):
        """ Return all the names of the available nodes in a list"""

        return self.keys()
    

    def get_nodefactory(self, id):
        """ Return the node factory associated with id """

        try:
            nodefactory = self[id]
        except KeyError:
            raise UnknownNodeError()

        return nodefactory


    def get_node_info(self, id):
        """ Return the tuple (name, category, description, doc) for the node factory id """

        nf = self.get_nodefactory(id)

        return (nf.name, nf.category, nf.description, nf.doc)

        


        

###############################################################################

def pid(package):
    """ Package id. """
    return package.name

