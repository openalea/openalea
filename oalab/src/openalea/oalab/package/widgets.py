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

from openalea.vpltk.qt import QtGui
from openalea.core.node import NodeFactory
from openalea.visualea.node_treeview import NodeFactoryView, PkgModel, CategoryModel
from openalea.visualea.node_treeview import DataPoolListView, DataPoolModel
from openalea.visualea.node_treeview import SearchListView, SearchModel
from openalea.oalab.package.treeview import OALabTreeView

class PackageViewWidget(OALabTreeView):
    """
    Widget for Package Manager
    """
    def __init__(self, session, controller, parent=None):
        super(PackageViewWidget, self).__init__(session, controller, parent=parent) 
        self.session = session
        self.controller = controller
        
        # package tree view
        self.pkg_model = PkgModel(self.session.pm)
        self.setModel(self.pkg_model)
        
        self.clicked.connect(self.on_package_manager_focus_change)
        
    def on_package_manager_focus_change(self, item):
        pkg_id, factory_id, mimetype = NodeFactoryView.get_item_info(item)
        if len(pkg_id) and len(factory_id) and mimetype in [NodeFactory.mimetype,
                                                            CompositeNodeFactory.mimetype]:
            factory = self.session.pm[pkg_id][factory_id]
            factoryDoc = factory.get_documentation()
            txt = factory.get_tip(asRst=True) + "\n\n"
            if factoryDoc is not None:
                txt += "**Docstring:**\n" + factoryDoc
            self.controller.applets['Help'].setText(txt)        

    def reinit_treeview(self):
        """ Reinitialise package and category views """
        self.pkg_model.reset()

class PackageCategorieViewWidget(OALabTreeView):
    """
    Widget for Package Manager Categories
    """
    def __init__(self, session, controller, parent=None):
        super(PackageCategorieViewWidget, self).__init__(session, controller, parent=parent) 
        self.session = session
        self.controller = controller
        # category tree view
        self.cat_model = CategoryModel(self.session.pm)
        self.setModel(self.cat_model)
        self.clicked.connect(self.on_package_manager_focus_change)
        
    def on_package_manager_focus_change(self, item):
        pkg_id, factory_id, mimetype = NodeFactoryView.get_item_info(item)
        if len(pkg_id) and len(factory_id) and mimetype in [NodeFactory.mimetype,
                                                            CompositeNodeFactory.mimetype]:
            factory = self.session.pm[pkg_id][factory_id]
            factoryDoc = factory.get_documentation()
            txt = factory.get_tip(asRst=True) + "\n\n"
            if factoryDoc is not None:
                txt += "**Docstring:**\n" + factoryDoc
            self.controller.applets['Help'].setText(txt)   
            
    def reinit_treeview(self):
        """ Reinitialise package and category views """
        self.cat_model.reset()


class PackageSearchWidget(QtGui.QWidget):
    """
    Use it to find packages.
    
    Same thing as in Visualea.
    
    Widget with line edit (to search) and finding packages.
    """
    def __init__(self, session, controller, parent=None):
        super(PackageSearchWidget, self).__init__()
        self.session = session
        self.controller = controller
        
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
        self.result_widget.clicked.connect(self.on_package_manager_focus_change)
        
    def on_package_manager_focus_change(self, item):
        pkg_id, factory_id, mimetype = NodeFactoryView.get_item_info(item)
        if len(pkg_id) and len(factory_id) and mimetype in [NodeFactory.mimetype,
                                                            CompositeNodeFactory.mimetype]:
            factory = self.session.pm[pkg_id][factory_id]
            factoryDoc = factory.get_documentation()
            txt = factory.get_tip(asRst=True) + "\n\n"
            if factoryDoc is not None:
                txt += "**Docstring:**\n" + factoryDoc
            self.controller.applets['Help'].setText(txt)   
            
    def search_node(self):
        """ Activated when search line edit is validated """
        text = str(unicode(self.search_lineEdit.text()).encode('latin1'))
        results = self.session.pm.search_node(text)
        self.search_model.set_results(results) ###result_model, result_widget
