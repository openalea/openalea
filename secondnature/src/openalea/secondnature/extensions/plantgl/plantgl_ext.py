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

    # currently we don't know how to create a curve url, so we don't open anything:
    __supports_open__ = False

    def __init__(self):
        AppletFactory.__init__(self)
        self.__pglEscSwallower = EscEventSwallower()
        self.__ctr = 0

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
        iname = "Curve2D " + str(self.__ctr)
        self.__ctr += 1
        #ugh????? what is an url for a patch?
        parsedUrl = urlparse.ParseResult(scheme="oa",
                                         netloc="local",
                                         path  ="/unknown",
                                         params = "",
                                         query ="fac="+iname+"&ft=Curve2D",
                                         fragment = ""
                                         )

        document = Document(iname, "PlantGL", parsedUrl.geturl(),
                            data, constraintType=constraint)
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

    # currently we don't know what is a nurbs url url, so we don't open anything:
    __supports_open__ = False

    def __init__(self):
        AppletFactory.__init__(self)
        self.__pglEscSwallower = EscEventSwallower()
        self.__ctr = 0

    def new_document(self):
        from vplants.plantgl.gui import nurbspatcheditor

        data = nurbspatcheditor.NurbsPatchEditor.newDefaultNurbsPatch()
        iname = "NurbsPatch " + str(self.__ctr)
        self.__ctr += 1
        #ugh????? what is an url for a patch?
        parsedUrl = urlparse.ParseResult(scheme="oa",
                                         netloc="local",
                                         path  ="/unknown",
                                         params = "",
                                         query ="fac="+iname+"&ft=NurbsPatch",
                                         fragment = ""
                                         )
        document = Document(iname, "PlantGL", parsedUrl.geturl(), data)
        return document

    def get_applet_space(self, document):
        from vplants.plantgl.gui import nurbspatcheditor

        patch = document.obj
        editor = nurbspatcheditor.NurbsPatchEditor(None)
        editor.setNurbsPatch(patch)
        editor.installEventFilter(self.__pglEscSwallower)
        return LayoutSpace(self.__name__, self.__namespace__, editor)



# -- instantiate widget factories --
curve2d_f = Curve2DFactory()
nurbspatch_f = NurbsPatchFactory()


