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
from subgraph_widget import SubGraphWidget



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

        # Dictionnary to map node with workspace tabs
        self.node_tabindex = {} 

        self.tabWorkspace.removeTab(0)

        # python interpreter

        self.interpreterWidget = PyCutExt(locals=globals, parent=self.splitter)

        # package tree view

        self.pkg_model = PkgModel(pkgman)

        self.packageTreeView = NodeTreeView(self.packageview)
        self.packageTreeView.setModel(self.pkg_model)
        self.vboxlayout.addWidget(self.packageTreeView)

        # menu callbacks

        self.connect(self.action_About, SIGNAL("activated()"), self.about)
        self.connect(self.action_Help, SIGNAL("activated()"), self.help)

        self.connect(self.action_Quit, SIGNAL("activated()"), self.quit)

        self.connect(self.action_Close_current_workspace, SIGNAL("activated()")
                     , self.close_workspace)


        # final init
        self.root = rootsubgraph
        self.open_widget(rootsubgraph)


    def about(self):
        """ Display About Dialog """

        mess = QtGui.QMessageBox.about(self, "About Visualea",
                                       "Visualea is part of the OpenAlea framework.\n\n"+
                                       u"Copyright \xa9  2006 INRIA - CIRAD - INRA\n"+
                                       "This Software is distributed under the GPL License\n\n"+
                                       
                                       "Visit http://openalea.gforge.inria.fr\n")

    def help(self):
        """ Display help """
        pass

    def quit(self):
        """ Quit Application """

        self.close()

    def close_workspace(self):
        """ Close current workspace """

        cindex = self.tabWorkspace.currentIndex()
        if(cindex == 0):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "You cannot close Root workspace")
            return
        
        self.tabWorkspace.removeTab( cindex )

        for n in self.node_tabindex.keys():
            if(self.node_tabindex[n] == cindex):
                del(self.node_tabindex[n])


    def open_widget(self, factory, node = None, caption=""):
        """
        Open a widget giving the factory and an instance
        if node is null, a new instance is allocated
        caption is append to the tab title
        """

        container = QtGui.QWidget()

        if ( node == None) :
            node = factory.instantiate()

        # Test if the node is already opened
        elif( self.node_tabindex.has_key(node)):
            self.tabWorkspace.setCurrentIndex(self.node_tabindex[node])
            return
            
        widget = factory.instantiate_widget(node, self, container)
        widget.wcaption = caption
        
        vboxlayout = QtGui.QVBoxLayout(container)
        vboxlayout.addWidget(widget)

        if(caption) : caption = " - %s "%(caption,)
        
        index = self.tabWorkspace.addTab(container, factory.get_id() + caption)
        self.tabWorkspace.setCurrentIndex(index)

        self.node_tabindex[node] = index
        

