# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#                       Thomas Cokelaer <thomas.cokelaer@sophia.inria.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
"""Custom Tooltip Widget"""

__license__ = "CeCILL v2"
__revision__ = " $Id$ "

from openalea.vpltk.qt import qt

class VertexTooltip( qt.QtGui.QWidget ):

    __WIDTH = 640
    __HEIGHT = 300

    __size = qt.QtCore.QSize(__WIDTH, __HEIGHT)

    def __init__(self, parent=None):
        #qt.QtGui.QWidget.__init__(self, parent, qt.QtCore.Qt.Popup)
        qt.QtGui.QWidget.__init__(self, parent, qt.QtCore.Qt.ToolTip)
        self.setWindowModality(qt.QtCore.Qt.ApplicationModal)
        self.setBackgroundRole(qt.QtGui.QPalette.ToolTipBase)
        self.setForegroundRole(qt.QtGui.QPalette.AlternateBase)

        #layouts
        mainLayout = qt.QtGui.QVBoxLayout()
        topLayout  = qt.QtGui.QGridLayout()
        topLayout.setVerticalSpacing(2)

        #widgets that display the labels
        self.__vNameWidget   = qt.QtGui.QLabel("Name :")
        self.__pNameWidget   = qt.QtGui.QLabel("Package :")
        self.__vAuthorWidget = qt.QtGui.QLabel("Author(s) :")

        #widgets that display the labels values
        self.__vNameValueWidget   = qt.QtGui.QLabel()
        self.__pNameValueWidget   = qt.QtGui.QLabel()
        self.__vAuthorValueWidget = qt.QtGui.QLabel()

        #long description
        __tooltipScroll = qt.QtGui.QScrollArea()
        self.__tooltipWidget = qt.QtGui.QLabel()
        __tooltipScroll.setWidget(self.__tooltipWidget)
        __tooltipScroll.setWidgetResizable(True)
        self.__tooltipWidget.setWordWrap(True)
        font = self.__tooltipWidget.font()
        font.setPointSize(10)
        self.__tooltipWidget.setFont(font)

        #now, the layout of labels:
        topLayout.addWidget(self.__vNameWidget, 0, 0, qt.QtCore.Qt.AlignLeft)
        topLayout.addWidget(self.__pNameWidget, 1, 0, qt.QtCore.Qt.AlignLeft)
        topLayout.addWidget(self.__vAuthorWidget, 2, 0, qt.QtCore.Qt.AlignLeft)

        #now, the layout of labels values:
        topLayout.addWidget(self.__vNameValueWidget, 0, 1, qt.QtCore.Qt.AlignRight)
        topLayout.addWidget(self.__pNameValueWidget, 1, 1, qt.QtCore.Qt.AlignRight)
        topLayout.addWidget(self.__vAuthorValueWidget, 2, 1, qt.QtCore.Qt.AlignRight)

        self.__vNameWidget.setSizePolicy(qt.QtGui.QSizePolicy.Preferred, qt.QtGui.QSizePolicy.Fixed)
        self.__pNameWidget.setSizePolicy(qt.QtGui.QSizePolicy.Preferred, qt.QtGui.QSizePolicy.Fixed)
        self.__vAuthorWidget.setSizePolicy(qt.QtGui.QSizePolicy.Preferred, qt.QtGui.QSizePolicy.Fixed)
        self.__vNameValueWidget.setSizePolicy(qt.QtGui.QSizePolicy.Preferred, qt.QtGui.QSizePolicy.Fixed)
        self.__pNameValueWidget.setSizePolicy(qt.QtGui.QSizePolicy.Preferred, qt.QtGui.QSizePolicy.Fixed)
        self.__vAuthorValueWidget.setSizePolicy(qt.QtGui.QSizePolicy.Preferred, qt.QtGui.QSizePolicy.Fixed)

        #main layout
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(__tooltipScroll)

        self.setLayout(mainLayout)

    #############
    # Accessors #
    #############
    def set_vertex_name(self, name):
        self.__vNameValueWidget.setText(name)

    def set_package_name(self, name):
        self.__pNameValueWidget.setText(name)

    def set_vertex_author(self, author):
        self.__vAuthorValueWidget.setText(author)

    def set_long_description(self, tooltip):
        self.__tooltipWidget.setText(tooltip)

    #################
    # Qt Size stuff #
    #################
    def size(self):
        return self.__size #size is fixed.

    def sizeHint(self):
        return self.__size #size is fixed.

    def leaveEvent(self, event):
        self.close()

    def paintEvent(self, event):
        painter = qt.QtGui.QPainter(self)
        painter.setPen(qt.QtCore.Qt.black)
        rect = qt.QtCore.QRect(self.rect())
        rect.adjust(0,0,-1,-1)
        painter.drawRect(rect)
        qt.QtGui.QWidget.paintEvent(self, event)
