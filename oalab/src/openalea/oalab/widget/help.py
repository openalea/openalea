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

from Qt import QtWidgets, QtGui, QtCore

import resources_rc  # do not remove this import else icon are not drawn
import webbrowser

from openalea.oalab.widget.preferences import PreferenceWidget
from openalea.oalab.utils import ModalDialog
from openalea.oalab.service.help import register_helper

default_text2 = """
<H1>Welcome in OpenAleaLab.</H1>

To begin, <b>choose your lab</b> or open an existing file or project:
<ul>
<li>  <b>MiniLab</b> is a minimal environnement with only a text editor and a shell.</li>
<li>  <b>3DLab</b> is an environnement to work on 3D Objects.</li>
<li>  <b>PlantLab</b> is an environnement to work on entire plant.</li>
<li>  <b>TissueLab</b>is an environnement to work on tissue part of plants.</li>
<li>  Open an existing project.</li>
<li>  Restore previous session.</li>
</ul>
"""

default_text = """
<H1>Welcome in OpenAleaLab.</H1>

<p>
This lab permit to create and execute virtual experiments that use different modelling paradigms.
</p>
<p>
To begin, you can work in this temporary project, write code, execute it...
If you want to save your project, please use "<b>Save As</b>" button in "<b>Project</b>" menu to rename/move your project.
</p>
<p>
Examples of project are available in pressing "<b>Open</b>" button in "<b>Project</b>" menu.
Then go into "oalab_examples" repository and select a project.
</p>
"""


class HelpWidget(QtWidgets.QTextBrowser):

    """
    Widget which permit to display informations/help.
    Usefull in visualea or LPy.
    """

    def __init__(self, session=None, controller=None, parent=None):
        super(HelpWidget, self).__init__(parent=parent)
        self.setAccessibleName("HelpWidget")

        actionHelpOpenAlea = QtWidgets.QAction(
            QtGui.QIcon(":/images/resources/openalealogo.png"), "OpenAlea WebSite", self)
        actionHelpGForge = QtWidgets.QAction(QtGui.QIcon(":/images/resources/git.png"), "Submit Issues", self)
        actionHelpTasks = QtWidgets.QAction(QtGui.QIcon(":/images/resources/gforge.png"), "See Tasks", self)
        actionEditPref = QtWidgets.QAction(QtGui.QIcon(":/images/resources/node.png"), "Preferences", self)

        self.connect(actionHelpOpenAlea, QtCore.SIGNAL('triggered(bool)'), self.openWebsiteOpenalea)
        self.connect(actionHelpGForge, QtCore.SIGNAL('triggered(bool)'), self.openOALabIssues)
        self.connect(actionHelpTasks, QtCore.SIGNAL('triggered(bool)'), self.openOALabTasks)
        actionEditPref.triggered.connect(self.open_preferences)

        self._actions = [["Help", "Website", actionHelpOpenAlea, 0],
                         ["Help", "Website", actionHelpGForge, 0],
                         ["Help", "Settings", actionEditPref, 0],
                         ]
        self.setText(default_text)
        register_helper(self)

    def actions(self):
        return self._actions

    def toolbar_actions(self):
        return self.actions()

    def menus(self):
        menu = QtWidgets.QMenu('Help', self)
        actions = [action[2] for action in self.actions()]
        menu.addActions(actions)
        return [menu]

    def openWebsiteOpenalea(self):
        self.openWeb('http://openalea.github.io')

    def openOALabIssues(self):
        self.openWeb('https://github.com/openalea/openalea/issues/new')

    def openOALabTasks(self):
        self.openWeb('https://gforge.inria.fr/pm/task.php?group_project_id=6971&group_id=79&func=browse')

    def openWeb(self, url):
        webbrowser.open(url)

    def open_preferences(self):
        preferences = PreferenceWidget()
        dialog = ModalDialog(preferences)
        if dialog.exec_():
            preferences.update_config(save=True)
            # preferences.close()

    def mainMenu(self):
        """
        :return: Name of menu tab to automatically set current when current widget
        begin current.
        """
        return "Help"

    def set_text(self, text):
        self.setText(text)
