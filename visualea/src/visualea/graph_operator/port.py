# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import base as graphOpBase
from PyQt4 import QtGui, QtCore
from openalea.grapheditor import qtgraphview


class PortOperators(graphOpBase.Base):

    
    def port_print_value(self):
        """ Print the value of the connector """
        
        node = self.master.portItem().port().vertex()
        data = str(node.get_output(self.master.portItem().port().get_id()))
        data = data[:500]+"[...truncated]" if len(data)>500 else data
        print data

    
    def port_send_to_pool(self):
        master = self.master

        (result, ok) = QtGui.QInputDialog.getText(master.get_graph_view(), "Data Pool", "Instance name",
                                                  QtGui.QLineEdit.Normal, )
        if(ok):
            from openalea.core.session import DataPool
            datapool = DataPool()  # Singleton

            port = self.master.portItem().port()
            node = port.vertex()
            data = node.get_output(port.get_id())
            datapool[str(result)] = data
