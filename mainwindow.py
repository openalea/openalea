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

__doc__="""
QT4 Main window 
"""

__license__= "GPL"
__revision__=" $Id$ "


from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL

import ui_mainwindow
from pycutext import PyCutExt

class MainWindow(  QtGui.QMainWindow, ui_mainwindow.Ui_MainWindow) :

    def __init__(self, model, globals=None, parent=None):


        QtGui.QMainWindow.__init__(self, parent)
        ui_mainwindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)


        self.interpreterWidget = PyCutExt(locals=globals, parent=self.splitter)
        self.interpreterWidget.setObjectName("interpreterWidget")


        self.packageTreeView.setModel(model)


        self.connect(self.action_About, SIGNAL("activated()"), self.about)
        self.connect(self.action_Help, SIGNAL("activated()"), self.help)

        self.connect(self.action_Quit, SIGNAL("activated()"), self.quit)


    def about(self):
        """ Display About Dialog """

        mess = QtGui.QMessageBox.about(self, "About Visualea",
                                       "Visualea is part of the OpenAlea framework.\n\n"+
                                       u"Copyright \xa9  2006 INRIA - CIRAD - INRA\n"+
                                       "This Software is distributed under the GPL License\n\n"+
                                       
                                       "Visit http://openalea.gforge.inria.fr\n")

    def help(self):
        """ Display help """
        pass

    def quit(self):
        """ Quit Application """

        self.close()


