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

from PyQt4 import QtGui, QtCore
from openalea.grapheditor import qtgraphview

#To handle availability of actions automatically
from openalea.grapheditor import interactionstates as OAGIS
masker = OAGIS.make_interaction_level_decorator()

class ColorOperators(object):

    @masker(OAGIS.EDITIONLEVELLOCK_2)
    def graph_set_selection_color(self):
        items = self.get_graph_view().scene().get_selected_items(qtgraphview.Vertex)
        length = len(items)
        if(length==0): return
        if(length==1):
            color = items[0].vertex().get_ad_hoc_dict().get_metadata("userColor")
            if(color):
                color = QtGui.QColor(*color)
            else: color = QtGui.QColor(100,100,100,255)
        else:
            color = QtGui.QColor(100,100,100,255)

        color = QtGui.QColorDialog.getColor(color, self.get_graph_view())

        if not color.isValid():
            return

        color = [color.red(), color.green(), color.blue()]
        for i in items:
            try:
                i.vertex().get_ad_hoc_dict().set_metadata("userColor", color)
                i.vertex().get_ad_hoc_dict().set_metadata("useUserColor", True)
            except Exception, e:
                print "graph_set_selection_color exception", e
                pass

    @masker(OAGIS.EDITIONLEVELLOCK_2)
    def graph_use_user_color(self, useit):
        items = self.get_graph_view().scene().get_selected_items(qtgraphview.Vertex)
        if(not items): return
        scheduleASetColor = False
        for i in items:
            if(i.vertex().get_ad_hoc_dict().get_metadata("userColor") is None
               and useit):
                scheduleASetColor = True
                continue
            else:
                i.vertex().get_ad_hoc_dict().set_metadata("useUserColor", useit)
                i.setSelected(False)
        if(scheduleASetColor):
            self.graph_set_selection_color()

    vertex_set_color    = graph_set_selection_color
    vertex_use_user_color = graph_use_user_color
