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

from openalea.secondnature.extendable_objects import *

import urlparse

from openalea.visualea import dataflowview
from openalea.core.pkgmanager import PackageManager
from openalea.core.compositenode import CompositeNodeFactory, CompositeNode



#lets create the PackageManager ressource
from openalea.secondnature.ripped.node_treeview import NodeFactoryTreeView, PkgModel
model    = PkgModel(PackageManager())
pmurl    = "oa://pm.local"
pmanager = Document("PackageManager", "Visualea", pmurl, model, category="system")


class PackageManagerFactory(SingletonWidgetFactory):
    __name__ = "PackageManager"
    __namespace__ = "Visualea"

    def handles(self, url):
        return pmurl == url.geturl()

    def _instanciate_space(self, url):
        assert self.handles(url)
        view = NodeFactoryTreeView(None)
        view.setModel(model)
        return None, LayoutSpace(self.__name__, self.__namespace__, view )




class DataflowViewFactory(WidgetFactory):
    __name__ = "Dataflowview"
    __namespace__ = "Visualea"

    def __init__(self):
        WidgetFactory.__init__(self)
        self.__ctr = 0

    def split_query(self, query):
        return urlparse.parse_qs(query)

    def _instanciate_space(self, url):
        node = None
        if url is None:
            iname = "Dataflow " + str(self.__ctr)
            node = CompositeNodeFactory(iname).instantiate()
            self.__ctr += 1
            node.set_caption(iname)
            url = urlparse.ParseResult(scheme="oa",
                                       netloc="local",
                                       path  ="/unknown",
                                       params = "",
                                       query ="?fac="+iname+"&ft=CompositeNodeFactory",
                                       fragment = ""
                                       )
        else:
            assert self.handles(url)
            pm = PackageManager()
            node = pm.get_node_from_url(url)

        gwidget = dataflowview.GraphicalGraph.create_view(node)
        document = Document(node.caption, "Visualea", url.geturl(), node)
        return document, LayoutSpace(self.__name__, self.__namespace__, gwidget)

    def handles(self, url):
        assert isinstance(url, urlparse.ParseResult)
        good = False
        if url.scheme == "oa" and url.netloc == "local":
            queries = urlparse.parse_qs(url.query)
            if "ft" not in queries or "CompositeNodeFactory" not in queries["ft"]:
                good = False
            else:
                good = True
        return good



# -- instantiate widget factories --
dataflow_f = DataflowViewFactory()
pmanager_f = PackageManagerFactory()




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
             widgetmap={1:"Visualea.PackageManager",
                        4:"Openalea.Logger"})

df2 = Layout("Dataflow Editing2",
             "Visualea",
             skeleton=sk,
             widgetmap={4:"Visualea.PackageManager",
                        3:"Openalea.Logger"})




