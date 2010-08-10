# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
"""QT4 Main window"""

__license__ = "CeCILL v2"
__revision__ = " $Id$ "


from PyQt4 import QtCore, QtGui, QtSvg
from PyQt4.QtCore import SIGNAL

import ui_mainwindow
from openalea.visualea.shell import get_shell_class

from openalea.core import cli
from openalea.core.pkgmanager import PackageManager
from openalea.core.settings import Settings,NoSectionError,NoOptionError
from code import InteractiveInterpreter as Interpreter

from openalea.visualea.node_treeview import NodeFactoryView, NodeFactoryTreeView, PkgModel, CategoryModel
from openalea.visualea.node_treeview import DataPoolListView, DataPoolModel
from openalea.visualea.node_treeview import SearchListView, SearchModel
from openalea.visualea.node_widget import SignalSlotListener
import metainfo
from openalea.visualea import helpwidget

from openalea.visualea.dialogs import NewGraph, NewPackage
from openalea.visualea.dialogs import PreferencesDialog, NewData

#from openalea.grapheditor import qtgraphview
from openalea.visualea import dataflowview
from graph_operator import GraphOperator

class MainWindow(QtGui.QMainWindow,
                 ui_mainwindow.Ui_MainWindow,
                 SignalSlotListener) :

    def __init__(self, session, parent=None):
        """
        @param session : user session
        @param parent : parent window
        """

        QtGui.QMainWindow.__init__(self, parent)
        SignalSlotListener.__init__(self)
        ui_mainwindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose)

        #configure GraphOperator class: TODO: make this a singleton
        GraphOperator.__main__ = self
        GraphOperator.vertexType = dataflowview.vertex.GraphicalVertex
        GraphOperator.annotationType = dataflowview.anno.GraphicalAnnotation
        GraphOperator.edgeType = dataflowview.edge.GraphicalEdge


        self.pkgmanager = session.pkgmanager

        # Set observer
        self.initialise(session)

        self.tabWorkspace.removeTab(0)
        self.tabWorkspace.setTabsClosable(True)
        self.ws_cpt = 0

        #last opened nodes
        self._last_opened = []

        # python interpreter
        interpreter = Interpreter()
        cli.init_interpreter(interpreter, session, {"tabs":self.tabWorkspace})
        shellclass = get_shell_class()
        self.interpreterWidget = shellclass(interpreter,
                                            cli.get_welcome_msg(),
                                            parent=self.splitter)

        # package tree view
        self.pkg_model = PkgModel(self.pkgmanager)
        self.packageTreeView = \
            NodeFactoryTreeView(self, self.packageview)
        self.packageTreeView.setModel(self.pkg_model)
        self.vboxlayout1.addWidget(self.packageTreeView)
        self.packageTreeView.clicked.connect(self.on_package_manager_focus_change)

        # category tree view
        self.cat_model = CategoryModel(self.pkgmanager)
        self.categoryTreeView = \
            NodeFactoryTreeView(self, self.categoryview)
        self.categoryTreeView.setModel(self.cat_model)
        self.vboxlayout2.addWidget(self.categoryTreeView)
        self.categoryTreeView.clicked.connect(self.on_package_manager_focus_change)

        # search list view
        self.search_model = SearchModel()
        self.searchListView = \
            SearchListView(self, self.searchview)
        self.searchListView.setModel(self.search_model)
        self.vboxlayout3.addWidget(self.searchListView)
        self.searchListView.clicked.connect(self.on_package_manager_focus_change)

        # data pool list view
        self.datapool_model = DataPoolModel(session.datapool)
        self.datapoolListView = \
            DataPoolListView(self, session.datapool, self.pooltab)
        self.datapoolListView.setModel(self.datapool_model)
        self.vboxlayout4.addWidget(self.datapoolListView)

        self.helpWidget = helpwidget.HelpWidget()
        self.poolTabWidget.addTab(self.helpWidget, "Help")

        # use view
      #   self.datapoolListView2 = DataPoolListView(self, session.datapool, self.usetab)
