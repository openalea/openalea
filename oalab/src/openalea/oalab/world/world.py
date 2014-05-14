# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
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
__revision__ = ""

import time
from openalea.oalab.scene.vplscene import VPLScene

# from collections import OrderedDict
# from openalea.core.observer import Observed
# class World(OrderedDict, Observed):

class World(VPLScene):
    """
    Contain objects of the world.

    When world changes, it notifies all listeners with these events:
        - WorldObjectChanged(scene, changes)
        - WorldObjectReplaced(scene, key, old_object, new_object)
        - WorldObjectAdded(scene, key, new_object)
        - WorldObjectRemoved(scene, old_object)
        - WorldObjectIndexChanged(scene, old_idx, new_idx)

    A generic "WorldChanged" event is also notified for all previous changes.

    .. warning::

        currently only WorldChanged event is implemented

    """
    def __setitem__(self, key, value):
        if not isinstance(value, WorldObject):
            world_obj = WorldObject(value)
        VPLScene.__setitem__(self, key, world_obj)

class WorldObject(object):
    """
    Object of the world.

    WorldObject provides meta-information like ...
        - origin
        - time required to compute object
        - visibility in scene
        - date when object has been added to scene
    """
    def __init__(self, obj, model_id=None, output_id=None):
        """
        :param obj: object to store
        :param model_id: identifier of the model used to create this object
        :param output_id: identifier of output of the model used to create this object
        :param in_scene: set to True if it is a part of the scene (so it is viewable)
        """
        self.obj = obj
        self.model_id = model_id
        self.output_id = output_id
        self.in_scene = True

