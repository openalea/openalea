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

from openalea.secondnature.extendable_objects import AppletFactory
from openalea.secondnature.extendable_objects import Layout
from openalea.secondnature.extendable_objects import LayoutSpace
from openalea.secondnature.extendable_objects import Document

import urlparse

from vplants.plantgl.gui import curve2deditor


class Curve2DFactory(AppletFactory):
    __name__ = "Curve2D"
    __namespace__ = "PlantGL"
    
    # currently we don't know how to create a curve url, so we don't open anything:
    __supports_open__ = False 
    
    def __init__(self):
        AppletFactory.__init__(self)
        self.__ctr = 0

    def new_document(self):
        data = curve2deditor.Curve2DConstraint().defaultCurve()
        iname = "Curve2D " + str(self.__ctr)
        self.__ctr += 1
        #ugh????? what is an url for a curve?
        parsedUrl = urlparse.ParseResult(scheme="oa",
                                         netloc="local",
                                         path  ="/unknown",
                                         params = "",
                                         query ="fac="+iname+"&ft=Curve2D",
                                         fragment = ""
                                         )
        document = Document(iname, "Visualea", parsedUrl.geturl(), data)
        return document

    def get_applet_space(self, document):
        curve = document.obj
        editor = curve2deditor.Curve2DEditor(None)
        editor.setCurve(curve)
        return LayoutSpace(self.__name__, self.__namespace__, editor)



# -- instantiate widget factories --
curve2d_f = Curve2DFactory()


