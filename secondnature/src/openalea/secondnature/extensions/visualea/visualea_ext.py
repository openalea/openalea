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

class DT_Dataflow(DataReader):
    __name__             = "Dataflow"
    __created_mimetype__ = CompositeNode.mimetype
    __opened_mimetypes__ = [CompositeNodeFactory.mimetype]
    __icon_rc__   = ":icons/dataflow.png"

    def new(self):
        iname = self.__name__
        node = CompositeNodeFactory(iname).instantiate()
        node.set_caption(iname)
        return self.wrap_data(node.caption, node)

    def open_url(self, parsedUrl):
        pm = PackageManager()
        node = pm.get_node_from_url(parsedUrl)
        return self.wrap_data(node.caption, node)

    def data_to_stream(self, data, stream):
        cn  = data.obj
        cn.set_caption(data.name)
        fac = cn.factory
        cn.to_factory(fac)
        writer = fac.get_writer()
        facStr = str(writer)
        stream.write(facStr)

    def data_from_stream(self, name, stream, type_):
        facStr = stream.read()
        facStr = facStr[facStr.index("=")+1:]
        factory = eval(facStr)
        obj = factory.instantiate()
        return self.wrap_data(name, obj, type_)


class DataflowViewFactory(AbstractApplet):
    __name__          = "DataflowView"
    __datafactories__ = [DT_Dataflow]

    def create_space_content(self, data):
        node = data.obj
        gwidget = dataflowview.GraphicalGraph.create_view(node, clone=True)
        return SpaceContent(gwidget)



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
             appletmap={1:"PackageManager",
                        3:"DataflowView",
                        4:"Logger"},
             easy_name="Visual Programming")






