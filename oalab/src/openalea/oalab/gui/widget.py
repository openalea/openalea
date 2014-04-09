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

from openalea.oalab.gui.logger import Logger
from openalea.oalab.applets.container import AppletContainer
from openalea.oalab.project.widgets import ProjectManager
from openalea.oalab.scene.view3d import Viewer
from openalea.oalab.gui.help import Help
from openalea.oalab.control.controlpanel import ControlPanel
from openalea.oalab.control.observerpanel import ObserverPanel
import abc

class WidgetABC:
    __metaclass__ = abc.ABCMeta
    def actions(self):
        """
        :return: list of actions to set in the menu.
        False means "no actions to set".
        """
        return False

    def mainMenu(self):
        """
        :return: Name of menu tab to automatically set current when current widget
        begin current.
        False means that widget will not change automatically the menu tab.
        """
        return False    

WidgetABC.register(ProjectManager)
# WidgetABC.register(SceneWidget)
WidgetABC.register(ControlPanel)
WidgetABC.register(ObserverPanel)
WidgetABC.register(Viewer)
WidgetABC.register(Logger)
WidgetABC.register(Help)
WidgetABC.register(AppletContainer)
