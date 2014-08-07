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
from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.package import Package
from openalea.visualea.node_treeview import NodeFactoryTreeView
from openalea.visualea.node_treeview import SearchListView
from openalea.oalab.service.applet import get_applet

class OALabTreeView(NodeFactoryTreeView):
    def __init__(self, session, controller, parent=None):
        super(OALabTreeView, self).__init__(controller) 
        self.session = session
        self.controller = controller

    def mouseDoubleClickEvent(self, event):

        item = self.currentIndex()
        obj =  item.internalPointer()

        if(isinstance(obj, CompositeNodeFactory)):
            applet = get_applet(identifier='EditorManager')
            if applet:
                #applet.newTab('Workflow', obj.name + '.wpy', obj)
                cat, fn = applet.add(applet.project(), obj.name + '.wpy', obj, category='model', dtype='Workflow')
                applet.open_project_data(cat, fn)
                #applet.open_data(obj, dtype='Workflow')
        elif (not isinstance(obj, Package)):
            self.open_node()


class OALabSearchView(SearchListView):
    def __init__(self, session, controller, parent=None):
        main_win = QtGui.QWidget()
        super(OALabSearchView, self).__init__(main_win)
        self.session = session
        self.controller = controller

    def mouseDoubleClickEvent(self, event):

        item = self.currentIndex()
        obj =  item.internalPointer()

        if(isinstance(obj, CompositeNodeFactory)):
            applet = get_applet(identifier='EditorManager')
            if applet:
                #applet.newTab('Workflow', obj.name + '.wpy', obj)
                cat, fn = applet.add(applet.project(), obj.name + '.wpy', obj, category='model', dtype='Workflow')
                applet.open_project_data(cat, fn)


        elif (not isinstance(obj, Package)):
            self.open_node()
