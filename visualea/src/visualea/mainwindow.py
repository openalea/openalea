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
from pycutext import PyCutExt


from openalea.core import cli
from code import InteractiveInterpreter as Interpreter

from node_treeview import NodeFactoryTreeView, PkgModel, CategoryModel
from node_treeview import DataPoolListView, DataPoolModel
from node_treeview import SearchListView, SearchModel

import metainfo

from openalea.core.core import UserFactory
from openalea.core.subgraph import SubGraphFactory
from openalea.core.observer import AbstractListener

class MainWindow(QtGui.QMainWindow,
                 ui_mainwindow.Ui_MainWindow,
                 AbstractListener) :

    def __init__(self, pkgman, session, parent=None):
        """
        @param pkgman : the package manager
        @param session : user session
        @param parent : parent window
        """

        QtGui.QMainWindow.__init__(self, parent)
        AbstractListener.__init__(self)
        ui_mainwindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.pkgmanager = pkgman

        # Set observer
        self.initialise(session)

        # Array to map tab index with node widget
        self.index_nodewidget = []

        self.tabWorkspace.removeTab(0)

        # python interpreter
        interpreter = Interpreter()
        cli.init_interpreter(interpreter, session)
        self.interpreterWidget = PyCutExt(interpreter, cli.get_welcome_msg(), parent=self.splitter)

        # package tree view
        self.pkg_model = PkgModel(pkgman)
        self.packageTreeView = NodeFactoryTreeView(self, self.packageview)
        self.packageTreeView.setModel(self.pkg_model)
        self.vboxlayout.addWidget(self.packageTreeView)

        # category tree view
        self.cat_model = CategoryModel(pkgman)
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
        self.datapoolListView = DataPoolListView(self, session.datapool, self.datapoolview)
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
        self.connect(self.actionClear_Data_Pool, SIGNAL("activated()"),
                     self.clear_data_pool)
        self.connect(self.search_lineEdit, SIGNAL("editingFinished()"),
                     self.search_node)

        self.connect(self.action_New_Network, SIGNAL("activated()"),
                     self.new_graph)
        self.connect(self.actionNew_Python_Node, SIGNAL("activated()"),
                     self.new_python_node)
                
        
        # final init
        self.session = session
        workspace_factory = self.session.user_pkg['Workspace']
        node = workspace_factory.instantiate()
        self.session.add_workspace(node)
        self.open_widget_tab(node)


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
        

    def close_workspace(self):
        """ Close current workspace """

        cindex = self.tabWorkspace.currentIndex()

        subgraph = self.index_nodewidget[cindex].node
        # Generate factory if user want
        try :
            modified = subgraph.graph_modified
        except:
            modified = False
            
        if(modified):

            ret = QtGui.QMessageBox.question(self, "Close Workspace",
                                             "Subgraph has been modified.\n"+
                                             "Do you want to report changes to factory ?\n",
                                             QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,)
            
            if(ret == QtGui.QMessageBox.Yes):
                subgraph.to_factory(subgraph.factory)
        

        # Update session
        try:
            factory = self.index_nodewidget[cindex].node.factory
            self.session.close_workspace(factory)
            self.close_tab_workspace(cindex)
        except:
            pass
        

    def close_tab_workspace(self, cindex):
        """ Close workspace indexed by cindex cindex is Node"""
        
        w = self.tabWorkspace.widget(cindex)
        self.tabWorkspace.removeTab( cindex )
        w.close()
        w.emit(QtCore.SIGNAL("close()"))
        
        #self.index_nodewidget[cindex].release_listeners()
        del(self.index_nodewidget[cindex])
      

    def update_tabwidget(self):
        """ open tab widget """

        # open tab widgets
        for i in range(len(self.session.workspaces)):
            node = self.session.workspaces[i]

            try:
                widget = self.index_nodewidget[i]
                if(node != widget.node):
                    self.close_tab_workspace(i)
            except: pass
            
            self.open_widget_tab(node, pos = i)

        removelist = range( len(self.session.workspaces),
                        len(self.index_nodewidget))
        removelist.reverse()
        
        for i in removelist:
            self.close_tab_workspace(i)


    def open_widget_tab(self, node, caption=None, pos = -1):
        """
        Open a widget in a tab giving the factory and an instance
        if node is null, a new instance is allocated
        caption is append to the tab titleself.action_New_Network
        """
        
        # Test if the node is already opened
        for i in range(len(self.index_nodewidget)):
            widget = self.index_nodewidget[i]
            f = widget.node.factory
            if(node.factory is f):
                self.tabWorkspace.setCurrentIndex(i)
                return

        factory = node.factory

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

        self.pkgmanager
        self.pkgmanager.find_and_register_packages()
        self.reinit_treeview()

    
    def run(self):
        """ Run the active workspace """

        cindex = self.tabWorkspace.currentIndex()
        self.index_nodewidget[cindex].node.eval()
        

    def export_to_factory(self):
        """ Export current workspace subgraph to its factory """

        cindex = self.tabWorkspace.currentIndex()
        subgraph = self.index_nodewidget[cindex].node
        subgraph.to_factory(subgraph.factory)


    def export_to_application(self):
        """ Export current workspace subgraph to an Application """

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

        action = menu.addAction("Run")
        self.connect(action, SIGNAL("activated()"), self.run)

        action = menu.addAction("Apply changes")
        self.connect(action, SIGNAL("activated()"), self.export_to_factory)

        menu.move(event.globalPos())
        menu.show()


    def new_graph(self):
        """ Create a new graph """

        # Get default package
        pkg = self.session.user_pkg

        dialog = NewGraph("New Dataflow", pkg, self.pkgmanager.category.keys())
        ret = dialog.exec_()

        if(ret>0):
            (name, nin, nout, cat, desc) = dialog.get_data()

            newfactory = SubGraphFactory(self.pkgmanager, name=name,
                                         description= desc,
                                         category = cat,
                                         )
            
            newfactory.set_nb_input(nin)
            newfactory.set_nb_output(nout)
            
            pkg.add_factory(newfactory)
            self.pkgmanager.add_package(pkg)

            self.reinit_treeview()

            node = newfactory.instantiate()
            self.session.add_workspace(node)
            self.open_widget_tab(node)


    def new_python_node(self):
        """ Create a new node """

        # Get default package
        pkg = self.session.user_pkg

        dialog = NewGraph("New Python Node", pkg, self.pkgmanager.category.keys())
        ret = dialog.exec_()

        if(ret>0):
            (name, nin, nout, cat, desc) = dialog.get_data()

            newfactory = UserFactory(name=name,
                                     description= desc,
                                     category = cat,
                                     )
            
            pkg.add_factory(newfactory)
            self.pkgmanager.add_package(pkg)

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
            self, "OpenAlea Session", QtCore.QDir.homePath(), "XML file (*.xml)")

        filename = str(filename)
        if(not filename) : return

        self.session.load(filename)


    def export_subgraph(self):
        """ Export all open subgraph to there factory"""

        ret = QtGui.QMessageBox.question(self, "Export",
                                         "Subgraphs has been modified.\n"+
                                         "Do you want to report changes to Package Manager ?\n",
                                         QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,)

        if(ret == QtGui.QMessageBox.No): return

        for widget in self.index_nodewidget:

            subgraph = widget.node
            try:
                subgraph.to_factory(subgraph.factory)
            except:
                pass


    def save_session(self):

        if(not self.session.session_filename):
            self.save_as()
        else :
            self.export_subgraph()
            self.session.save(self.session.session_filename)

        
    def save_as(self):

        self.export_subgraph()
        filename = QtGui.QFileDialog.getSaveFileName(
            self, "OpenAlea Session",  QtCore.QDir.homePath(), "XML file (*.xml)")

        filename = str(filename)
        if(not filename) : return

        self.session.save(filename)

    def clear_data_pool(self):

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
       


################################################################################
import ui_newgraph

class NewGraph(QtGui.QDialog, ui_newgraph.Ui_NewGraphDialog) :
    """ New network dialog """
    
    def __init__(self, title, package, categories, parent=None):
        """
        Constructor
        @param pacakge : the package the graph will be added to
        """

        QtGui.QDialog.__init__(self, parent)
        ui_newgraph.Ui_NewGraphDialog.__init__(self)
        self.setWindowTitle(title)

        self.setupUi(self)

        self.package = package
        self.categoryEdit.addItems(categories)


    def accept(self):

        # Test if name is correct
        name = str(self.nameEdit.text())
        if(self.package.has_key(name)):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                            "The Name is already use")
            return

        
        QtGui.QDialog.accept(self)


    def get_data(self):
        """
        Return the dialog data in a tuple
        (name, nin, nout, category, description)
        """

        name = str(self.nameEdit.text())
        category = str(self.categoryEdit.currentText().toAscii())
        description = str(self.descriptionEdit.text().toAscii())

        return (name, self.inBox.value(), self.outBox.value(), category, description)
    
        


