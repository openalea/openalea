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

from collections import OrderedDict


class World(OrderedDict):
    """
    Contain objects of the world.
    """
    # TODO: How to manage time?
    def __init__(self):
        super(World, self).__init__()

    def get_scene(self):
        """
        return only object stock in self that are part of the scene
        """
        return_dict = OrderedDict()
        for obj in self:
            if self[obj].in_scene:
                return_dict[obj] = self[obj]
        return return_dict


class WorldObject(object):
    """
    Object of the world.
    """
    def __init__(self, obj, model_id, output_id, in_scene=False):
        """
        :param obj: object to store
        :param model_id: identifier of the model used to create this object
        :param output_id: identifier of output of the model used to create this object
        :param in_scene: set to True if it is a part of the scene (so it is viewable)
        """
        self.obj = obj
        self.model_id = model_id
        self.output_id = output_id
        self.in_scene = in_scene

    def _repr_qglviewer_(self):
        """
        Return a 3d representation used in the viewer (PyQGLViewer)
        """
        # TODO: use services
        pass
