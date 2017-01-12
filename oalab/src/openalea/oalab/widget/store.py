# -*- python -*-
#
#       Store Class
#       Use it to install new packages
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
__revision__ = "$Id$"

from openalea.deploygui.alea_install_gui import MainWindow as MainWindowAleaInstall
from openalea.deploygui.alea_install_gui import *

import sys


class Store(MainWindowAleaInstall):

    """
    This class is used to search, install and upgrade packages.

    Warning!!! Will kill OALab!!!
    """

    def __init__(self, parent=None):
        # Save stdout and stderr because MainWindowAleaInstall try to redirect it.
        oldstdout = sys.stdout
        oldstderr = sys.stderr
        super(Store, self).__init__()

        self.setAccessibleName("Store")
        # Restore stdout and stderr
        sys.stdout = oldstdout
        sys.stderr = oldstderr
        # Hide old logger
        self.logText.hide()
        self.label_3.hide()

        self._show = False
        #self.actionShowHide = QtGui.QAction(QtGui.QIcon(":/images/resources/store.png"),"Show/Hide", self)
        #self.actionShowHide.triggered[bool].connect(self.showhide)
        #self._actions = [["Help","Package Store",self.actionShowHide,0]]
        self._actions = None

    '''
    def showhide(self):
        """
        Show / Hide this widget
        """
        # TODO : do the "setVisible" on the dock widget and not on the widget inside the dock (cf mainwindow._dockwidgets["Store"])
        self.setVisible(self.show)
        self.show = not self.show'''

    def actions(self):
        """
        :return: list of actions to set in the menu.
        """
        return self._actions

    def toolbar_actions(self):
        return []

    def mainMenu(self):
        """
        :return: Name of menu tab to automatically set current when current widget
        begin current.
        """
        return "Package Store"
