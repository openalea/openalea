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

from openalea.vpltk.qt import QtGui, QtCore
import webbrowser

default_text = """
<H1>Welcome in OpenAleaLab.</H1>

To begin, create or open an existing file or project.
"""

class Help(QtGui.QTextBrowser):
    """
    Widget which permit to display informations/help.
    Usefull in visualea or LPy.
    """
    def __init__(self):
        super(QtGui.QWidget, self).__init__() 
        
        actionHelpOpenAlea = QtGui.QAction(QtGui.QIcon(":/images/resources/openalealogo.png"),"OpenAlea", self)
        actionHelpGForge = QtGui.QAction(QtGui.QIcon(":/images/resources/gforge.png"),"Submit Bug", self)
        actionHelpTasks = QtGui.QAction(QtGui.QIcon(":/images/resources/gforge.png"),"See Tasks", self)
        
        QtCore.QObject.connect(actionHelpOpenAlea, QtCore.SIGNAL('triggered(bool)'),self.openWebsiteOpenalea)
        QtCore.QObject.connect(actionHelpGForge, QtCore.SIGNAL('triggered(bool)'),self.openOALabBugs)
        QtCore.QObject.connect(actionHelpTasks, QtCore.SIGNAL('triggered(bool)'),self.openOALabTasks)
        
        self._actions = [["Help","Website",actionHelpOpenAlea,0],
                         ["Help","Website",actionHelpGForge,0]]
        self.setText(default_text)                

    def actions(self):
        return self._actions
    
    def openWebsiteOpenalea(self):
        self.openWeb('http://openalea.gforge.inria.fr/dokuwiki/doku.php')
        
    def openOALabBugs(self):
        self.openWeb('https://gforge.inria.fr/tracker/?func=add&group_id=79&atid=13823')    
        
    def openOALabTasks(self):
        self.openWeb('https://gforge.inria.fr/pm/task.php?group_project_id=6971&group_id=79&func=browse')
        
    def openWeb(self, url):
        webbrowser.open(url)

    def mainMenu(self):
        """
        :return: Name of menu tab to automatically set current when current widget
        begin current.
        """
        return "Help"  

