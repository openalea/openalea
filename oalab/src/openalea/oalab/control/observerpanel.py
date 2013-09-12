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
__revision__ = "$Id: $"

from openalea.vpltk.qt import QtGui, QtCore

class ObserverPanel(QtGui.QWidget):
    """
    Widget to display observers
    """
    def __init__(self):
        super(QtGui.QWidget, self).__init__() 
        'connected to current_project.observer'
        pass
        
    def add(self):
        pass
    
    def delete(self):
        pass
        
    def rename(self):
        pass
    
    def diplay_thumbnails(self):    
        """
        Display thumbnails of all controls.
        - List controls
        - Call control.thumbnail() on each one
        """ 


