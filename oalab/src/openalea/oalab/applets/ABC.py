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

"""

"""

from openalea.oalab.applets.lpy import LPyApplet
from openalea.oalab.applets.python import PythonApplet
from openalea.oalab.applets.visualea import VisualeaApplet
import abc

class AppletABC:
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
        return "Simulation" 
    
    @abc.abstractmethod
    def save(self):
        """
        Save the current simulation oppened in the applet
        """
        pass
    
    @abc.abstractmethod    
    def run(self):
        """
        Run the current simulation oppened in the applet
        """
        pass
      
    def animate(self):
        """
        Run step by step the current simulation oppened in the applet
        """
        pass
        
    @abc.abstractmethod
    def step(self):
        """
        Run one step in the current simulation oppened in the applet
        """
        pass    
        
    def stop(self):
        """
        Stop the current simulation
        """
        pass
        
    def reinit(self):
        """
        Go to the step zero
        """
        pass

AppletABC.register(PythonApplet)
AppletABC.register(LPyApplet)
AppletABC.register(VisualeaApplet)
