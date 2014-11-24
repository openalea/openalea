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

from openalea.vpltk.qt import qt
from openalea.visualea.graph_operator.base import Base

class LayoutOperators(Base):

    def graph_align_selection_horizontal(self):
        """Align all items on a median ligne"""
        master = self.master
        scene = master.get_graph_scene()

        if scene is None :
            return

        items = scene.get_selected_items( master.vertexType, lambda x: (x, x.get_view_data("position")) )
        count = len(items)
        if count > 1 :
            #find median base
            ymean = sum(pos[1] for item, pos in items) / count

            #move all items
            for item, pos in items :
                item.store_view_data(position=[pos[0], ymean])
            #notify
            scene.notify(None,("graph_modified",) )

        return


    def graph_align_selection_left (self):
        """Align all items on their left side."""
        master = self.master
        scene = master.get_graph_scene()
        if scene is None :
            return

        items = scene.get_selected_items(master.vertexType, lambda x: (x, x.get_view_data("position")) )
        count = len(items)
        if count > 1 :
            #find left ligne
            xmean = sum(pos[0] for item, pos in items) / count

            #move all items
            for item, pos in items :
                item.store_view_data(position=[xmean, pos[1]])
            #notify
            scene.notify(None,("graph_modified",) )

        return


    def graph_align_selection_right (self):
        """Align all items on their right side"""
        master = self.master
        scene = master.get_graph_scene()
        if scene is None :
            return

        items = scene.get_selected_items(master.vertexType, lambda x: (x,
                                                                       x.get_view_data("position"),
                                                                       x.boundingRect().width()) )
        count = len(items)
        if count > 1 :
            #find left line
            xmean = sum(pos[0] + width for item, pos, width in items) / count

            #move all items
            for item, pos, width in items :
                item.store_view_data(position=[xmean - width, pos[1]])

            #notify
            scene.notify(None,("graph_modified",) )

        return


    def graph_align_selection_mean (self):
        """Align all items vertically around a mean line."""
        master = self.master
        scene = master.get_graph_scene()
        if scene is None :
            return

        items = scene.get_selected_items(master.vertexType, lambda x: (x,
                                                                       x.get_view_data("position"),
                                                                       x.boundingRect().width()) )
        count = len(items)
        if count > 1 :
            #find left ligne
            xmean = sum(pos[0] + width/2. for item, pos, width in items) / count

            #move all items
            for item, pos, width in items :
                item.store_view_data(position=[xmean - width/2., pos[1]])
            #notify
            scene.notify(None,("graph_modified",) )

        return


    def graph_distribute_selection_horizontally (self):
        """distribute the horizontal distances between items."""
        master = self.master
        scene = master.get_graph_scene()
        if scene is None :
            return

        items = scene.get_selected_items(master.vertexType, lambda x: (x,
                                                                       x.get_view_data("position"),
                                                                       x.boundingRect().width()) )

        count = len(items)
        if count > 2 :
            #find xmin,xmax of selected items
            xmin = min(pos[0] for item, pos, width in items)
            xmax = max(pos[0] + width for item, pos, width in items)

            #find mean distance between items
            dist = ( (xmax - xmin)-sum(width for item, pos, width in items) ) / (count - 1)

            # #sort all items by their mean position
            items.sort( lambda x, y: cmp(x[1][0]+x[2]/2, y[1][0]+y[2]/2) )

            #first item serves as reference
            item, pos, width = items[0]
            current_x = pos[0] + width

            for item, pos, width in items[1:-1] :
                item.store_view_data(position=[current_x + dist, pos[1]])
                current_x += dist + width
            #notify
            scene.notify(None,("graph_modified",) )

        return


    def graph_distribute_selection_vertically (self):
        """distribute the vertical distances between items."""
        master = self.master
        scene = master.get_graph_scene()
        if scene is None :
            return

        items = scene.get_selected_items(master.vertexType, lambda x: (x,
                                                                       x.get_view_data("position"),
                                                                       x.boundingRect().height()) )
        count = len(items)
        if count > 1 :
            #find ymin,ymax of selected items
            ymin = min(pos[1] for item, pos, height in items)
            ymax = max(pos[1] + height for item, pos, height in items)

            #find mean distance between items
            dist = ( (ymax - ymin) - sum(height for item, pos, height in items) ) / (count - 1)

            #sort all items by their mean position
            items.sort( lambda x, y: cmp(x[1][1]+x[2]/2, y[1][1]+y[2]/2) )

            #first item serves as reference
            item, pos, height = items[0]
            current_y = pos[1] + height

            for item, pos, height in items[1:-1] :
                item.store_view_data(position=[pos[0], current_y + dist])
                current_y += dist + height

            #notify
            scene.notify(None,("graph_modified",) )

        return
