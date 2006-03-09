"""
This module provides the basic tests for workflow module

:Version: 0.0.1
:Authors: Loic Calvino, Szymon Stoma
"""

import os
pj=os.path.join
import sys
sys.path.append(pj("..","src"))

from workflow import *

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
 
 
        self.workflow = Workflow()
        self.workflow._add_vertex(InitialVertexData(1, f1, fd1))
        self.workflow._add_vertex(InitialVertexData(2, f2))
        self.workflow._add_vertex(InitialVertexData(3, f3))
        self.workflow._add_vertex(InitialVertexData(4, f4))
        self.workflow.get_vertex_by_id(1)._set_output_desc('p1', (2, 'p1'))
        self.workflow.get_vertex_by_id(1)._set_output_desc('p2', (4, 'p1'))
        self.workflow.get_vertex_by_id(2)._set_output_desc('p1', (3, 'p1'))
        self.workflow.get_vertex_by_id(3)._set_output_desc('p1', (4, 'p2'))

    def test_update_functions(self):
        """
        Tests the right order of function call graph.
        """
        assert([1,2,3,4] == self.workflow.update_vertices()
               and self.workflow.get_vertex_by_id(4).data.output_params['p1'] == '2'
               and self.workflow.get_vertex_by_id(4).data.output_params['p2'] == '1')
