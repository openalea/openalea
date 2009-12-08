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

class LayoutOperators(object):
    def graph_align_selection_horizontal(self):
        """Align all items on a median ligne.
        """
        widget = self.get_graph_view()
        
        if widget is None :
            return
        
        items = widget.get_selected_items(qtgraphview.Vertex)
        if len(items) > 1 :
            #find median base #TODO beware of relative to parent coordinates
            ymean = sum(item.vertex().get_ad_hoc_dict().get_metadata("position")[1] for item in items) / len(items)
            
            #move all items
            for item in items :
                item.vertex().get_ad_hoc_dict().set_metadata("position",
                                                             [item.vertex().get_ad_hoc_dict().get_metadata("position")[0],ymean])
        
            #notify
            widget.notify(None,("graph_modified",) )
        
        return

    def graph_align_selection_left (self):
        """Align all items on their left side.
        """
        widget = self.get_graph_view()        
        if widget is None :
            return
        
        items = widget.get_selected_items(qtgraphview.Vertex)
        if len(items) > 1 :
            #find left ligne #TODO beware of relative to parent coordinates
            xmean = sum(item.vertex().get_ad_hoc_dict().get_metadata("position")[0] for item in items) / len(items)
            
            #move all items
            for item in items :
                item.vertex().get_ad_hoc_dict().set_metadata("position", 
                                                             [xmean,
                                                              item.vertex().get_ad_hoc_dict().get_metadata("position")[1]])
            #notify
            widget.notify(None,("graph_modified",) )
        
        return

    def graph_align_selection_right (self):
        """Align all items on their right side.
        """
        widget = self.get_graph_view()
        if widget is None :
            return
        
        items = widget.get_selected_items(qtgraphview.Vertex)
        if len(items) > 1 :
            #find left ligne #TODO beware of relative to parent coordinates
            xmean = sum(item.vertex().get_ad_hoc_dict().get_metadata("position")[0] + \
                        item.boundingRect().width() \
                        for item in items) / len(items)
            
            #move all items
            for item in items :
                item.vertex().get_ad_hoc_dict().set_metadata("position", 
                                                             [xmean - item.boundingRect().width(),
                                                              item.vertex().get_ad_hoc_dict().get_metadata("position")[1]])
        
            #notify
            widget.notify(None,("graph_modified",) )
        
        return

    def graph_align_selection_mean (self):
        """Align all items vertically around a mean ligne.
        """
        widget = self.get_graph_view()        
        if widget is None :
            return

        items = widget.get_selected_items(qtgraphview.Vertex)        
        if len(items) > 1 :
            #find left ligne #TODO beware of relative to parent coordinates
            xmean = sum(item.vertex().get_ad_hoc_dict().get_metadata("position")[0] + \
                        item.boundingRect().width() / 2. \
                        for item in items) / len(items)
            
            #move all items
            for item in items :
                item.vertex().get_ad_hoc_dict().set_metadata("position", 
                                                             [xmean - item.boundingRect().width() / 2.,
                                                              item.vertex().get_ad_hoc_dict().get_metadata("position")[1]])
        
            #notify
            widget.notify(None,("graph_modified",) )
        
        return

    def graph_distribute_selection_horizontally (self):
        """distribute the horizontal distances between items.
        """
        widget = self.get_graph_view()        
        if widget is None :
            return
        
        items = widget.get_selected_items(qtgraphview.Vertex)        
        if len(items) > 2 :
            #find xmin,xmax of selected items #TODO beware of relative to parent coordinates
            xmin = min(item.vertex().get_ad_hoc_dict().get_metadata("position")[0] for item in items)
            xmax = max(item.vertex().get_ad_hoc_dict().get_metadata("position")[0] + item.boundingRect().width() \
                       for item in items)
            
            #find mean distance between items
            dist = ( (xmax - xmin) - \
                   sum(item.boundingRect().width() for item in items) )\
                   / (len(items) - 1)
            
            #sort all items by their mean position
            item_centers = [(item.vertex().get_ad_hoc_dict().get_metadata("position")[0] + item.boundingRect().width() / 2.,item) for item in items]
            item_centers.sort()
            
            #move all items
            first_item = item_centers[0][1]
            current_x = first_item.vertex().get_ad_hoc_dict().get_metadata("position")[0] + first_item.boundingRect().width()
            
            for x,item in item_centers[1:-1] :
                item.vertex().get_ad_hoc_dict().set_metadata("position", 
                                                             [current_x + dist,
                                                              item.vertex().get_ad_hoc_dict().get_metadata("position")[1]])
                current_x += dist + item.boundingRect().width()
        
            #notify
            widget.notify(None,("graph_modified",) )
        
        return

    def graph_distribute_selection_vertically (self):
        """distribute the vertical distances between items.
        """
        widget = self.get_graph_view()
        if widget is None :
            return
        
        items = widget.get_selected_items(qtgraphview.Vertex)        
        if len(items) > 1 :
            #find ymin,ymax of selected items #TODO beware of relative to parent coordinates
            ymin = min(item.vertex().get_ad_hoc_dict().get_metadata("position")[1] for item in items)
            ymax = max(item.vertex().get_ad_hoc_dict().get_metadata("position")[1] + item.boundingRect().height() \
                       for item in items)
            
            #find mean distance between items
            dist = ( (ymax - ymin) - \
                   sum(item.boundingRect().height() for item in items) )\
                   / (len(items) - 1)
            
            #sort all items by their mean position
            item_centers = [(item.vertex().get_ad_hoc_dict().get_metadata("position")[1] + item.boundingRect().height() / 2.,item) for item in items]
            item_centers.sort()
            
            #move all items
            first_item = item_centers[0][1]
            current_y = first_item.vertex().get_ad_hoc_dict().get_metadata("position")[1] + first_item.boundingRect().height()
            
            for y,item in item_centers[1:-1] :
                item.vertex().get_ad_hoc_dict().set_metadata("position", 
                                                             [item.vertex().get_ad_hoc_dict().get_metadata("position")[0],
                                                              current_y + dist])
                current_y += dist + item.boundingRect().height()
            
            #notify
            widget.notify(None,("graph_modified",) )
        
        return
