# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
"""This module provide a set of concepts to add properties to graph elements
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

class IPortGraph(object):
    """
    Directed graph with connections between in_ports
    of vertices and out_port of vertices
    """
    ####################################################
    #
    #       edge port view
    #
    ####################################################
    def source_port (self, eid) :
        """todo"""
        raise NotImplementedError
    
    def target_port (self, eid) :
        """todo"""
        raise NotImplementedError
    ####################################################
    #
    #       vertex port view
    #
    ####################################################
    def out_ports(self, vid=None) :
        """todo """
        raise NotImplementedError
    
    def in_ports(self, vid=None) :
        """todo """
        raise NotImplementedError
    
    def ports(self, vid=None) :
        """todo """
        raise NotImplementedError
    ####################################################
    #
    #       port view
    #
    ####################################################
    def is_in_port(self, pid):
        """todo """
        raise NotImplementedError
    
    def is_out_port(self, pid) :
        """todo """
        raise NotImplementedError
    
    def vertex (self, pid) :
        """todo """
        raise NotImplementedError
    
    def port_neighbors (self, pid) :
        """todo """
        raise NotImplementedError
    
    def port_edges (self, pid) :
        """todo """
        raise NotImplementedError
    ####################################################
    #
    #       limited number of connections
    #
    ####################################################
    def capacity (self, pid) :
        """todo """
        raise NotImplementedError
    
    def set_capacity (self, pid, capacity) :
        """todo """
        raise NotImplementedError
    ####################################################
    #
    #       local port concept
    #
    ####################################################
    def port (self, pid) :
        """todo """
        raise NotImplementedError
    
    def out_port (self, vid, local_pid) :
        """todo """
        raise NotImplementedError
    
    def in_port (self, vid, local_pid) :
        """todo """
        raise NotImplementedError
    #####################################################
    #
    #       mutable concept
    #
    #####################################################
    def add_in_port (self, vid, local_pid, pid=None) :
        """todo """
        raise NotImplementedError
    
    def add_out_port (self, vid, local_pid, pid=None) :
        """todo """
        raise NotImplementedError
    
    def remove_port (self, pid) :
        """todo """
        raise NotImplementedError
    
    def connect (self, source_pid, target_pid, eid=None) :
        """todo """
        raise NotImplementedError
    
    def disconnect (self, eid) :
        """todo """
        raise NotImplementedError
