# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
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

__doc__="""
QT4 Main window 
"""

__license__= "CeCILL v2"
__revision__=" $Id$ "


from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL

import ui_mainwindow
from shell import get_shell_class

from openalea.core import cli
from code import InteractiveInterpreter as Interpreter

from node_treeview import NodeFactoryTreeView, PkgModel, CategoryModel
from node_treeview import DataPoolListView, DataPoolModel
from node_treeview import SearchListView, SearchModel

import metainfo

from openalea.core.observer import AbstractListener

from dialogs import NewGraph, NewPackage, FactorySelector, IOConfigDialog, PreferencesDialog

from util import exception_display, busy_pointer



class MainWindow(QtGui.QMainWindow,
                 ui_mainwindow.Ui_MainWindow,
                 AbstractListener) :

    def __init__(self, session, parent=None):
        """
        @param pkgman : the package manager
        @param session : user session
        @param parent : parent window
        """

        QtGui.QMainWindow.__init__(self, parent)
        AbstractListener.__init__(self)
        ui_mainwindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.pkgmanager = session.pkgmanager

        # Set observer
        self.initialise(session)

        # Array to map tab index with node widget
        self.index_nodewidget = []

        self.tabWorkspace.removeTab(0)
        self.ws_cpt = 0

        # python interpreter
        interpreter = Interpreter()
        cli.init_interpreter(interpreter, session)
        shellclass = get_shell_class()
        self.interpreterWidget = shellclass(interpreter,
                                            cli.get_welcome_msg(),
                                            parent=self.splitter)

        # package tree view
        self.pkg_model = PkgModel(self.pkgmanager)
        self.packageTreeView = NodeFactoryTreeView(self, self.packageview)
        self.packageTreeView.setModel(self.pkg_model)
        self.vboxlayout.addWidget(self.packageTreeView)

        # category tree view
        self.cat_model = CategoryModel(self.pkgmanager)
        self.categoryTreeView = NodeFactoryTreeView(self, self.categoryview)
        self.categoryTreeView.setModel(self.cat_model)
        self.vboxlayout1.addWidget(self.categoryTreeView)

        # search list view
        self.search_model = SearchModel()
        self.searchListView = SearchListView(self, self.searchview)
        self.searchListView.setModel(self.search_model)
        self.vboxlayout2.addWidget(self.searchListView)


        # data pool list view
        self.datapool_model = DataPoolModel(session.datapool)
        self.datapoolListView = DataPoolListView(self, session.datapool, self.pooltab)
        self.datapoolListView.setModel(self.datapool_model)
        self.vboxlayout3.addWidget(self.datapoolListView)

        # use view
        self.datapoolListView2 = DataPoolListView(self, session.datapool, self.usetab)
        self.datapoolListView2.setModel(self.datapool_model)
        self.vboxlayout5.addWidget(self.datapoolListView2)

        # Widgets
        self.connect(self.tabWorkspace, SIGNAL("contextMenuEvent(QContextMenuEvent)"),
                     self.contextMenuEvent)
        self.connect(self.search_lineEdit, SIGNAL("editingFinished()"), self.search_node)


        # Help Menu
        self.connect(self.action_About, SIGNAL("activated()"), self.about)
        self.connect(self.actionOpenAlea_Web, SIGNAL("activated()"), self.web)
        self.connect(self.action_Help, SIGNAL("activated()"), self.help)
        self.connect(self.actionPreferences, SIGNAL("activated()"), self.open_preferences)


        # File Menu
        self.connect(self.action_New_Session, SIGNAL("activated()"), self.new_session)
        self.connect(self.action_Open_Session, SIGNAL("activated()"), self.open_session)
        self.connect(self.action_Save_Session, SIGNAL("activated()"), self.save_session)
        self.connect(self.actionSave_as, SIGNAL("activated()"), self.save_as)
        self.connect(self.action_Quit, SIGNAL("activated()"), self.quit)

        # Package Manager Menu
        self.connect(self.action_Auto_Search, SIGNAL("activated()"), self.find_wralea)
        self.connect(self.action_Add_File, SIGNAL("activated()"), self.add_wralea)
        self.connect(self.actionFind_Node, SIGNAL("activated()"),
                     self.find_node)
        self.connect(self.action_New_Network, SIGNAL("activated()"), self.new_graph)
        self.connect(self.actionNew_Python_Node, SIGNAL("activated()"), self.new_python_node)
        self.connect(self.actionNew_Package, SIGNAL("activated()"), self.new_package)

        # DataPool Menu
        self.connect(self.actionClear_Data_Pool, SIGNAL("activated()"), self.clear_data_pool)

        # Python Menu
        self.connect(self.action_Execute_script, SIGNAL("activated()"),
                     self.exec_python_script)
        self.connect(self.actionOpen_Console, SIGNAL("activated()"),
                     self.open_python_console)
        # WorkspaceMenu
        self.connect(self.action_Run, SIGNAL("activated()"), self.run)
        self.connect(self.actionReset, SIGNAL("activated()"), self.reset)
        
        self.connect(self.action_Copy, SIGNAL("activated()"), self.copy)
        self.connect(self.action_Paste, SIGNAL("activated()"), self.paste)
        self.connect(self.action_Cut, SIGNAL("activated()"), self.cut)
        
        self.connect(self.action_Delete_2, SIGNAL("activated()"), self.delete_selection)
        self.connect(self.actionGroup_Selection, SIGNAL("activated()"), self.group_selection)
        self.connect(self.action_New_Empty_Workspace, SIGNAL("activated()"), self.new_workspace)
        self.connect(self.action_Close_current_workspace, SIGNAL("activated()"),
                     self.close_workspace)
        self.connect(self.actionConfigure_I_O, SIGNAL("activated()"),
                     self.configure_io)
        self.connect(self.actionReload_from_Model, SIGNAL("activated()"), self.reload_from_factory)
        self.connect(self.action_Export_to_Factory, SIGNAL("activated()"), self.export_to_factory)
        self.connect(self.actionExport_to_Application, SIGNAL("activated()"),
                     self.export_to_application)
        self.connect(self.actionPreview_Application, SIGNAL("activated()"),
                     self.preview_application)

        
        self.setAcceptDrops(True)
        # final init
        self.session = session
        session.notify_listeners()
        
        

    def open_compositenode(self, factory):
        """ open a  composite node editor """
        node = factory.instantiate()

        self.session.add_workspace(node, notify=False)
        self.open_widget_tab(node, factory=factory)


    def about(self):
        """ Display About Dialog """
        
        mess = QtGui.QMessageBox.about(self, "About Visualea",
                                       "Version %s\n\n"%(metainfo.version) +
                                       "VisuAlea is part of the OpenAlea framework.\n"+
                                       u"Copyright \xa9  2006-2007 INRIA - CIRAD - INRA\n"+
                                       "This Software is distributed under the Cecill-V2 License.\n\n"+
                                       
                                       "Visit http://openalea.gforge.inria.fr\n\n"
                                       )

    def help(self):
        """ Display help """
        self.web()

    def web(self):
        """ Open OpenAlea website """
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(metainfo.url))


    def quit(self):
        """ Quit Application """

        self.close()


    def notify(self, sender, event):
        """ Notification from observed """

        if(type(sender) == type(self.session)):
            self.update_tabwidget()
            self.reinit_treeview()

    
    def closeEvent(self, event):
        """ Close All subwindows """
        
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
        

    def close_workspace(self):
        """ Close current workspace """

        cindex = self.tabWorkspace.currentIndex()

        # Try to save factory if widget is a graph
        try:
            w = self.index_nodewidget[cindex]
            modified = w.node.graph_modified
            if(modified):
                # Generate factory if user want
                ret = QtGui.QMessageBox.question(self, "Close Workspace",
                                                 "Graph has been modified.\n"+
                                                 "Do you want to report modification "+
                                                 "in the model ?\n",
                                                 QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,)
            
                if(ret == QtGui.QMessageBox.Yes):
                    self.export_to_factory(cindex, False)

        except Exception, e:
            pass

        # Update session
        node = self.index_nodewidget[cindex].node
        self.session.close_workspace(cindex, False)
        self.close_tab_workspace(cindex)
            

    def close_tab_workspace(self, cindex):
        """ Close workspace indexed by cindex cindex is Node"""
        
        w = self.tabWorkspace.widget(cindex)
        self.tabWorkspace.removeTab(cindex)
        w.close()
        w.emit(QtCore.SIGNAL("close()"))
        
        del(self.index_nodewidget[cindex])

      
    def current_view (self) :
        """ Return the active widget """
        cindex = self.tabWorkspace.currentIndex()
        return self.index_nodewidget[cindex]

    
    def update_tabwidget(self):
        """ open tab widget """

        # open tab widgets
        for (i, node) in enumerate(self.session.workspaces):

            if(i<len(self.index_nodewidget)):
                widget = self.index_nodewidget[i]
                if(node != widget.node):
                    self.close_tab_workspace(i)
            self.open_widget_tab(node, factory=node.factory, pos = i)

            
        # close last tabs
        removelist = range( len(self.session.workspaces),
                        len(self.index_nodewidget))
        removelist.reverse()
        for i in removelist:
            self.close_tab_workspace(i)


    def open_widget_tab(self, node, factory, caption=None, pos = -1):
        """
        Open a widget in a tab giving an instance and its widget
        caption is append to the tab title
        """

                # Test if the node is already opened
        for i in range(len(self.index_nodewidget)):
            widget = self.index_nodewidget[i]
            n = widget.node
            if(node is n):
                self.tabWorkspace.setCurrentIndex(i)
                return

        container = QtGui.QWidget(self)
        container.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        widget = factory.instantiate_widget(node, parent=container, edit=True)
        widget.wcaption = caption
        widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        vboxlayout = QtGui.QVBoxLayout(container)
        vboxlayout.addWidget(widget)

        if(not caption) :
            i = self.session.workspaces.index(node)
            caption = "Workspace %i - %s"%(i, node.get_caption())
        
        index = self.tabWorkspace.insertTab(pos, container, caption)
        self.tabWorkspace.setCurrentIndex(index)
        self.index_nodewidget.append(widget)

        return index
        

    def add_wralea(self):

        filename = QtGui.QFileDialog.getOpenFileName(self, "Add Wralea")
        if(filename):
            self.pkgmanager.add_wralea(str(filename))
            self.reinit_treeview()

    
    def find_wralea(self):

        self.pkgmanager.find_and_register_packages()
        self.reinit_treeview()


    @exception_display
    @busy_pointer
    def run(self):
        """ Run the active workspace """

        cindex = self.tabWorkspace.currentIndex()
        self.index_nodewidget[cindex].node.eval()


    def reload_from_factory(self, index=-1):
        """ Reload a tab node givin its index"""

        if(index<0): index = self.tabWorkspace.currentIndex()

        widget = self.index_nodewidget[index]
        newnode = widget.node.factory.instantiate()
        widget.node = newnode
        self.session.workspaces[index] = newnode


    def group_selection(self):
        """ Replace selected nodes with a composite node """

        index = self.tabWorkspace.currentIndex()
        widget = self.index_nodewidget[index]

        if(not widget.get_selected_item()) : return

        # Create a new factory
        dialog = NewGraph("New Composite Node", self.pkgmanager, self)
        ret = dialog.exec_()

        if(not ret): return
        
        factory = dialog.create_cnfactory(self.pkgmanager)
        f = widget.group_selection(factory)

        try:
            factory.package.write()
        except AttributeError, e:
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "Cannot write Graph model on disk. :\n"+
                                             "You try to write in a System Package:\n")
        

    def export_to_factory(self, index=-1):
        """
        Export workspace index to its factory
        """

        if(index < 0): index = self.tabWorkspace.currentIndex()
        widget = self.index_nodewidget[index]

        # Get a composite node factory
        dialog = FactorySelector(widget.node.factory, self)
            
        # Display Dialog
        ret = dialog.exec_()
        if(ret == 0): return None
        factory = dialog.get_factory()

        widget.node.to_factory(factory, None)

        try:
            factory.package.write()

        except AttributeError, e:
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "Cannot write Graph model on disk. :\n"+
                                             "You try to write in a System Package:\n")
        

    def configure_io(self, index=-1):
        """ Configure workspace IO """

        if(index < 0): index = self.tabWorkspace.currentIndex()
        widget = self.index_nodewidget[index]

        dialog = IOConfigDialog(widget.node.input_desc,
                                widget.node.output_desc,
                                parent=self)
        ret = dialog.exec_()

        if(ret):
            widget.node.set_io(dialog.inputs, dialog.outputs)
            widget.rebuild_scene()
        

            
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
        if (index<0) :  return 

        # set hitted bar to front
        self.tabWorkspace.setCurrentIndex(index)
        
        menu = QtGui.QMenu(self)

        action = menu.addAction("Close")
        self.connect(action, SIGNAL("activated()"), self.close_workspace)

