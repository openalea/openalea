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
    - the scene
"""

__revision__ = '$Id$'


from openalea.core.node import Node

from openalea.plantgl.all import Scene as PglScene

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