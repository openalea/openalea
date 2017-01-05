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

from Qt import QtCore, QtGui, QtWidgets

class VertexTooltip( QtWidgets.QWidget ):

    __WIDTH = 640
    __HEIGHT = 300

    __size = QtCore.QSize(__WIDTH, __HEIGHT)

    def __init__(self, parent=None):
        #QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.Popup)
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.ToolTip)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setBackgroundRole(QtWidgets.QPalette.ToolTipBase)
        self.setForegroundRole(QtWidgets.QPalette.AlternateBase)

        #layouts
        mainLayout = QtWidgets.QVBoxLayout()
        topLayout  = QtWidgets.QGridLayout()
        topLayout.setVerticalSpacing(2)

        #widgets that display the labels
        self.__vNameWidget   = QtWidgets.QLabel("Name :")
        self.__pNameWidget   = QtWidgets.QLabel("Package :")
        self.__vAuthorWidget = QtWidgets.QLabel("Author(s) :")

        #widgets that display the labels values
        self.__vNameValueWidget   = QtWidgets.QLabel()
        self.__pNameValueWidget   = QtWidgets.QLabel()
        self.__vAuthorValueWidget = QtWidgets.QLabel()

        #long description
        __tooltipScroll = QtWidgets.QScrollArea()
        self.__tooltipWidget = QtWidgets.QLabel()
        __tooltipScroll.setWidget(self.__tooltipWidget)
        __tooltipScroll.setWidgetResizable(True)
        self.__tooltipWidget.setWordWrap(True)
        font = self.__tooltipWidget.font()
        font.setPointSize(10)
        self.__tooltipWidget.setFont(font)

        #now, the layout of labels:
        topLayout.addWidget(self.__vNameWidget, 0, 0, QtCore.Qt.AlignLeft)
        topLayout.addWidget(self.__pNameWidget, 1, 0, QtCore.Qt.AlignLeft)
        topLayout.addWidget(self.__vAuthorWidget, 2, 0, QtCore.Qt.AlignLeft)

        #now, the layout of labels values:
        topLayout.addWidget(self.__vNameValueWidget, 0, 1, QtCore.Qt.AlignRight)
        topLayout.addWidget(self.__pNameValueWidget, 1, 1, QtCore.Qt.AlignRight)
        topLayout.addWidget(self.__vAuthorValueWidget, 2, 1, QtCore.Qt.AlignRight)

        self.__vNameWidget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.__pNameWidget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.__vAuthorWidget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.__vNameValueWidget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.__pNameValueWidget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.__vAuthorValueWidget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

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
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.black)
        rect = QtCore.QRect(self.rect())
        rect.adjust(0,0,-1,-1)
        painter.drawRect(rect)
        QtWidgets.QWidget.paintEvent(self, event)