#         action = menu.addAction("Run")
#         self.connect(action, SIGNAL("activated()"), self.run)

#         action = menu.addAction("Export to Model")
#         self.connect(action, SIGNAL("activated()"), self.export_to_factory)

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
        """ Open an independant window with a python console """

        self.interpreterWidget.setFocus(QtCore.Qt.ShortcutFocusReason)
        

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


    def delete_selection(self):
        """ Delete selection in current workspace """
        cindex = self.tabWorkspace.currentIndex()
        widget = self.index_nodewidget[cindex]

        try:
            widget.remove_selection()
        except AttributeError:
            pass


    def copy(self):
        """ Copy """

        if(self.interpreterWidget.hasFocus()):
            try:
                self.interpreterWidget.copy()
            except:
                pass
        else:
            cindex = self.tabWorkspace.currentIndex()
            widget = self.index_nodewidget[cindex]

            try:
                widget.copy(self.session)
            except AttributeError:
                pass


    def paste(self):
        """ Paste """

        if(self.interpreterWidget.hasFocus()):
            try:
                self.interpreterWidget.paste()
            except:
                pass
        else:
            cindex = self.tabWorkspace.currentIndex()
            widget = self.index_nodewidget[cindex]
            
            try:
                widget.paste(self.session)
            except AttributeError:
                pass


    def cut(self):
        """ Cut """
        if(self.interpreterWidget.hasFocus()):
            try:
                self.interpreterWidget.cut()
            except:
                pass
        else:
            cindex = self.tabWorkspace.currentIndex()
            widget = self.index_nodewidget[cindex]
            
            try:
                widget.copy(self.session)
                widget.remove_selection()
            except AttributeError:
                pass


    def open_preferences(self):
        """ Open Preference dialog """

        dialog = PreferencesDialog(self)
        ret = dialog.exec_()


    def reset(self):
        """ Reset current workspace """

        cindex = self.tabWorkspace.currentIndex()
        self.index_nodewidget[cindex].node.reset()



    def get_current_factory(self, name):
        """ Build a temporary factory for current workspace
        Return (node, factory)
        """

        cindex = self.tabWorkspace.currentIndex()
        node = self.index_nodewidget[cindex].node

        # Export as temporary factory
        from openalea.core.compositenode import CompositeNodeFactory
        tempfactory = CompositeNodeFactory(name = name)
        node.to_factory(tempfactory)

        return (node, tempfactory)
    
        
    def preview_application(self):
        """ Open Application widget """

        (node, tempfactory) = self.get_current_factory("Preview")
        w = tempfactory.instantiate_widget(node, self)

        from util import open_dialog
        open_dialog(self, w, 'Preview Application')


    def export_to_application(self):
        """ Export current workspace composite node to an Application """

        # Get Filename
        filename = QtGui.QFileDialog.getSaveFileName(
            self, "Python Application", QtCore.QDir.homePath(), "Python file (*.py)")
        
        filename = str(filename)
        if(not filename) : return

        # Get Application Name
        (result, ok) = QtGui.QInputDialog.getText(self, "Application Name", "",
                                   QtGui.QLineEdit.Normal, "")
        if(not ok): return

        name = str(result)
        if(not name) : name = "OpenAlea Application"
        
        (node, tempfactory) = self.get_current_factory(name)
        w = tempfactory.instantiate_widget(node, self)

        from openalea.core import export_app
        export_app.export_app(name, filename, tempfactory)
        

    # Drag and drop support 
    def dragEnterEvent(self, event):
        
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):

        urls = event.mimeData().urls()
        try:
            file = urls[0]
            filename = str(file.path())
            self.session.load(filename)
            event.accept()

        except Exception, e:
            print e
            event.ignore()

            


