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
    - controls
    - observer
"""

__revision__ = '$Id$'

from openalea.core import *
from openalea.oalab.scene import Scene

# Nodes for read/write in scene

class AbstractScene(Node):
    def __init__(self, inputs, outputs):
        Node.__init__(self, inputs, outputs)
        self.scene = Scene()

class SceneReader(AbstractScene):
    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        obj = self.scene.get(key)
        if key in self.scene:
            self.set_caption("%s"%(key, ))
        return (obj, )


class SceneWriter(AbstractScene):

    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        obj = inputs[1]
        self.set_caption("%s = %s"%(key, obj))
        self.scene[key] = obj
        self.key = key
        return (obj, )

    def reset(self):
        if hasattr(self,'key'):
            del self.scene[self.key]

class SceneDefault(AbstractScene):
    def __init__(self, *args, **kwds):
        AbstractScene.__init__(self,*args, **kwds)
        self.initial_state = True

    def reset(self):
        if hasattr(self,'key'):
            self.scene[self.key] = default_value
        self.initial_state = True

    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        default_value = inputs[1]
        if self.initial_state:
           self.default = default_value if key not in self.scene else self.scene[key]
        self.key = key
        obj = self.scene.setdefault(key, default_value)
        self.set_caption("%s"%(key,))
        return (obj, )