#         self.datapoolListView2.setModel(self.datapool_model)
#         self.vboxlayout5.addWidget(self.datapoolListView2)

        # Widgets
        self.connect(self.tabWorkspace, SIGNAL("contextMenuEvent(QContextMenuEvent)"),
                     self.contextMenuEvent)
        self.tabWorkspace.currentChanged.connect( self.ws_changed)
        self.search_lineEdit.editingFinished.connect( self.search_node)
        self.tabWorkspace.tabCloseRequested.connect( self.close_tab_workspace)


        # Help Menu
        self.action_About.triggered.connect( self.about)
        self.actionOpenAlea_Web.triggered.connect( self.web)
        self.action_Help.triggered.connect( self.help)

        # File Menu
        self.action_New_Session.triggered.connect( self.new_session)
        self.action_Open_Session.triggered.connect( self.open_session)
        self.action_Save_Session.triggered.connect( self.save_session)
        self.actionSave_as.triggered.connect( self.save_as)
        self.action_Quit.triggered.connect( self.quit)

        self.action_Image.triggered.connect( self.export_image)
        self.action_Svg.triggered.connect( self.export_image_svg)

        # Package Manager Menu
        self.action_Auto_Search.triggered.connect( self.reload_all)
        self.action_Add_File.triggered.connect( self.add_pkgdir)
        self.actionFind_Node.triggered.connect( self.find_node)
        self.action_New_Network.triggered.connect( self.new_graph)
        self.actionNew_Python_Node.triggered.connect( self.new_python_node)
        self.actionNew_Package.triggered.connect( self.new_package)
        self.action_Data_File.triggered.connect( self.new_data)
        self.actionShow_log.triggered.connect( self.pkgmanager.log.print_log)

        # DataPool Menu
        self.actionClear_Data_Pool.triggered.connect( self.clear_data_pool)

        # Python Menu
        self.action_Execute_script.triggered.connect(
                     self.exec_python_script)
        self.actionOpen_Console.triggered.connect(
                     self.open_python_console)
        self.actionClea_r_Console.triggered.connect(
                     self.clear_python_console)

        # WorkspaceMenu
        self._last_open_action_group = QtGui.QActionGroup(self)
        self.connect(self._last_open_action_group,
                     SIGNAL("triggered(QAction*)"),
                     self.reopen_last)
        # daniel was here: now the menu is built using the graph operator.
        self.operator = GraphOperator()
        # self.operator.set_main(self)
        # self.operator.vertexType = dataflowview.vertex.GraphicalVertex
        # self.operator.annotationType = dataflowview.anno.GraphicalAnnotation
        # self.operator.edgeType = dataflowview.edge.GraphicalEdge
        self.operator.register_listener(self)
        self.menu_Workspace.aboutToShow.connect(self.__wsMenuShow)
        self.action_New_Empty_Workspace.triggered.connect(self.new_workspace)
        self.operator + (self.action_Run, "graph_run")
        self.operator + (self.actionInvalidate, "graph_invalidate")
        self.operator + (self.actionReset, "graph_reset")
        self.operator + (self.actionConfigure_I_O, "graph_configure_io")
        self.operator + (self.actionGroup_Selection, "graph_group_selection")
        self.operator + (self.action_Copy, "graph_copy")
        self.operator + (self.action_Paste, "graph_paste")
        self.operator + (self.action_Cut, "graph_cut")
        self.operator + (self.action_Delete_2, "graph_remove_selection")
        self.operator + (self.action_Close_current_workspace, "graph_close")
        self.operator + (self.action_Export_to_Factory, "graph_export_to_factory")
        self.operator + (self.actionReload_from_Model, "graph_reload_from_factory")
        self.operator + (self.actionExport_to_Application, "graph_export_application")
        self.operator + (self.actionPreview_Application, "graph_preview_application")
        self.operator + (self.actionAlignHorizontally, "graph_align_selection_horizontal")
        self.operator + (self.actionAlignLeft, "graph_align_selection_left")
        self.operator + (self.actionAlignRight, "graph_align_selection_right")
        self.operator + (self.actionAlignMean, "graph_align_selection_mean")
        self.operator + (self.actionDistributeHorizontally, "graph_distribute_selection_horizontally")
        self.operator + (self.actionDistributeVertically, "graph_distribute_selection_vertically")
        self.operator + (self.actionSetCustomColor, "graph_set_selection_color")
        self.operator + (self.actionUseCustomColor, "graph_use_user_color")

        self.actionTo_script.triggered.connect(self.to_python_script)

        # Window Mneu
        self.actionPreferences.triggered.connect(self.open_preferences)
        self.actionDisplay_Package_Manager.toggled.connect(self.display_leftpanel)
        self.actionDisplay_Workspaces.toggled.connect(self.display_rightpanel)

        # action = self.menu_Workspace.addAction("DEBUG")
        # self.connect(action, SIGNAL("triggered()"), self.debug)

        # final init
        self.session = session
        self.session.simulate_workspace_addition()
        #load personnal GUI settings
        self.read_settings()

    def debug (self) :
        v = self.packageTreeView
        print "items",v.expanded_items
        print "model",v.model()
        print "map",v.model().index_map

    def write_settings (self) :
        """Save application settings.
        """
        settings = Settings()

        #main window
        settings.set("MainWindow","size","(%d,%d)" % (self.width(),self.height() ) )
        settings.set("MainWindow","pos","(%d,%d)" % (self.x(),self.y() ) )

        sizes = "[%s]" % ",".join("%d" % val for val in self.splitter_2.sizes() )
        settings.set("MainWindow","splitter_2",sizes)
        sizes = "[%s]" % ",".join("%d" % val for val in self.splitter_3.sizes() )
        settings.set("MainWindow","splitter_3",sizes)

        #tree view
        settings.set("TreeView","open","[]")

        #workspace
        last_open = "[%s]" % ",".join("'%s'" % item for item in self._last_opened)
        settings.set("WorkSpace","last",last_open)

        settings.write_to_disk()

    def read_settings (self) :
        """Read application settings.
        """
        settings = Settings()

        #main window
        try :
            size = eval(settings.get("MainWindow","size") )
            self.resize(QtCore.QSize(*size) )
        except NoSectionError :
            pass
        except NoOptionError :
            pass
        try :
            pos = eval(settings.get("MainWindow","pos") )
            self.move(QtCore.QPoint(*pos) )
        except NoSectionError :
            pass
        except NoOptionError :
            pass
        try :
            sizes = eval(settings.get("MainWindow","splitter_2") )
            self.splitter_2.setSizes(sizes)
        except NoSectionError :
            pass
        except NoOptionError :
            pass
        try :
            sizes = eval(settings.get("MainWindow","splitter_3") )
            self.splitter_3.setSizes(sizes)
        except NoSectionError :
            pass
        except NoOptionError :
            pass
        #workspace
        try :
            last_open = eval(settings.get("WorkSpace","last") )
            last_open.reverse()
            for item in last_open :
                gr = item.split(".")
                pkgid = ".".join(gr[:-1])
                name = gr[-1]
                self.add_last_open(pkgid,name)
        except NoSectionError :
            pass
        except NoOptionError :
            pass

    def redo_last_open_menu (self) :
        """Create entries for last opened nodes.
        """
        self.menuLast_open.clear()
        for action in self._last_open_action_group.actions() :
            self._last_open_action_group.removeAction(action)

        for i,node_descr in enumerate(self._last_opened) :
            action = self.menuLast_open.addAction(node_descr)
            action.setShortcut("Ctrl+%d" % (i + 1) )
            self._last_open_action_group.addAction(action)

        self.menuLast_open.setEnabled(len(self._last_opened) > 0)

    def reopen_last (self, action) :
        """Reopen a last open node.
        """
        gr = str(action.text() ).split(".")
        pkgid = ".".join(gr[:-1])
        name = gr[-1]
        manager = PackageManager()
        factory = manager[pkgid][name]
        self.open_compositenode(factory)

    def add_last_open (self, pkgid, factory_name) :
        """Register a new lest opened node.
        """
        key = ".".join([pkgid,factory_name])
        try :
            self._last_opened.remove(key)
        except ValueError :
            pass

        self._last_opened.insert(0,key)
        if len(self._last_opened) > 4 :
            del self._last_opened[-1]

        self.redo_last_open_menu()

    def __wsMenuShow(self):
        widget = self.tabWorkspace.currentWidget()
        if widget is None:
            return

        #check if the current selection is coloured and tick the
        #menu item if an item of the selection uses the user color.
        items = widget.scene().get_selected_items(dataflowview.vertex.GraphicalVertex)
        self.actionUseCustomColor.setChecked(False)
        for i in items:
            if i.vertex().get_ad_hoc_dict().get_metadata("useUserColor"):
                self.actionUseCustomColor.setChecked(True)
                break

    def open_compositenode(self, factory):
        """ open a  composite node editor """
        node = factory.instantiate()

        self.session.add_workspace(node, notify=False)
        self.open_widget_tab(node, factory=factory)

        self.add_last_open(factory.__pkg_id__,factory.name)


    def about(self):
        """ Display About Dialog """

        mess = QtGui.QMessageBox.about(self, "About Visualea",
                                       "Version %s\n\n"%(metainfo.get_version()) +
                                       "VisuAlea is part of the OpenAlea framework.\n"+
                                       metainfo.get_copyrigth()+
                                       "This Software is distributed under the Cecill-V2 License.\n\n"+
                                       "Visit " + metainfo.url +"\n\n"
                                       )

    def help(self):
        """ Display help """
        self.web()

    def web(self):
        """ Open OpenAlea website """
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(metainfo.url))


    def quit(self):
        """ Quit Application """
        if( QtGui.QMessageBox.question(self, "Quit?", "Are you sure you want to quit?",
                                       QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel) ==
                        QtGui.QMessageBox.Ok):
            QtGui.QApplication.exit(0)

    def notify(self, sender, event):
        """ Notification from observed """
        if event and sender == self.operator :
            index = self.tabWorkspace.indexOf(event[1])
            if(event[0] == "graphoperator_graphsaved"):
                if index > -1:
                    self.reinit_treeview()
                    caption = "Workspace %i - %s"%(index, event[2].name)
                    self.tabWorkspace.setTabText(index, caption)
            elif(event[0] == "graphoperator_graphclosed"):
                if index > -1:
                    self.close_tab_workspace(index)
            elif(event[0] == "graphoperator_graphreloaded"):
                if index > -1:
                    self.session.workspaces[index] = event[2]

        if(type(sender) == type(self.session)):
            if(event and event[0]=="workspace_added"):
                graph=event[1]
                self.open_widget_tab(graph, graph.factory)
            else:
                self.update_tabwidget()
                self.reinit_treeview()

    def closeEvent(self, event):
        """ Close All subwindows """

        #Save personnal settings
        self.write_settings()

        #close windows
        for i in range(self.tabWorkspace.count()):
            w = self.tabWorkspace.widget(i)
            w.close()

        event.accept()


    def reinit_treeview(self):
        """ Reinitialise package and category views """
        self.cat_model.reset()
        self.pkg_model.reset()
        self.datapool_model.reset()
        self.search_model.reset()


    def close_tab_workspace(self, cindex):
        """ Close workspace indexed by cindex cindex is Node"""
        w = self.tabWorkspace.widget(cindex)
        self.tabWorkspace.removeTab(cindex)
        self.session.close_workspace(cindex, False)
        w.close()
        del w

    def current_view (self) :
        """ Return the active widget """
        return self.tabWorkspace.currentWidget()

    def update_tabwidget(self):
        """ open tab widget """
        # open tab widgets
        for (i, node) in enumerate(self.session.workspaces):

            if(i< self.tabWorkspace.count()):
                widget = self.tabWorkspace.widget(i)
                if(node != widget.scene().get_graph()):
                    self.close_tab_workspace(i)
                self.open_widget_tab(node, factory=node.factory, pos = i)

        # close last tabs
        removelist = range( len(self.session.workspaces), self.tabWorkspace.count())
        removelist.reverse()
        for i in removelist:
            self.close_tab_workspace(i)

    def open_widget_tab(self, graph, factory, caption=None, pos = -1):
        """
        Open a widget in a tab giving an instance and its widget
        caption is append to the tab title
        """
        # Test if the node is already opened
        for i in range(self.tabWorkspace.count()):
            widget = self.tabWorkspace.widget(i)
            other = widget.scene().get_graph()
            if other:
                if(graph is other):
                    self.tabWorkspace.setCurrentIndex(i)
                    return

        #gengraph
        gwidget = None
        try:
            gwidget = dataflowview.GraphicalGraph.create_view(graph, parent=self)
            gwidget.scene().focusedItemChanged.connect(self.on_scene_focus_change)
            self.session.add_graph_view(gwidget)
        except Exception, e:
            print "open_widget_tab", e
            return
        #/gengraph

        if(not caption) :
            i = self.session.workspaces.index(graph)
            caption = "Workspace %i - %s"%(i, graph.get_caption())

        index = self.tabWorkspace.insertTab(pos, gwidget, caption)
        self.tabWorkspace.setCurrentIndex(index)
        #there is a bug in QGraphicsScene+QTabWidget that makes
        #secondary tabs inactive, so we force them to be active
        #by sending new views the QEvent.WindowActivate event.
        #The bug is present until Qt4.6.2 at least. Bugreport:
        #http://bugreports.qt.nokia.com/browse/QTBUG-11148
        QtCore.QCoreApplication.instance().notify(gwidget, QtCore.QEvent(QtCore.QEvent.WindowActivate))
        if gwidget is not None :
            gwidget.show_entire_scene()

        return index


    def add_pkgdir(self):

        dirname = QtGui.QFileDialog.getExistingDirectory(self, "Select Package/Directory")
        if(dirname):
            self.pkgmanager.load_directory(str(dirname))
            self.reinit_treeview()


    def reload_all(self):

        # Reload package manager
        self.pkgmanager.reload()
        self.reinit_treeview()

        # Reload workspace
        print "WARNING TODO RELOAD EACH TAB"
        #for index in range(len(self.index_nodewidget)):
        #    self.reload_from_factory(index)

    def ws_changed(self, index):
        """ Current workspace has changed """
        self.session.cworkspace = index


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        pos = self.tabWorkspace.mapFromGlobal(event.globalPos())

        tabBar = self.tabWorkspace.tabBar()
        count = tabBar.count()

        index = -1
        for i in range(count):
            if(tabBar.tabRect(i).contains(pos)):
                index = i
                break

        # if no bar was hit, return
        if (index<0):
            return

        # set hit bar to front
        self.tabWorkspace.setCurrentIndex(index)

        def close_current_ws():
            self.close_tab_workspace(index)

        menu = QtGui.QMenu(self)

        action = menu.addAction("Close")
        self.connect(action, SIGNAL("triggered()"), close_current_ws)

