# -*- python -*-
#
#       OpenAlea.Secondnature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "CeCILL v2"
__revision__ = " $Id$ "

from openalea.secondnature.extension_objects import AppletFactory
from openalea.secondnature.extension_objects import Layout
from openalea.secondnature.extension_objects import LayoutSpace
from openalea.secondnature.extension_objects import Document
from openalea.secondnature.extension_objects import EscEventSwallower

import urlparse



class Curve2DFactory(AppletFactory):
    __name__ = "Curve2D"
    __namespace__ = "PlantGL"
    __mimeformats__ = ["application/plantgl-curve"]
    # currently we don't know how to create a curve url, so we don't open anything:
    __supports_open__ = False


    def __init__(self):
        AppletFactory.__init__(self)
        self.__pglEscSwallower = EscEventSwallower()

    def new_document(self):
        from PyQt4 import QtGui
        from vplants.plantgl.gui import curve2deditor

        # -- let the user choose the curve type he wants --
        constraint = curve2deditor.Curve2DConstraint
        constraintName, ok = QtGui.QInputDialog.getItem(None, "Curve type choose",
                                                    "Please choose a curve type",
                                                    ["2D Curve", "Function"],
                                                    editable=False)

        if constraintName == "Function":
            constraint = curve2deditor.FuncConstraint


        data = constraint.defaultCurve()
        iname = "Curve2D"

        document = Document(iname,
                            "PlantGL",
                            data,
                            mimetype=self.__mimeformats__[0],
                            constraintType=constraint)
        return document

    def get_applet_space(self, document):
        from vplants.plantgl.gui import curve2deditor
        curve = document.obj
        constraint = document.get_inner_property("constraintType")
        editor = curve2deditor.Curve2DEditor(None, constraints=constraint())
        editor.setCurve(curve)
        editor.installEventFilter(self.__pglEscSwallower)
        return LayoutSpace(self.__name__, self.__namespace__, editor)



class NurbsPatchFactory(AppletFactory):
    __name__ = "NurbsPatch"
    __namespace__ = "PlantGL"
    __mimeformats__ = ["application/plantgl-nurbspatch"]
    # currently we don't know what is a nurbs url url, so we don't open anything:
    __supports_open__ = False

    def __init__(self):
        AppletFactory.__init__(self)
        self.__pglEscSwallower = EscEventSwallower()

    def new_document(self):
        from vplants.plantgl.gui import nurbspatcheditor

        data = nurbspatcheditor.NurbsPatchEditor.newDefaultNurbsPatch()
        iname = "NurbsPatch"
        document = Document(iname, "PlantGL",
                            data,
                            mimetype=self.__mimeformats__[0])
        return document

    def get_applet_space(self, document):
        from vplants.plantgl.gui import nurbspatcheditor

        patch = document.obj
        editor = nurbspatcheditor.NurbsPatchEditor(None)
        editor.setNurbsPatch(patch)
        editor.installEventFilter(self.__pglEscSwallower)
        return LayoutSpace(self.__name__, self.__namespace__, editor)



class InterpolatedProfileFactory(AppletFactory):
    __name__ = "InterpolatedProfile"
    __namespace__ = "PlantGL"
    __mimeformats__ = ["application/plantgl-interpolatedcurve"]
    # currently we don't know what is a nurbs url url, so we don't open anything:
    __supports_open__ = False

    def __init__(self):
        AppletFactory.__init__(self)
        self.__pglEscSwallower = EscEventSwallower()

    def new_document(self):
        from vplants.plantgl.scenegraph.interpolated_profile import CrossSection
        from vplants.plantgl.scenegraph.interpolated_profile import InterpolatedProfile
        from vplants.plantgl.scenegraph.interpolated_profile import CSplineMethod

        crsSect1 = CrossSection((0., 0.), (0.5, 0.), (0.6, 0.1), (1., 0.))
        crsSect2 = CrossSection((0., 2.), (0.5, 1.), (0.8, 0.3), (1., 0.))
        crsSect3 = CrossSection((0., 0.), (0.5, 0.), (0.7, 0.8), (1., 0.))
        tc = InterpolatedProfile(interpolator=CSplineMethod)

        tc.set_param_range(-180.0, 180.0)
        tc.add_cross_sections(-180, crsSect1,
                              0, crsSect2,
                              180, crsSect3)

        iname = "InterpolatedProfile"

        document = Document(iname,
                            "PlantGL",
                            tc,
                            mimetype=self.__mimeformats__[0] )
        return document

    def get_applet_space(self, document):
        from vplants.plantgl.gui import interpolated_profile_gui

        profile = document.obj
        editor = interpolated_profile_gui.ProfileEditor(editingCentral=False)
        editor.set_profile(profile)
        editor.installEventFilter(self.__pglEscSwallower)
        return LayoutSpace(self.__name__, self.__namespace__, editor)


# -- instantiate widget factories --
curve2d_f = Curve2DFactory()
nurbspatch_f = NurbsPatchFactory()
interpolatedprofile_f = InterpolatedProfileFactory()

