"""
This module provides basic internal alea Vertex class, with is managed by Workspace class.

:Version: 0.0.1
:Authors: Loic Calvino, Szymon Stoma
"""
from top_sort import *

class Workflow(object):
    '''
    This is a basic class for storing and managing vertices.
    
    TODO extend the docs..
    '''
    def __init__(self):
        '''
        Default init.
        '''
        self._vertices = {}

    def _add_vertex(self, vertex_data):
        '''
        Adds an vertex to the current workflow instance.

        @type vertex_data: InitialVertexData
        @param vertex_data: data to initialize the vertex
        '''
        self._vertices[vertex_data.id] = Vertex(vertex_data, self)

    def add_vertex(self, vertex):
        """
        Adds an vertex to the current workflow instance.

        :Parameters:
         - `vertex`
        """
        self._vertices[vertex.data.id] = vertex
                
    def get_vertex_by_id(self, id):
        '''
        Returns the vertex described by id.

        @type id: integer?
        @param id: the id
        '''
        return self._vertices[id]

    def update_vertices(self):
        '''
        Recalculate the vertex information.

        TODO: correct efficiency of call_functions (too many vertices are updated)
        '''
        V = []
        E = []
        for w_id in self._vertices.keys():
            V.append(w_id)

        for w_id in V:
            deps = self._vertices[w_id].dependencies
            for d in deps:
                E.append((V.index(d), V.index(w_id)))

        callOrder = top_sort(V,E)
        self.call_functions(callOrder)
        return callOrder

    def call_functions(self, callOrder):
        """
        Call all the functions associated to vertices from callOrder id vertices list.

        :Parameters:
         - `callOrder`: list of id vertices
        :Types:
         - `callOrder`: list of integers
        """
        l = []
        for i in callOrder:
            if self.get_vertex_by_id(i).is_calculated == False:
                l = callOrder[callOrder.index(i):]
                break
        for e in l:
            self.get_vertex_by_id(e).call()

    def connect(self, (vertex1, output_name), (vertex2, input_name)):
        """
        Connect two vertices.

        It connects the output of the first argument with the input of the second argument.

        :Parameters:
         - `vertex1`: The first vertex
         - `vertex2`: The second vertex
         - `output_name`: blbla
         blabal
        :Types:
         - `vertex1`: Vertex
         ...

        @type vertex1: Vertex
        @param vertex1: The first vertex
        @type output_name: String
        @param output_name: The name of the output of the vertex1
        @type vertex2: Vertex
        @param vertex2: The second vertex
        @type input_name: String
        @param input_name: The name of the input of the vertex2
        """
        if vertex1.data.output_desc.has_key(output_name):
            connected_vertex = self.workflow.get_vertex_by_id(vertex1.data.output_desc[output_name]['id'])
            connected_vertex.dependencies.remove(vertex1.data.id)
        vertex1.data.output_desc[output_name] = {'id':vertex2.data.id, 'param':input_name}
        vertex2.dependencies = vertex1.data.id
              
            
class InitialVertexData(object):
    '''
    Data used to initialise the vertex.
    '''
    def __init__(self, id_, function, input_params = {}):
        self.name = ''
        self.id = id_
        self.function = function
        self.output_desc = {}
        self.input_params = input_params.copy()
        # the result params of the function are stored in output_params
        self.output_params = {}
        self.workflow = None
        # contain the ids` of Vertices on which depand the Vertex
        self._dependency = []


class Vertex(object):
    '''
    Basic vertex class.
    '''  
    def __init__(self, initial_vertex_data, workflow=None):
        '''
        Default init method.

        :Parameters:
         - `initial_vertex_data`: data used to initialise the vertex.
         - `workflow`: workflow to which the vertex is connected.
        :Types:
         - `initial_vertex_data`: InitialVertexData
         - `workflow`: Workflow
        '''
        # it is set to True when the result is calculated
        self.is_calculated = False
        self.data = initial_vertex_data
        self.data.workflow = workflow

    def __repr__(self):
        return '__\n'+str(self.data.function)+'\n'+str(self.data.input_params)+'\n'+str(self.data.output_params)+'\n'
        
    def call(self):
        '''
        Call the function associated to the vertex, update parameters.
        '''
        self.data.output_params = self.data.function(self.data.input_params)
        self.is_calculated = True
        self._update_others_inputs()
        
    def _set_output_desc(self, output_name, (vertex_id, input_name)):
        '''
        update self.data.output_param_desc data insertig inforamtion about connections to others Vertices, update dependency list conected Vertex.

        "name" output will be connected with Vertex "vertex_id" to the input "name_of_input"  
        '''

        if self.data.output_desc.has_key(output_name):
            connected_vertex = self.data.workflow.get_vertex_by_id(self.data.output_desc[output_name]['id'])
            connected_vertex.dependencies.remove(self.data.id)
        self.data.output_desc[output_name] = {'id':vertex_id, 'param':input_name}
        self.data.workflow.get_vertex_by_id(vertex_id).dependencies = self.data.id
                
    def _set_input(self, input_name, value):
        '''
        sets the self.data.input_params["input_name"] to "value"
        '''
        self.data.input_params[input_name] = value

    def update_vertex(self, d={}):
        """
        Update vertex inputs using the data from the dictionnary.

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
        checks self.data.output_desc and updates all connected vertex params
        '''
        for e in self.data.output_desc.keys():
            id_of_vertex = self.data.output_desc[e]['id']
            name_of_vertex_param = self.data.output_desc[e]['param']
            self.data.workflow.get_vertex_by_id(id_of_vertex)._set_input(name_of_vertex_param, self.data.output_params[e])

    def get_dependencies(self):
        return self.data._dependency

    def set_dependency(self, id):
        self.data._dependency.append(id)

    dependencies = property(get_dependencies, set_dependency, None, "List of dependencies id")
