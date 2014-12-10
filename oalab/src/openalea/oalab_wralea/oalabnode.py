# -*- python -*-
#
#       OpenAlea.MyModule: MyModule Description
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): FirstName LastName <firstname.lastname@lab.com>
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
"""
Visual Programming nodes define to interact with the oalab application components like:
    - the scene
    - control
    - observer
"""

__revision__ = '$Id$'

from openalea.core import *
from openalea.plantgl.all import Scene as PglScene
from openalea.oalab.world.world import World
from openalea.core.control.manager import ControlManager

# Nodes for read/write in world


class AbstractWorld(Node):

    def __init__(self, inputs, outputs):
        Node.__init__(self, inputs, outputs)
        self.world = World()


class WorldReader(AbstractWorld):

    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        obj = self.world.get(key)
        if key in self.world:
            self.set_caption("%s" % (key, ))
        return (obj, )


class WorldWriter(AbstractWorld):

    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        obj = inputs[1]
        self.set_caption("%s = %s" % (key, obj))
        self.world[key] = obj
        self.key = key
        return (obj, )

    def reset(self):
        if hasattr(self, 'key'):
            del self.world[self.key]


class WorldDefault(AbstractWorld):

    def __init__(self, *args, **kwds):
        AbstractWorld.__init__(self, *args, **kwds)
        self.initial_state = True

    def reset(self):
        if hasattr(self, 'key'):
            self.world[self.key] = default_value
        self.initial_state = True

    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        default_value = inputs[1]
        if self.initial_state:
            self.default = default_value if key not in self.world else self.world[key]
        self.key = key
        obj = self.world.setdefault(key, default_value)
        self.set_caption("%s" % (key,))
        return (obj, )


class Control(Node, AbstractListener):

    def __init__(self, inputs, outputs):
        Node.__init__(self, inputs, outputs)
        AbstractListener.__init__(self)
        self.cm = ControlManager()
        self.cm.register_listener(self)

    def notify(self, sender, event):
        signal, data = event
        if signal == 'control_value_changed':
            self.invalidate()
            print 'control changed'
        elif signal == 'control_name_changed':
            ctrl, name = data
            self.set_input(0, name)
            self.set_caption(name)
            self.notify_listeners(("input_modified", 0))

    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        if key in self.cm:
            obj = self.cm.control(name=key)
            self.set_caption("%s" % (key, ))
        if isinstance(obj, list):
            obj = obj[0]
        return (obj.value, )


class Scene2Geom(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name="scene", interface=None)
        self.add_output(name="geom", interface=None)
        #self.add_output( name = "geom2", interface = None)
        #self.add_output( name = "geom3", interface = None)

    def __call__(self, inputs):
        scene = inputs[0]
        geom = scene[0].geometry
        #geom2 = scene[1].geometry
        #geom3 = scene[2].geometry
        return (geom,)


class Geom2Scene(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name="geom", interface=None)
        self.add_output(name="scene", interface=None)

    def __call__(self, inputs):
        geometry = inputs[0]
        scene = PglScene([geometry])
        return (scene, )
