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
"""Dataflow painting strategies"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import weakref
from PyQt4 import QtGui, QtCore

# Color Definition
default_not_modified_color       = QtGui.QColor(0, 0, 255, 200)
default_selected_color           = QtGui.QColor(180, 180, 180, 180)
default_not_selected_color       = QtGui.QColor(255, 255, 255, 100)
default_error_color              = QtGui.QColor(255, 0, 0, 255)    
default_selected_error_color     = QtGui.QColor(0, 0, 0, 255)
default_not_selected_error_color = QtGui.QColor(100, 0, 0, 255)

#Shape definition
default_corner_radius = 5.0
default_margin        = 3.0
#optimisation : paths are cached and recreated only when the
#geometry changes or no path exists for the object.
default_paths         = weakref.WeakKeyDictionary()


def default_dataflow_paint(owner, painter, option, widget):
    global default_paths
    path = default_paths.get(owner, None)
    rect = owner.rect() 
    if(path is None or owner.shapeChanged):
        path = QtGui.QPainterPath()
        top = owner._inPortLayout().geometry().center().y()
        bottom = owner._outPortLayout().geometry().center().y()
        rect.setTop(top)
        rect.setBottom(bottom)
        path.addRoundedRect(rect, default_corner_radius, default_corner_radius)
        owner.shapeChanged = False
        default_paths[owner] = path

    painter.setPen(QtCore.Qt.NoPen)
    painter.setBrush(QtGui.QColor(100, 100, 100, 50))
    path.moveTo(3.0,3.0)
    painter.drawPath(path)
    path.moveTo(0.0,0.0)
    pen = QtGui.QPen(QtCore.Qt.black, 1)

    userColor = owner.get_view_data("userColor")
    if( userColor is None ):
        owner.store_view_data("useUserColor", False)

    if hasattr(owner.vertex(), 'raise_exception'):
        color = default_error_color
        if(owner.isSelected()):
            pen = QtGui.QPen(QtCore.Qt.red, 1)
            secondcolor = default_selected_error_color
        else:
            secondcolor = default_not_selected_error_color                
    else:
        if(owner.isSelected()):
            pen = QtGui.QPen(QtGui.QColor(180, 180, 255, 255), 1)
            color = default_selected_color
        elif(owner.get_view_data("useUserColor")):
            color=QtGui.QColor(*userColor)
        else:
            color = default_not_selected_color

    if(owner.get_view_data("useUserColor")):
        secondcolor=QtGui.QColor(*userColor)
    elif(owner.vertex().user_application):
        secondcolor = QtGui.QColor(255, 144, 0, 200)
    else:
        secondcolor = default_not_modified_color

    # Draw Box
    gradient = QtGui.QLinearGradient(0, 0, 0, 100)
    gradient.setColorAt(0.0, color)
    gradient.setColorAt(0.8, secondcolor)
    painter.setBrush(QtGui.QBrush(gradient))

    painter.setPen(pen)
    painter.drawPath(path)

    if(owner.vertex().block):
        painter.setBrush(QtGui.QBrush(QtCore.Qt.BDiagPattern))
        painter.drawPath(path)
