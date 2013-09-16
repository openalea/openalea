# -*- python -*-
#
#       LPy manager applet.
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

from openalea.oalab.applets.texteditor import TextEditor
from openalea.lpy import Lsystem, AxialTree, registerPlotter
from openalea.lpy.gui import documentation as doc_lpy
from openalea.vpltk.qt import QtCore

class LPyApplet(object):
    def __init__(self, session, name="script.lpy", script=""):
        super(LPyApplet, self).__init__()
        self._widget = TextEditor(session=session)
        self._widget.applet = self
        self.session = session
        self.name = name

        script = self.filter_old_lpy_file(script)
        self.widget().set_text(script)

        self.lsys = Lsystem()
        self.code = str()
        # TODO self.name = ""
        self.axialtree = AxialTree()
        
        self.lastIter = -1
        
    def focus_change(self):
        """
        Set doc string in Help widget when focus changed
        """
        txt = doc_lpy.getSpecification()
        self.session.help.setText(txt)
        
    def filter_old_lpy_file(self, script):
        """
        Permit to open old LPy in removing initialisation part
        
        :param: script to filter (str)
        :return: lpy script (str) without end begining with "###### INITIALISATION ######"
        """
        if script is None: script = ""
        if not "###### INITIALISATION ######" in script:
            return str(script)
        else:
            return str(script).split("###### INITIALISATION ######")[0]

    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget

    def run(self):
        code = str(self.widget().get_text())
        # If code has changer since the last step
        if code != self.code:
            param = dict(self.session.scene_widget.getScene())
            # setCode method set the lastIterationNb to zero
            # So, if you change code, next step will do a 'reinit()'
            self.lsys.setCode(code)
            self.code = code
            
        self.axialtree = self.lsys.iterate()
        new_scene = self.lsys.sceneInterpretation(self.axialtree)
        self.session.scene_widget.getScene()["lpy_scene"] = new_scene
        
    def step(self):
        code = str(self.widget().get_text())
        # If code has changer since the last step
        if code != self.code:
            param = dict(self.session.scene_widget.getScene())
            # /!\ setCode method set the lastIterationNb to zero
            # So, if you change code, next step will do a 'reinit()'
            self.lsys.setCode(code)
            self.code = code
            
        if self.lsys.getLastIterationNb() == 0:
            # If step 0 : print axiom
            if self.lastIter == -1:
                self.axialtree = self.lsys.axiom
            # If step 1 : print pre step but lastIterationNb is still to 0
            elif self.lastIter == 0:
                self.axialtree = self.lsys.iterate(1)
            # If step 2 : print real first step and lastIterationNb go to 1
            else :        
                self.axialtree = self.lsys.iterate(self.lsys.getLastIterationNb()+2)
        # If step > 2
        else:
            self.axialtree = self.lsys.iterate(self.lsys.getLastIterationNb()+2)
        self.lastIter = self.lastIter + 1
        new_scene = self.lsys.sceneInterpretation(self.axialtree)
        if new_scene:
            self.session.scene_widget.getScene()["lpy_scene"] = new_scene
        
    def stop(self):
        # TODO : to implement
        # print "stop lpy"
        pass

    def animate(self):
        registerPlotter(self.session.viewer)
        self.step()
        self.lsys.animate()

    def reinit(self):
        self.lastIter = -1
        self.code = str(self.widget().get_text())
        # setCode set lastIterationNb to zero
        self.lsys.setCode(self.code)
        self.step()
