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

from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.package import Package
from openalea.visualea.node_treeview import NodeFactoryTreeView

class OALabTreeView(NodeFactoryTreeView):
    def __init__(self, session, controller, parent=None):
        super(OALabTreeView, self).__init__(controller) 
        self.session = session
        self.controller = controller

    def mouseDoubleClickEvent(self, event):

        item = self.currentIndex()
        obj =  item.internalPointer()

        if(isinstance(obj, CompositeNodeFactory)):
            self.controller.applet_container.newTab('Workflow',obj.name+'.wpy',obj)

        elif (not isinstance(obj, Package)):
            self.open_node()

