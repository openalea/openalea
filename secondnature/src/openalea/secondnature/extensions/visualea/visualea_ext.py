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


from openalea.core.pkgmanager import PackageManager
from openalea.core.compositenode import CompositeNodeFactory, CompositeNode

import urlparse
import visualea_icons

# -- Datapool and Datapool view --
class DT_DataPool(SingletonFactory):
    __name__ = "DataPool"
    __created_mimetype__ = "visualea/datapool"

    def build_raw_instance(self):
        from openalea.secondnature.ripped.node_treeview import DataPoolModel
        from openalea.core.session import DataPool
        self.datapool = DataPool() #singleton
        # -- the other way is to get the datapool from the session --
        # session = GlobalDataManager().get_data_by_name("Session")
        # if not session:
        #     return None
        # session = session.obj
        # self.datapool = session.datapool
        self.dp_model = DataPoolModel(self.datapool)
        return self.dp_model


class DataPoolViewFactory(AbstractApplet):
    __name__ = "DataPoolView"
    __datafactories__ = [DT_DataPool]

    def create_space_content(self, data):
        from openalea.secondnature.ripped.node_treeview import DataPoolListView
        poolModel = data.obj
        widget = DataPoolListView(poolModel.datapool)
        widget.setModel(poolModel)
        return SpaceContent(widget)


# -- Dataflow and Dataflow view --
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

    def start(self):
        from openalea.visualea.graph_operator import GraphOperator
        self.__clipboard = CompositeNodeFactory("Clipboard")
        self.__siblings  = SiblingList(CompositeNode.mimetype)


    def create_space_content(self, data):
        from openalea.visualea import dataflowview
        from openalea.visualea.graph_operator import GraphOperator
        interpreter = GlobalDataManager().get_data_by_name("Interpreter")
        GraphOperator.globalInterpreter = interpreter.obj

        node = data.obj
        gwidget = dataflowview.GraphicalGraph.create_view(node, clone=True)
        menus = self.make_menus_helper(node, gwidget)
        return SpaceContent(gwidget, menuList=menus)

    def make_menus_helper(self, node, gwidget):
        from openalea.visualea.graph_operator import GraphOperator
        from openalea.vpltk.qt import QtGui

        operator = GraphOperator(graph      = node,
                                 graphScene = gwidget.scene(),
                                 clipboard  = self.__clipboard,
                                 siblings   = self.__siblings,
                                 )

        # -- Construction the Export menu
        exp_menu = QtGui.QMenu("Export")
        exp_menu.addAction(operator("To Package Manager...", exp_menu,
                                    "graph_export_to_factory"))

        # ---- to app submenu ----
        exp_toapp_menu = exp_menu.addMenu("To Application")
        exp_toapp_menu.addAction(operator("Preview...", exp_toapp_menu,
                                          "graph_preview_application"))
        exp_toapp_menu.addAction(operator("Export...", exp_toapp_menu,
                                          "graph_export_application"))

        # ---- to image submenu ----
        exp_image_menu = exp_menu.addMenu("To Image")
        exp_image_menu.addAction(operator("Raster (PNG)", exp_image_menu,
                                          "graph_export_png"))
        exp_image_menu.addAction(operator("Vector (SVG)", exp_image_menu,
                                          "graph_export_svg"))


        exp_menu.addAction(operator("To Script", exp_menu,
                                    "graph_export_script"))

        # -- Contructing the Dataflow menu --
        df_menu = QtGui.QMenu("Dataflow")
        df_menu.addAction(operator("Reload", df_menu,
                                   "graph_reload_from_factory"))
        df_menu.addSeparator()
        df_menu.addAction(operator("Run", df_menu,
                                   "graph_run"))
        df_menu.addAction(operator("Invalidate", df_menu,
                                   "graph_invalidate"))
        df_menu.addAction(operator("Reset", df_menu,
                                   "graph_reset"))
        df_menu.addAction(operator("Configure IO", df_menu,
                                   "graph_configure_io"))
        df_menu.addSeparator()
        df_menu.addAction(operator("Group", df_menu,
                                   "graph_group_selection"))
        df_menu.addAction(operator("Copy", df_menu,
                                   "graph_copy"))
        df_menu.addAction(operator("Cut", df_menu,
                                   "graph_cut"))
        df_menu.addAction(operator("Paste", df_menu,
                                   "graph_paste"))
        df_menu.addAction(operator("Delete", df_menu,
                                   "graph_remove_selection"))

        return [exp_menu, df_menu]








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
             contentmap={1:("PackageManager", "g"),
                        3:("DataflowView","a"),
                        4:("Logger", "g")},
             easy_name="Visual Programming")






