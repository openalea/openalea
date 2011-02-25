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

import urlparse

from openalea.visualea import dataflowview
from openalea.core.pkgmanager import PackageManager
from openalea.core.compositenode import CompositeNodeFactory, CompositeNode


class DataflowViewFactory(AppletFactory):
    __name__ = "DataflowView"
    __namespace__ = "Visualea"
    __mimeformats__ = [CompositeNodeFactory.mimetype]

    def __init__(self):
        AppletFactory.__init__(self)
        self.__ctr = 0

    def new_document(self):
        iname = "Dataflow " + str(self.__ctr)
        node = CompositeNodeFactory(iname).instantiate()
        self.__ctr += 1
        node.set_caption(iname)
        parsedUrl = urlparse.ParseResult(scheme="oa",
                                         netloc="local",
                                         path  ="/unknown",
                                         params = "",
                                         query ="fac="+iname+"&ft=CompositeNodeFactory",
                                         fragment = ""
                                         )
        document = Document(node.caption, "Visualea", parsedUrl.geturl(), node)
        return document

    def open_document(self, parsedUrl):
        pm = PackageManager()
        node = pm.get_node_from_url(parsedUrl)
        document = Document(node.caption, "Visualea", parsedUrl.geturl(), node)
        return document

    def get_applet_space(self, document):
        node = document.obj
        gwidget = dataflowview.GraphicalGraph.create_view(node)
        return LayoutSpace(self.__name__, self.__namespace__, gwidget)



# -- instantiate widget factories --
dataflow_f = DataflowViewFactory()


# -- instantiate layouts --
sk = "{0: [1, 2], 2: [3, 4]},"+\
     "{0: None, 1: 0, 2: 0, 3: 2, 4: 2},"+\
     "{0: {'amount': 0.2, 'splitDirection': 1},"+\
     "1: {},"+\
     "2: {'amount': 0.7, 'splitDirection': 2},"+\
     "3: {}, 4: {}}"


df1 = Layout("Dataflow Editing",
             "Visualea",
             skeleton = sk,
             # the widgets we want are those  placed under the
             # `Visualea` application namespace.
             # but you could have "PlantGl.viewer" here too.
             appletmap={1:"Openalea.PackageManager",
                        3:"Visualea.DataflowView",
                        4:"Openalea.Logger"},
             easy_name="Visual Programming")






