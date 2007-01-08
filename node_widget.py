# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the GPL License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.gnu.org/licenses/gpl.txt
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#       This code is inspired from the puzzle QT4 example

__doc__="""
Default Node Widget and Subgraph Widget
"""

__license__= "GPL"
__revision__=" $Id$"



import sys
import math

from PyQt4 import QtCore, QtGui
from core.core import NodeWidget


class DefaultNodeWidget(QtGui.QWidget, NodeWidget):
    """
    Default implementation of a NodeWidget
    It displays the node contents
    """

    def __init__(self, node, mainwindow, parent):

        NodeWidget.__init__(self, node, mainwindow)
        QtGui.QWidget.__init__(self, parent)

        vboxlayout = QtGui.QVBoxLayout(self)

        self.label = QtGui.QLabel(self)
        self.label.setText(self.get_node_contents())

        vboxlayout.addWidget(self.label)

        

    def get_node_contents(self):
        """ Return a string representing the node internal dict """

        str = self.factory.get_tip()
        str += "\n"
        for (key, value) in self.node.items():
            str += "%s : %s\n"%(key, value)
        
        return str

    def notify(self):
        """ Function called by observed objects """
        
        self.label.setText(self.get_node_contents())



