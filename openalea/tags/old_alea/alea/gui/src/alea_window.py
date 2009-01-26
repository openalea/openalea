# -*- coding: utf-8 -*-
"""
Module implementing the main window of the ALEA application.

:author: Barbier de Reuille Pierre, Dones Nicolas, Chaubert Florence
:version: 0.1
:since: 08/11/2005
"""

import sys
from PyQt4 import QtCore, QtGui

from alea_workspace import WSCanvas
from alea_base_window import Ui_BaseWnd


class AleaWnd(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.ui = Ui_BaseWnd()
        self.ui.setupUi(self)
	
	# Fill the package tabs
	eframe = self.explore_frame.page( 0 )
	self.pkg_explore = PkgExplorer(eframe, name = "Package Explorer")
	eframe.layout().add( self.pkg_explore )

	# Fill the objects tabs

	# Fill the file system tabs

        # Fill the workspace with an empty one
        wframe = self.ui.workspaces.widget( 0 )
        self.ui.wscanvas = WSCanvas( wframe, name = "WSCanvas" )
        self.ui.workspace_layout = QtGui.QHBoxLayout( wframe )
        self.ui.workspace_layout.addWidget( self.ui.wscanvas )



 
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	w = AleaWnd()
	w.show()
	sys.exit(app.exec_())
