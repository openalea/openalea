# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the GPL License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.gnu.org/licenses/gpl.txt
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
QT4 Main window 
"""

__license__= "GPL"
__revision__=" $Id$ "


from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL

import ui_mainwindow
from pycutext import PyCutExt

from node_treeview import NodeTreeView, PkgModel

import config



class MainWindow(  QtGui.QMainWindow, ui_mainwindow.Ui_MainWindow) :

    def __init__(self, pkgman, rootsubgraph, globals=None, parent=None):
        """
        @param pkgman : the package manager
        @param globals : python interpreter globals
        @param parent : parent window
        @param rootsubgraph : root SubGraphFactory 
        """

        QtGui.QMainWindow.__init__(self, parent)
        ui_mainwindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)


        self.pkgmanager = pkgman

        # Dictionnary to map factory with workspace tabs
        self.factory_tabindex = {} 

        self.tabWorkspace.removeTab(0)

        # python interpreter

        self.interpreterWidget = PyCutExt(locals=globals, parent=self.splitter)

        # package tree view

        self.pkg_model = PkgModel(pkgman)

        self.packageTreeView = NodeTreeView(self, self.packageview)
        self.packageTreeView.setModel(self.pkg_model)
        self.vboxlayout.addWidget(self.packageTreeView)

        # menu callbacks

        self.connect(self.action_About, SIGNAL("activated()"), self.about)
        self.connect(self.action_Help, SIGNAL("activated()"), self.help)

        self.connect(self.action_Quit, SIGNAL("activated()"), self.quit)

        self.connect(self.action_Close_current_workspace, SIGNAL("activated()"),
                     self.close_workspace)

        self.connect(self.action_Auto_Search, SIGNAL("activated()"),
                     self.find_wralea)
        self.connect(self.action_Add_File, SIGNAL("activated()"),
                     self.add_wralea)
        

        
        # final init
        self.root = rootsubgraph
        self.open_widget_tab(rootsubgraph)


    def about(self):
        """ Display About Dialog """

        
        mess = QtGui.QMessageBox.about(self, "About Visualea",
                                       "Version %s\n\n"%(config.version) +
                                       "VisuAlea is part of the OpenAlea framework.\n"+
                                       u"Copyright \xa9  2006 INRIA - CIRAD - INRA\n"+
                                       "This Software is distributed under the GPL License.\n\n"+
                                       
                                       "Visit http://openalea.gforge.inria.fr\n")

    def help(self):
        """ Display help """
        pass

    def quit(self):
        """ Quit Application """

        self.close()

    def closeEvent(self, event):
        """ Close All subwindows """
        
        for i in range(self.tabWorkspace.count()):
            w = self.tabWorkspace.widget(i)
            w.close()
        event.accept()
            
    def close_workspace(self):
        """ Close current workspace """

        cindex = self.tabWorkspace.currentIndex()
        if(cindex == 0):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "You cannot close Root workspace")
            return
        
        w = self.tabWorkspace.widget(cindex)
        self.tabWorkspace.removeTab( cindex )
        w.close()
        w.emit(QtCore.SIGNAL("close()"))
        
        for n in self.factory_tabindex.keys():
            if(self.factory_tabindex[n] == cindex):
                del(self.factory_tabindex[n])



    def open_widget_tab(self, factory, node = None, caption=""):
        """
        Open a widget in a tab giving the factory and an instance
        if node is null, a new instance is allocated
        caption is append to the tab title
        """

        
        # Test if the node is already opened
        if( self.factory_tabindex.has_key(factory)):
            self.tabWorkspace.setCurrentIndex(self.factory_tabindex[factory])
            return

        container = QtGui.QWidget(self)
        container.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        widget = factory.instantiate_widget(node, self, parent=container)
        widget.wcaption = caption
        
        vboxlayout = QtGui.QVBoxLayout(container)
        vboxlayout.addWidget(widget)

        if(caption) : caption = " - %s "%(caption,)
        
        index = self.tabWorkspace.addTab(container, factory.get_id() + caption)
        self.tabWorkspace.setCurrentIndex(index)

        self.factory_tabindex[factory] = index
        

    def add_wralea(self):

        filename = QtGui.QFileDialog.getOpenFileName(self, "Add Wralea")
        
        self.pkgmanager.add_wralea(str(filename))
        self.packageTreeView.model().emit(QtCore.SIGNAL("layoutChanged()"))
    
    def find_wralea(self):

        self.pkgmanager.find_and_register_packages()
        self.packageTreeView.model().emit(QtCore.SIGNAL("layoutChanged()"))
    
