# -*- python -*-
#
#       Python Manager applet
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
    
class PythonApplet(object):
    def __init__(self, session, name="script.py"):
        super(PythonApplet, self).__init__()
        self._widget = TextEditor(session=session)
        self._widget.applet = self
        self.session = session
        self.name = name
        self._step = None
        self._animate = None
        self._init = None
        
    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget
        
    def run(self):
        code = self.widget().get_text()
        interp = self.session.shell.get_interpreter()
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
