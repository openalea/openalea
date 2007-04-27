# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
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

from dialogs import NewGraph, NewPackage, FactorySelector



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


        # menu callbacks
        self.connect(self.action_About, SIGNAL("activated()"), self.about)
        self.connect(self.actionOpenAlea_Web, SIGNAL("activated()"), self.web)
        self.connect(self.action_Help, SIGNAL("activated()"), self.help)
        self.connect(self.action_Quit, SIGNAL("activated()"), self.quit)
        self.connect(self.action_Close_current_workspace, SIGNAL("activated()"),
                     self.close_workspace)
        self.connect(self.action_Auto_Search, SIGNAL("activated()"), self.find_wralea)
        self.connect(self.action_Add_File, SIGNAL("activated()"), self.add_wralea)
        self.connect(self.action_Run, SIGNAL("activated()"), self.run)
        self.connect(self.tabWorkspace, SIGNAL("contextMenuEvent(QContextMenuEvent)"),
                     self.contextMenuEvent)
        self.connect(self.action_Execute_script, SIGNAL("activated()"),
                     self.exec_python_script)
        self.connect(self.actionFind_Node, SIGNAL("activated()"),
                     self.find_node)

        self.connect(self.action_New_Session, SIGNAL("activated()"), self.new_session)
        self.connect(self.action_Open_Session, SIGNAL("activated()"), self.open_session)
        self.connect(self.action_Save_Session, SIGNAL("activated()"), self.save_session)
        self.connect(self.actionSave_as, SIGNAL("activated()"), self.save_as)

        self.connect(self.action_Export_to_Factory, SIGNAL("activated()"), self.export_to_factory)
        self.connect(self.actionExport_to_Application, SIGNAL("activated()"),
                     self.export_to_application)
        self.connect(self.actionClear_Data_Pool, SIGNAL("activated()"), self.clear_data_pool)
        self.connect(self.search_lineEdit, SIGNAL("editingFinished()"), self.search_node)
        self.connect(self.action_New_Network, SIGNAL("activated()"), self.new_graph)
        self.connect(self.actionNew_Python_Node, SIGNAL("activated()"), self.new_python_node)
        self.connect(self.actionNew_Package, SIGNAL("activated()"), self.new_package)

        self.connect(self.action_Delete_2, SIGNAL("activated()"), self.delete_selection)

        


        # final init
        self.session = session
        wfactory = self.session.user_pkg['Workspace']
        self.open_compositenode(wfactory)
        
        

    def open_compositenode(self, factory):
        """ open a  composite node editor """
        node = factory.instantiate()

        self.open_widget_tab(node, factory=factory)
        self.session.add_workspace(node, notify=False)


    def about(self):
        """ Display About Dialog """
        
        mess = QtGui.QMessageBox.about(self, "About Visualea",
                                       "Version %s\n\n"%(metainfo.version) +
                                       "VisuAlea is part of the OpenAlea framework.\n"+
                                       u"Copyright \xa9  2006 INRIA - CIRAD - INRA\n"+
                                       "This Software is distributed under the GPL License.\n\n"+
                                       
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
                    self.export_to_factory(w)

        except Exception, e:
            pass

        # Update session
        try:
            node = self.index_nodewidget[cindex].node
            self.session.close_workspace(node, False)
            self.close_tab_workspace(cindex)
        except Exception, e:
            pass


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

        if(not caption) : caption = factory.get_id()
        
        index = self.tabWorkspace.insertTab(pos, container, caption)
        self.tabWorkspace.setCurrentIndex(index)
        self.index_nodewidget.append(widget)

        return index
        

    def add_wralea(self):

        filename = QtGui.QFileDialog.getOpenFileName(self, "Add Wralea")
        self.pkgmanager.add_wralea(str(filename))
        self.reinit_treeview()

    
    def find_wralea(self):

        self.pkgmanager.find_and_register_packages()
        self.reinit_treeview()

    
    def run(self):
        """ Run the active workspace """

        cindex = self.tabWorkspace.currentIndex()
        self.index_nodewidget[cindex].node.eval()
        

    def export_to_factory(self, widget=None):
        """ Export current workspace composite node to its factory """

        if(not widget):
            cindex = self.tabWorkspace.currentIndex()
            widget = self.index_nodewidget[cindex]
        
        try:
            f = widget.export_selection()
            if(not f) : return
            if(f is not widget.node.factory):
                self.open_compositenode(f)
            f.package.write()

        except AttributeError:
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "Cannot write Graph model on disk. :\n"+
                                             "You try to write in a System Package:\n")
            


    def export_to_application(self):
        """ Export current workspace composite node to an Application """

        mess = QtGui.QMessageBox.warning(self, "Error",
                                         "This functionality is not yet implemented")


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


    def new_graph(self):
        """ Create a new graph """

        pkgs = self.pkgmanager.get_user_packages()
        
        dialog = NewGraph("New Dataflow", pkgs, self.pkgmanager.category.keys(), self)
        ret = dialog.exec_()

        if(ret>0):
            newfactory = dialog.create_cnfactory(self.pkgmanager)
            self.reinit_treeview()
            self.open_compositenode(newfactory)


    def new_python_node(self):
        """ Create a new node """

        # Get default package
        pkgs = self.pkgmanager.get_user_packages()

        dialog = NewGraph("New Python Node", pkgs, self.pkgmanager.category.keys(), self)
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


    def new_session(self):

        self.session.clear()
        self.session.add_workspace(self.session.user_pkg['Workspace'].instantiate())

        
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


        

