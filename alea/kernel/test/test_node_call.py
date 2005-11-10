"""
This module provides the basic tests for alea_node module

:Version: 0.0.1
:Authors: Loic Calvino, Szymon Stoma
"""
from node import *

class TestOne:
    def setup_method(self, method):
        def f1(data):
            print 'f1', data
            return data.copy()
        def f2(data):
            print 'f2', data
            return data.copy()
        def f3(data):
            print 'f3', data
            return data.copy()
        def f4(data):
            print 'f4', data
            return data.copy()
        
        fd1 = {'p1':'1', 'p2': '2'}
 
 
        self.workspace = Workspace()
        self.workspace._add_node(InitialNodeData(1, f1, fd1))
        self.workspace._add_node(InitialNodeData(2, f2))
        self.workspace._add_node(InitialNodeData(3, f3))
        self.workspace._add_node(InitialNodeData(4, f4))
        self.workspace.get_node_by_id(1)._set_output_desc('p1', (2, 'p1'))
        self.workspace.get_node_by_id(1)._set_output_desc('p2', (4, 'p1'))
        self.workspace.get_node_by_id(2)._set_output_desc('p1', (3, 'p1'))
        self.workspace.get_node_by_id(3)._set_output_desc('p1', (4, 'p2'))

    def test_update_functions(self):
        """
        Tests the right order of function call graph.
        """
        assert([1,2,3,4] == self.workspace.update_nodes()
               and self.workspace.get_node_by_id(4).data.output_params['p1'] == '2'
               and self.workspace.get_node_by_id(4).data.output_params['p2'] == '1')