#         action = menu.addAction("Run")
#         self.connect(action, SIGNAL("triggered()"), self.run)

#         action = menu.addAction("Export to Model")
#         self.connect(action, SIGNAL("triggered()"), self.export_to_factory)

        menu.move(event.globalPos())
        menu.show()

    def new_workspace(self):
        """ Create an empty workspace """
        self.session.add_workspace()

    def new_graph(self):
        """ Create a new graph """

        dialog = NewGraph("New Composite Node", self.pkgmanager, self)
        ret = dialog.exec_()

        if(ret>0):
            newfactory = dialog.create_cnfactory(self.pkgmanager)
            self.reinit_treeview()
            self.open_compositenode(newfactory)

    def new_python_node(self):
        """ Create a new node """

        dialog = NewGraph("New Python Node", self.pkgmanager, self)
        ret = dialog.exec_()

        if(ret>0):
            dialog.create_nodefactory(self.pkgmanager)
            self.reinit_treeview()

    def new_data(self):
        """ Import file """

        dialog = NewData("Import data file", self.pkgmanager, self)
        ret = dialog.exec_()

        if(ret>0):
            dialog.create_datafactory(self.pkgmanager)
            self.reinit_treeview()

    def new_package(self):
        """ Create a new user package """

        dialog = NewPackage(self.pkgmanager.keys(), parent = self)
        ret = dialog.exec_()

        if(ret>0):
            (name, metainfo, path) = dialog.get_data()

            self.pkgmanager.create_user_package(name, metainfo, path)
            self.reinit_treeview()

    def exec_python_script(self):
        """ Choose a python source and execute it """

        filename = QtGui.QFileDialog.getOpenFileName(
            self, "Python Script", "Python script (*.py)")

        filename = str(filename)
        if(not filename) : return

        import code
        file = open(filename, 'r')

        sources = ''
        compiled = None

        for line in file:
            sources += line
            compiled = code.compile_command(sources, filename)

            if(compiled):
                self.interpreterWidget.get_interpreter().runcode(compiled)
                sources = ''

    def open_python_console(self):
        """ Set focus on the python shell """
        self.interpreterWidget.setFocus(QtCore.Qt.ShortcutFocusReason)

    def clear_python_console(self):
        """ Clear python shell """
        self.interpreterWidget.clear()

    def new_session(self):
        self.session.clear()

    def open_session(self):

        filename = QtGui.QFileDialog.getOpenFileName(
            self, "OpenAlea Session", QtCore.QDir.homePath(), "Session file (*.oas)")

        filename = str(filename)
        if(not filename) : return

        self.session.load(filename)

    def save_session(self):
        """ Save menu entry """

        if(not self.session.session_filename):
            self.save_as()
        else :
            self.session.save(self.session.session_filename)

    def save_as(self):
        """ Save as menu entry """

        filename = QtGui.QFileDialog.getSaveFileName(
            self, "OpenAlea Session",  QtCore.QDir.homePath(), "Session file (*.oas)")

        filename = str(filename)
        if(not filename) : return

        self.session.save(filename)

    def clear_data_pool(self):
        """ Clear the data pool """

        self.session.datapool.clear()

    def search_node(self):
        """ Activated when search line edit is validated """

        results = self.pkgmanager.search_node(str(self.search_lineEdit.text()))
        self.search_model.set_results(results)

    def find_node(self):
        """ Find node Command """

        i = self.tabPackager.indexOf(self.searchview)
        self.tabPackager.setCurrentIndex(i)
        self.search_lineEdit.setFocus()

    def open_preferences(self):
        """ Open Preference dialog """

        dialog = PreferencesDialog(self)
        ret = dialog.exec_()
        # ! does not return anythin and do not use ret ?

    # Drag and drop support
    def dragEnterEvent(self, event):
        """todo"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """todo"""
        urls = event.mimeData().urls()
        try:
            file = urls[0]
            filename = str(file.path())
            self.session.load(filename)
            event.accept()

        except Exception, e:
            print e
            event.ignore()


    ############################
    # Handling the Help widget #
    ############################
    def on_scene_focus_change(self, scene, item):
        assert isinstance(item, dataflowview.vertex.GraphicalVertex)
        self.helpWidget.set_rst(item.vertex().get_tip())

    def on_package_manager_focus_change(self, item):
        pkg_id, factory_id, mimetype = NodeFactoryView.get_item_info(item)
        if len(pkg_id) and len(factory_id) and mimetype=="openalea/nodefactory":
            factory = self.pkgmanager[pkg_id][factory_id]
            factoryDoc = factory.get_documentation()
            txt = factory.get_tip(asRst=True) + "\n\n"
            if factoryDoc is not None:
                txt += "**Docstring:**\n" + factoryDoc
            self.helpWidget.set_rst(txt)

    # Window support
    def display_leftpanel(self, toggled):
        self.splitter_2.setVisible(toggled)


    def display_rightpanel(self, toggled):
        self.splitter.setVisible(toggled)

    def to_python_script(self):
        """Translate the active workspace into a python script"""

        widget = self.tabWorkspace.currentWidget()
        if widget is None:
            return

        composite_node = widget.scene().get_graph()
        if composite_node is not None :
            print "BEGIN script"
            print composite_node.to_script(),"END script"

    def export_image(self):
        """ Export current workspace to an image """

        filename = QtGui.QFileDialog.getSaveFileName(
            self, "Export image",  QtCore.QDir.homePath(), "PNG Image (*.png)")

        filename = str(filename)
        if not filename:
            return
        elif '.' not in filename:
            filename += '.png'

        # Get current workspace
        view = self.tabWorkspace.currentWidget()
        # Retreive the user layout
        rect = view.scene().sceneRect()
        matrix = view.matrix()
        rect = matrix.mapRect(rect)

        pixmap = QtGui.QPixmap(rect.width(), rect.height())
        pixmap.fill()
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        view.update()
        view.scene().render(painter)
        painter.end()
        pixmap.save(filename)

    def export_image_svg(self):
        """ Export current workspace to an image """

        filename = QtGui.QFileDialog.getSaveFileName(
            self, "Export svg image",  QtCore.QDir.homePath(), "SVG Image (*.svg)")

        filename = str(filename)
        if not filename:
            return
        elif '.' not in filename:
            filename += '.png'

        # Get current workspace
        view = self.tabWorkspace.currentWidget()

        # Retreive the user layout
        rect = view.scene().sceneRect()
        matrix = view.matrix()
        rect = matrix.mapRect(rect)

        svg_gen = QtSvg.QSvgGenerator()
        svg_gen.setFileName(filename)
        svg_gen.setSize(rect.toRect().size())

        painter = QtGui.QPainter(svg_gen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        view.scene().render(painter, )
        painter.end()

