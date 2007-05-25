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
Starter unit tests
"""

__license__= "Cecill-C"
__revision__=" $Id"



from openalea.starter.sceneobject import SceneObject, Trunk, Leaf
from openalea.starter.scenecontainer import Scene
from openalea.starter.tree import Tree


class TestSceneObject:
    """Test the SceneObject class"""

    def setup_method(self, method):
        self.sceneobj = SceneObject()

    def teardown_method(self, method):
        self.sceneobj = None

    def test_name(self):
        try :
            self.sceneobj.get_name()
        except RuntimeError :
            pass
        except :
            assert False


class TestLeaf:
    """Test the Leaf class"""

    def setup_method(self, method):
        self.leaf = Leaf()

    def teardown_method(self, method):
        self.leaf = None

    def test_name(self):
        assert self.leaf.get_name() == "Leaf"

        
class TestTrunk:
    """Test the Trunk class"""

    def setup_method(self, method):
        self.trunk = Trunk()

    def teardown_method(self, method):
        self.trunk = None

    def test_name(self):
        assert self.trunk.get_name() == "Trunk"

        
class TestTree:
    """Test the Tree class"""

    def setup_method(self, method):
        self.nbleaf=20
        self.tree = Tree(self.nbleaf)

    def teardown_method(self, method):
        self.tree = None

    def test_name(self):
        assert self.tree.get_name() == "Tree"
        
    def test_leaf(self):
        assert len(self.tree.leaf_list)== self.nbleaf 


class TestScene:
    """Test the Scene class"""

    def setup_method(self, method):
        self.scene = Scene()

    def teardown_method(self, method):
        self.scene = None

    def test_size(self):
        self.scene.add_object(Leaf())
        self.scene.add_object(Trunk())
        self.scene.add_object(Tree(2))
        assert self.scene.get_size() == 3


