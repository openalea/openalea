# -*- python -*-
#
#       OpenAlea.Starter: Example package
#
#       Copyright 2006 INRIA - CIRAD - INRA  
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
This module extends the sceneobject hierarchy and adds the tree class
"""

__license__= "Cecill-C"
__revision__=" $Id$ "



import sceneobject
import copy

class Tree(sceneobject.SceneObject) :
    """Sceneobject : Represents a tree composed by a trunk and several leafs"""

    def __init__(self, nbleaf):
        """Create a tree with nbleaf leafs"""

        sceneobject.SceneObject.__init__(self)

        self.leaf_list=[]
        self.trunk=sceneobject.Trunk()

        #create the leafs
        for i  in range(nbleaf):
            self.leaf_list.append(sceneobject.Leaf())


    def get_name(self):
        """Return the name"""
        return "Tree"

    def display(self):
        """Display the entire tree"""
        print self.get_name()
        print "  "+self.trunk.get_name()
        for l in self.leaf_list:
            print "  "+l.get_name()



