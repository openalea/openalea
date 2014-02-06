# -*- python -*-
#
#       R Manager applet
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

from openalea.oalab.editor.text_editor import RichTextEditor as Editor
from openalea.oalab.editor.highlight import Highlighter
from openalea.vpltk.qt import QtCore
    
class RApplet(object):
    def __init__(self, session, controller, parent=None, name="script.R", script=""):
        super(RApplet, self).__init__()
        self._widget = Editor(session=session, controller=controller, parent=parent)
        Highlighter(self._widget.editor)
        self._widget.applet = self
        self.session = session
        self.controller = controller
        self.name = name
        self._step = None
        self._animate = None
        self._init = None
        
        # TODO : Do it only once
        self.controller.shell.runcode(source="%load_ext rmagic",hidden=True)
        
        self.widget().set_text(script)
        
    def focus_change(self):
        """
        Set doc string in Help widget when focus changed
        """
        txt = """
<H1>R language</H1>

more informations: http://www.r-project.org/
"""
        self.controller.applets['Help'].setText(txt)
        
    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget
        
    def run_selected_part(self):
        code = self.widget().get_selected_text()
        if len(code) == 0:
            code = self.widget().get_text()
        code = """%%R

""" + code
        interp = self.controller.shell.get_interpreter()
        user_ns = self.session.interpreter.user_ns
        interp.runcode(code)    
        
    def run(self):
        code = self.widget().get_text()
        code = """%%R

""" + code
        interp = self.controller.shell.get_interpreter()
        user_ns = self.session.interpreter.user_ns
        interp.runcode(code)
        
        self._init = user_ns.get("init")
        if not callable(self._init):
            self._init = None

        self._step = user_ns.get("step")
        if not callable(self._step):
            self._step = None
        
        self._animate = user_ns.get("animate")
        if not callable(self._animate):
            self._animate = None
            if self._step :
                def animate():
                    for i in range(5):
                        self._step()
                self._animate = animate
            
    def step(self):
        # TODO : get function from the current widget!
        if self._step:
            self._step()
        #print "step python"    
        
    def stop(self):
        # TODO : to implement
        # print "stop python"
        pass
    
    def animate(self):
        # TODO : get function from the current widget!
        if self._animate:
            self._animate()
        # print "animate python"

    def reinit(self):
        # TODO : get function from the current widget!
        if self._init:
            self._init()
        #print "re-init python"   
