# -*- coding: latin-1 -*-

__doc__=" Example to use starter package "

from openalea.starter.sceneobject import Trunk, Leaf
from openalea.starter.scenecontainer import Scene
from openalea.starter.tree import Tree

#create a scene object
s=Scene()

#create a  trunk object
t=Trunk()

#add trunk to scene
s.add_object(t)

#add 10 leafs to the scene
for i in range(2):

    l=Leaf()
    s.add_object(l)

#create a complete tree
tr=Tree(6)
#add tree to scene
s.add_object(tr)


#display scene
s.display_scene()
