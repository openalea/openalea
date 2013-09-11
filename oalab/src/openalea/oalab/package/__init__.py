# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = ""

from openalea.vpltk.qt import qt
from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.package import Package

from openalea.visualea.node_treeview import NodeFactoryView, NodeFactoryTreeView, PkgModel, CategoryModel
from openalea.visualea.node_treeview import DataPoolListView, DataPoolModel
from openalea.visualea.node_treeview import SearchListView, SearchModel

class OALabTreeView(NodeFactoryTreeView):
    def __init__(self, parent):
        super(OALabTreeView, self).__init__(self) 
        self.session = parent

    def mouseDoubleClickEvent(self, event):

        item = self.currentIndex()
        obj =  item.internalPointer()

        if(isinstance(obj, CompositeNodeFactory)):
            session = self.session
            session.applet_container.newTab('wpy',obj.name+'.wpy',obj)

            #self.edit_node()
        elif (not isinstance(obj, Package)):
            self.open_node()

class OALabSearchView(SearchListView):
    def __init__(self, main_win, parent):
        super(OALabSearchView, self).__init__(self, main_win) 
        self.session = parent

    def mouseDoubleClickEvent(self, event):

        item = self.currentIndex()
        obj =  item.internalPointer()

        if(isinstance(obj, CompositeNodeFactory)):
            session = self.session
            session.applet_container.newTab('wpy',obj.name+'.wpy',obj)

            #self.edit_node()
        elif (not isinstance(obj, Package)):
            self.open_node()


class PackageViewWidget(OALabTreeView):
    """
    Widget for Package Manager
    """
    def __init__(self, parent):
        super(PackageViewWidget, self).__init__(self) 
        self.session = parent
        pkgmanager = parent.pm
        
        # package tree view
        self.pkg_model = PkgModel(pkgmanager)
        self.setModel(self.pkg_model)
        
    def reinit_treeview(self):
        """ Reinitialise package and category views """
        self.pkg_model.reset()

class PackageCategorieViewWidget(OALabTreeView):
    """
    Widget for Package Manager Categories
    """
    def __init__(self, parent):
        super(PackageCategorieViewWidget, self).__init__(self) 
        pkgmanager = parent.pm
        self.session = parent
        # category tree view
        self.cat_model = CategoryModel(pkgmanager)
        self.setModel(self.cat_model)

    def reinit_treeview(self):
        """ Reinitialise package and category views """
        self.cat_model.reset()


class PackageSearchWidget(QtGui.QWidget):
    """
    Use it to find packages.
    
    Same thing as in Visualea.
    
    Widget with line edit (to search) and finding packages.
    """
    def __init__(self, parent):
        super(PackageSearchWidget, self).__init__()
        
        self.pkgmanager = parent.pm
        
        self.searchview = QtGui.QWidget()
        self.result_widget = SearchListView(self.searchview)
        self.search_model = SearchModel()
        self.result_widget.setModel(self.search_model)
        
        self.search_lineEdit = QtGui.QLineEdit(self)
        self.search_lineEdit.editingFinished.connect( self.search_node)
        
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.search_lineEdit)
        layout.addWidget(self.result_widget)
        
        self.setLayout(layout)
        
    def search_node(self):
        """ Activated when search line edit is validated """
        text = str(unicode(self.search_lineEdit.text()).encode('latin1'))
        results = self.pkgmanager.search_node(text)
        self.search_model.set_results(results) ###result_model, result_widget
