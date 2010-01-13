# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Fred Theveny <frederic.theveny@cirad.fr>
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

class PropertyError (Exception) :
    """todo"""
    pass

class IPropertyGraph (object):
    """
    Directed graph with properties associated with edges and vertices
    Properties may not be defined on all elements
    Properties may be empty on some elements
    A property is a map between an element id (vid or eid) and a data
    """
    def vertex_property_names (self) :
        """
        iter on names of all property maps defined on vertices
        return iter of keys
        """
        raise NotImplementedError
    
    def vertex_property (self, property_name) :
        """
        return a map between vid and data for all vertices where
        property_name is defined
    
        :rtype: dict of ``{vid:data}``
        """
        raise NotImplementedError
    
    def edge_property_names (self) :
        """
        iter on names of all property maps defined on edge
        return iter of keys
        """
        raise NotImplementedError
    
    def edge_property (self, property_name) :
        """
        return a map between eid and data for all edges where
        property_name is defined
   
        :rtype: dict of ``{eid:data}``
        """
        raise NotImplementedError

    ###########################################################
    #
    #        mutable property concept
    #
    ###########################################################
    
    def add_vertex_property (self, property_name) :
        """
        add a new map between vid and a data
        do not fill this property for any vertex
        """
        raise NotImplementedError
    
    def remove_vertex_property (self, property_name) :
        """
        remove the map called property_name from the graph
        """
        raise NotImplementedError
    
    def add_edge_property (self, property_name) :
        """
        add a new map between eid and a data
        do not fill this property for any edge
        """
        raise NotImplementedError
    
    def remove_edge_property (self, property_name) :
        """
        remove the map called property_name from the graph
        """
        raise NotImplementedError
