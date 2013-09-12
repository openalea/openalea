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
__revision__ = "$Id: $"

from openalea.vpltk.qt import QtGui, QtCore
from openalea.plantgl.all import *
from PyQGLViewer import *
import sys


from openalea.deploygui.alea_install_gui import * 


class Store(QtGui.QWidget):
    """
    This class is used to search, install and upgrade packages.
    
    Warning!!! Will kill OALab!!!
    """
    
    def __init__(self,session):
        super(Store, self).__init__()
        self.show = False
        self.session = session
        self.actionShowHide = QtGui.QAction(QtGui.QIcon(""),"Show", self)
        self.actionLaunch = QtGui.QAction(QtGui.QIcon(""),"Launch", self)
        QtCore.QObject.connect(self.actionShowHide, QtCore.SIGNAL('triggered(bool)'),self.showhide)
        QtCore.QObject.connect(self.actionLaunch, QtCore.SIGNAL('triggered(bool)'),start_alea_install_gui)
        self._actions = ["Package Store",[#["Show",self.actionShowHide,0],
                                  ["Launch",self.actionLaunch,0]]]

    def showhide(self):
        """
        Show / Hide this widget
        """
        if self.show:
            self.session.storeDockWidget.hide()
            self.show = False
        else:
            self.session.storeDockWidget.show()
            self.session.storeDockWidget.raise_()
            self.show = True 
            
            
    def actions(self):
        """
        :return: list of actions to set in the menu.
        """
        return self._actions

    def mainMenu(self):
        """
        :return: Name of menu tab to automatically set current when current widget
        begin current.
        """
        return "Package Store" 
        
        
def start_alea_install_gui():    
    """
    Start the GUI to install packages.
    If the GUI use QT and a new version of QT has been installed, we need to start a new process
    which setup the environment (shared libs and so on).

    On darwin, for instance, the sudo command do not propagate the environment variables.
    So to update the env variables dynamically, we restart a new python process with the OpenAlea environment.
    
    
    
    Warning!!! Will kill OALab!!!
    
    """
    args = []
    #status = main_app(args)

    envdict = check_system_setuptools()

    if sys.platform.lower().startswith('win'):
        status = os.execle(sys.executable, sys.executable, "-c",
                  '"import sys; from openalea.deploygui import alea_install_gui;sys.argv="'+str(args)+'";alea_install_gui.main_app(sys.argv)"',
                  envdict)
    else:
        status = os.execle(sys.executable, sys.executable, "-c",
                  'import sys; from openalea.deploygui import alea_install_gui;sys.argv='+str(args)+';alea_install_gui.main_app(sys.argv)',
                  envdict)


    print "Update environment"

    if sys.platform.lower().startswith('win'):
        os.execl(sys.executable, sys.executable, '-c',
                  '"from openalea.deploy.command import set_env; set_env()"')
    else:
        os.execl(sys.executable, sys.executable, '-c',
                  'from openalea.deploy.command import set_env; set_env()')
    return status
