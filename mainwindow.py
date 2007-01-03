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

    def __init__(self, pkgman, globals=None, parent=None):
        """
        @param pkgman : the package manager
        @param globals : python interpreter globals
        @param parent : parent window
        """

        QtGui.QMainWindow.__init__(self, parent)
        ui_mainwindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.pkgmanager = pkgman
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

        self.connect(self.action_Close_current_workspace, SIGNAL("activated()"), self.close_workspace)

        


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

        self.tabWorkspace.removeTab( self.tabWorkspace.currentIndex())


    def open_tabwidget_byname(self, pkg_name, node_name):
        """ Open a widget in the tab view by its name """

        container = QtGui.QWidget()

        pkg = self.pkgmanager[pkg_name]
        factory = pkg[node_name]
        node = factory.instantiate()
        widget = factory.instantiate_widget(node, container)

        vboxlayout = QtGui.QVBoxLayout(container)
        vboxlayout.addWidget(widget)

        index = self.tabWorkspace.addTab(container, node_name)
        self.tabWorkspace.setCurrentIndex(index)


    def open_tabwidget(self, factory):
        """ Open a widget in the tab view """

        container = QtGui.QWidget()

        node = factory.instantiate()
        widget = factory.instantiate_widget(node, container)

        vboxlayout = QtGui.QVBoxLayout(container)
        vboxlayout.addWidget(widget)

        index = self.tabWorkspace.addTab(container, factory.get_id())
        self.tabWorkspace.setCurrentIndex(index)

