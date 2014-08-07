# -*- python -*-
# 
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = ""

from openalea.vpltk.qt import QtCore, QtGui

class GoToWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(GoToWidget, self).__init__()
        self.editor = parent
        self.setMinimumSize(100,100)
        self.setWindowTitle("Go To Line")

        self.actionGo = QtGui.QAction("Go to line", self)
        self.lineEdit = QtGui.QLineEdit()
        self.btnGo = QtGui.QToolButton()        
        self.btnGo.setDefaultAction(self.actionGo)
        
        QtCore.QObject.connect(self.actionGo, QtCore.SIGNAL('triggered(bool)'),self.go)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL('returnPressed()'),self.go)        
        
        layout = QtGui.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignLeft)
        
        layout.addWidget(self.lineEdit,0,0)
        layout.addWidget(self.btnGo,0,1)
        
        self.setLayout(layout)        
        self.hide()
        
    def go(self):
        lineno = self.lineEdit.text()
        if int(lineno) > 0:
            self.editor.go_to_line(int(lineno))
            
        