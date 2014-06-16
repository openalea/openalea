# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA
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

from openalea.core.interface import IInterface

class IColorList(IInterface):
    """
    List of tuple name, rgb(a) color.
    Example:

    [
        ('C1', (255,0,0,255)),
        ('C2', (0,255,0,255))
    ]

    """
    def __init__(self):
        self.value = self.sample()

    def __repr__(self):
        return 'IColorList'

    def sample(self):
        """
        Reinitialize control to default value
        """
        from openalea.plantgl.all import Material, Color3
        value = [
            ("Color_0", (80, 80, 80, 255), 2.), # Grey
            ("Color_1", (65, 45, 15), 2.), # Brown
            ("Color_2", (30, 60, 10), 2.), # Green
            ("Color_3", (60, 0, 0), 2.), # Red
            ("Color_4", (60, 60, 15), 2.), # Yellow
            ("Color_5", (0, 0, 60), 2.), # Blue
            ("Color_6", (60, 0, 60), 2.), # Purple
            ]
        return value


class ICurve2D(IInterface):
    """
    NurbsCurve2D(Point3Array([Vector3(-0.5,0,1),Vector3(-0.166667,0,1),Vector3(0.166667,0,1),Vector3(0.5,0,1)]), width = 2)
    """
    def __init__(self):
        self.value = self.sample()

    def __repr__(self):
        return 'ICurve2D'

    def sample(self):
        """
        Reinitialize control to default value
        """
        from openalea.plantgl.all import NurbsCurve2D, Point3Array, Vector3
        curve = NurbsCurve2D(
            Point3Array([
                Vector3(-0.5, 0, 1),
                Vector3(-0.166667, 0, 1),
                Vector3(0.166667, 0, 1),
                Vector3(0.5, 0, 1)
            ]),
            width=2)
        return curve



