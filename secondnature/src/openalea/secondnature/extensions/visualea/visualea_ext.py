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

from openalea.secondnature.api import *

from openalea.visualea import dataflowview
from openalea.core.pkgmanager import PackageManager
from openalea.core.compositenode import CompositeNodeFactory, CompositeNode

import urlparse
import visualea_icons

class DT_Dataflow(DataType):
    __name__      = "Dataflow"
    __mimetypes__ = [CompositeNodeFactory.mimetype, CompositeNode.mimetype]
    __icon_rc__   = ":icons/dataflow.png"

    def new(self):
        iname = self.__name__
        node = CompositeNodeFactory(iname).instantiate()
        node.set_caption(iname)
        return Data(node.caption, node, mimetype=CompositeNode.mimetype)

    def open_url(self, parsedUrl):
        pm = PackageManager()
        node = pm.get_node_from_url(parsedUrl)
        return Data(node.caption, node, mimetype=CompositeNode.mimetype)


class DataflowViewFactory(AppletBase):
    __name__ = "Visualea.DataflowView"

    def __init__(self):
        AppletBase.__init__(self)
        self.add_data_type(DT_Dataflow())

    def get_applet_space(self, data):
        node = data.obj
        gwidget = dataflowview.GraphicalGraph.create_view(node)
        return LayoutSpace(gwidget)



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
             skeleton = sk,
             # the widgets we want are those  placed under the
             # `Visualea` application namespace.
             # but you could have "PlantGl.viewer" here too.
             appletmap={1:"Openalea.PackageManager",
                        3:"Visualea.DataflowView",
                        4:"Openalea.Logger"},
             easy_name="Visual Programming")






