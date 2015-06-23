# -*- python -*-
#
#       OpenAlea.MyModule: MyModule Description
#
#       Copyright 2013-2015 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s): Julien Coste <julien.coste@inria.fr>,
#                            Guillaume Cerutti <guillaume.cerutti@inria.fr>
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
    - control
    - world
"""

__revision__ = '$Id$'

#from openalea.core import *

from openalea.core.node import Node
from openalea.core.observer import AbstractListener

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


class WorldAdder(AbstractWorld):

    def __call__(self, inputs):
        """ inputs is the list of input values """

        obj = inputs[0]
        name = inputs[1]
        kwargs = inputs[2]
        self.set_caption("World object: %s" % name)
        self.world.add(obj,name=name,**kwargs)
        return (obj, )

    def reset(self):
        if hasattr(self, 'key'):
            world.remove(self.key)


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


