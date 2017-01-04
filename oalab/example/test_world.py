# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.oalab.testing.applet import test_applet
from openalea.core.world import World, WorldObject

c1 = dict(min=1, max=5)
c2 = dict(min=0, max=10)

def add_objects_then_attributes():

    world = World()
    world["obj1"] = 1
    world["obj2"] = 2

    obj1 = world["obj1"]
    obj2 = world["obj2"]

    obj1.set_attribute('a1', 1, 'IInt', constraints=c1)
    obj1.set_attribute('a2', True, 'IBool')
    obj2.set_attribute('b1', 2.34, 'IFloat', constraints=c2)

def add_objects_with_attributes_set():
    """
    Attributes are defined before adding object to world.
    Results is less signals sent by world
    """
    world = World()
    world.clear()
    obj1 = WorldObject("obj1", 1)
    obj2 = WorldObject("obj2", 2)

    obj1.set_attribute('a1', 1, 'IInt', constraints=c1)
    obj1.set_attribute('a2', True, 'IBool')
    obj2.set_attribute('b1', 2.34, 'IFloat', constraints=c2)

    world["obj1"] = obj1
    world["obj2"] = obj2

if __name__ == '__main__':
    test_applet('WorldControl', 'World', tests=[
        add_objects_with_attributes_set,
        add_objects_then_attributes
    ])
