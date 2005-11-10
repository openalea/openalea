"""
This module provides basic internal alea Node class, with is managed by Workspace class.

:Version: 0.0.1
:Authors: Loic Calvino, Szymon Stoma
"""
from top_sort import *

class Workspace(object):
    '''
    This is a basic class for storing and managing nodes.
    
    TODO extend the docs..
    '''
    def __init__(self):
        '''
        Default init.
        '''
        self._nodes = {}

    def _add_node(self, node_data):
        '''
        Adds an node to the current workspace instance.

        @type node_data: InitialNodeData
        @param node_data: data to initialize the node
        '''
        self._nodes[node_data.id] = Node(node_data, self)

    def add_node(self, node):
        """
        Adds an node to the current workspace instance.

        :Parameters:
         - `node`
        """
        self._nodes[node.data.id] = node
                
    def get_node_by_id(self, id):
        '''
        Returns the node described by id.

        @type id: integer?
        @param id: the id
        '''
        return self._nodes[id]

    def update_nodes(self):
        '''
        Recalculate the node information.

        TODO: correct efficiency of call_functions (too many nodes are updated)
        '''
        V = []
        E = []
        for w_id in self._nodes.keys():
            V.append(w_id)

        for w_id in V:
            deps = self._nodes[w_id].dependencies
            for d in deps:
                E.append((V.index(d), V.index(w_id)))

        callOrder = top_sort(V,E)
        self.call_functions(callOrder)
        return callOrder

    def call_functions(self, callOrder):
        """
        Call all the functions associated to nodes from callOrder id nodes list.

        :Parameters:
         - `callOrder`: list of id nodes
        :Types:
         - `callOrder`: list of integers
        """
        l = []
        for i in callOrder:
            if self.get_node_by_id(i).is_calculated == False:
                l = callOrder[callOrder.index(i):]
                break
        for e in l:
            self.get_node_by_id(e).call()

    def connect(self, (node1, output_name), (node2, input_name)):
        """
        Connect two nodes.

        It connects the output of the first argument with the input of the second argument.

        :Parameters:
         - `node1`: The first node
         - `node2`: The second node
         - `output_name`: blbla
         blabal
        :Types:
         - `node1`: Node
         ...

        @type node1: Node
        @param node1: The first node
        @type output_name: String
        @param output_name: The name of the output of the node1
        @type node2: Node
        @param node2: The second node
        @type input_name: String
        @param input_name: The name of the input of the node2
        """
        if node1.data.output_desc.has_key(output_name):
            connected_node = self.workspace.get_node_by_id(node1.data.output_desc[output_name]['id'])
            connected_node.dependencies.remove(node1.data.id)
        node1.data.output_desc[output_name] = {'id':node2.data.id, 'param':input_name}
        node2.dependencies = node1.data.id
              
            
class InitialNodeData(object):
    '''
    Data used to initialise the node.
    '''
    def __init__(self, id_, function, input_params = {}):
        self.name = ''
        self.id = id_
        self.function = function
        self.output_desc = {}
        self.input_params = input_params.copy()
        # the result params of the function are stored in output_params
        self.output_params = {}
        self.workspace = None
        # contain the ids` of Nodes on which depand the Node
        self._dependency = []


class Node(object):
    '''
    Basic node class.
    '''  
    def __init__(self, initial_node_data, workspace=None):
        '''
        Default init method.

        :Parameters:
         - `initial_node_data`: data used to initialise the node.
         - `workspace`: workspace to which the node is connected.
        :Types:
         - `initial_node_data`: InitialNodeData
         - `workspace`: Workspace
        '''
        # it is set to True when the result is calculated
        self.is_calculated = False
        self.data = initial_node_data
        self.data.workspace = workspace

    def __repr__(self):
        return '__\n'+str(self.data.function)+'\n'+str(self.data.input_params)+'\n'+str(self.data.output_params)+'\n'
        
    def call(self):
        '''
        Call the function associated to the node, update parameters.
        '''
        self.data.output_params = self.data.function(self.data.input_params)
        self.is_calculated = True
        self._update_others_inputs()
        
    def _set_output_desc(self, output_name, (node_id, input_name)):
        '''
        update self.data.output_param_desc data insertig inforamtion about connections to others Nodes, update dependency list conected Node.

        "name" output will be connected with Node "node_id" to the input "name_of_input"  
        '''

        if self.data.output_desc.has_key(output_name):
            connected_node = self.data.workspace.get_node_by_id(self.data.output_desc[output_name]['id'])
            connected_node.dependencies.remove(self.data.id)
        self.data.output_desc[output_name] = {'id':node_id, 'param':input_name}
        self.data.workspace.get_node_by_id(node_id).dependencies = self.data.id
                
    def _set_input(self, input_name, value):
        '''
        sets the self.data.input_params["input_name"] to "value"
        '''
        self.data.input_params[input_name] = value

    def update_node(self, d={}):
        """
        Update node inputs using the data from the dictionnary.

        :Parameters:
          - 'd': dictionnary  {input_name : value} (default=0)
        """
        if len(d)==0:
            self.is_calculated = False
        else:
            for k,v in d.iteritems():
                self._set_input(k,v)

    def _update_others_inputs(self):
        '''
        checks self.data.output_desc and updates all connected node params
        '''
        for e in self.data.output_desc.keys():
            id_of_node = self.data.output_desc[e]['id']
            name_of_node_param = self.data.output_desc[e]['param']
            self.data.workspace.get_node_by_id(id_of_node)._set_input(name_of_node_param, self.data.output_params[e])

    def get_dependencies(self):
        return self.data._dependency

    def set_dependency(self, id):
        self.data._dependency.append(id)

    dependencies = property(get_dependencies, set_dependency, None, "List of dependencies id")
