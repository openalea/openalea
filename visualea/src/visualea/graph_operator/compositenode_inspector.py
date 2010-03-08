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


from PyQt4 import QtCore
from openalea.core.observer import AbstractListener
from openalea.grapheditor import qtgraphview
from openalea.visualea.util import exception_display

class Inspector(qtgraphview.View, AbstractListener):
    def __init__(self, parent, graph, mainOperator, parentOperator):
        qtgraphview.View.__init__(self, parent, graph)
        AbstractListener.__init__(self)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Inspecting " + graph.get_caption())
        self.__mainOperator   = mainOperator
        self.__parentOperator = parentOperator
        self.initialise(mainOperator)
        self.initialise(parentOperator)
        mainOperator.get_session().add_graph_view(self)

    @exception_display        
    def notify(self, sender, event):
        if(event):
            if(event[0] == "graphoperator_graphsaved"):
                event[1].setWindowTitle("Inspecting " + event[2].name)
            elif(event[0] == "graphoperator_graphclosed"):
                event[1].close()
            elif(event[0] == "graphoperator_graphreloaded"):
                pass
            return
        super(Inspector, self).notify(sender, event)
