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

from openalea.oalab.editor.text_editor import RichTextEditor as Editor
from openalea.oalab.editor.highlight import Highlighter
from openalea.oalab.editor.lpy_lexer import LPyLexer
from openalea.lpy import Lsystem, AxialTree, registerPlotter
from openalea.lpy.gui import documentation as doc_lpy

def get_default_text():
    return """Axiom: 

derivation length: 1

production:

interpretation:

endlsystem
"""


class LPyApplet(object):
    def __init__(self, session, name="script.lpy", script=""):
        super(LPyApplet, self).__init__()
        self._widget = Editor(session=session)
        Highlighter(self._widget.editor, lexer=LPyLexer())
        self._widget.applet = self
        self.session = session
        self.name = name
        
        # dict is mutable =D
        # Usefull if you want change scene_name inside application
        self.context = dict()
        self.context["scene_name"] = "lpy_scene"
        
        if script == "":
            script = get_default_text()

        script, self.parameters = self.filter_old_lpy_file(script)
        self.widget().set_text(script)

        self.lsys = Lsystem()

        self.session.interpreter.locals['lsys'] = self.lsys
        self.session.interpreter.locals['turtle'] = self.session.control_panel.colormap_editor.getTurtle() 
        #self.lsys.context().turtle = self.session.control_panel.colormap_editor.getTurtle() 
        #from openalea.lpy.gui.materialeditor import MaterialEditor
        #from openalea.plantgl.all import Material,Color3
        #self.lsys.context().turtle.setMaterial(0,Material('Yellow',Color3(60,60,15),3,Color3(40,40,40),Color3(0,0,0),1,0))        
        #self.lsys.context().turtle.getColorList()
        #self.lsys.context().turtle = project.control.colormap   # material_editor = MaterialEditor(parent) material_editor.getTurtle(), material_editor.setTurtle(project.control.colormap)
        
        self.code = str()
        self.axialtree = AxialTree()
        
        self.lastIter = -1
        registerPlotter(self.session.viewer)
        
        # Link with color map from application
        if self.session.current_is_project():
            proj = self.session.project
            if proj.controls.has_key("color map"):    
                i = 0
                for color in self.session.project.controls["color map"] :
                    self.lsys.context().turtle.setMaterial(i, color)
                    i += 1
        
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
        and a dict which contain the context
        """
        ns = self.session.interpreter.user_ns
        context = dict()

        context["context"] = self.context
        context["cache"] = ns
        context["scene"] = self.session.scene_widget.getScene()
        if self.session.project.is_project():
            context["controls"] = self.session.project.controls
        
        if script is None: script = ""
        if not "###### INITIALISATION ######" in script:
            return str(script), context
        else:
            new_script = str(script).split("###### INITIALISATION ######")[0]
            #context = dict()
            return new_script, context

    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget
        
    def run_selected_part(self):
        """
        Run selected code like a PYTHON code (not LPy code).
        If nothing selected, run like LPy (not Python).
        """       
        code = self.widget().get_selected_text()
        if len(code) == 0:
            self.run()
        else:
            interp = self.session.shell.get_interpreter()
            user_ns = self.session.interpreter.user_ns
            interp.runcode(code)

    def run(self):
        """
        Run/iterate all the code (LPy and not PYTHON).
        """
        # Get code from application
        code = str(self.widget().get_text())
        # Get controls
        if self.session.project.is_project():
            self.parameters["controls"] = self.session.project.controls
        # set code (so reinit: step = 0)
        self.lsys.setCode(code, self.parameters)
            
        self.axialtree = self.lsys.iterate()
        new_scene = self.lsys.sceneInterpretation(self.axialtree)
        self.session.scene_widget.getScene()[self.context["scene_name"]] = new_scene
        
    def step(self):
        # Get code from application
        code = str(self.widget().get_text())

        # If code has changed since the last step
        if code != self.code:
            # /!\ setCode method set the lastIterationNb to zero
            # So, if you change code, next step will do a 'reinit()'
            self.lsys.setCode(code, self.parameters)
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
            self.session.scene_widget.getScene()[self.context["scene_name"]] = new_scene
        
    def stop(self):
        # TODO : to implement
        # print "stop lpy"
        #self.lsys.early_return = True
        #self.lsys.forceRelease()
        pass

    def animate(self):
        # Get code from application
        code = str(self.widget().get_text())
        if self.session.project.is_project():        
            self.parameters["controls"] = self.session.project.controls
        self.lsys.setCode(code, self.parameters)
        self.step()
        self.lsys.animate()

    def reinit(self):
        if self.session.project.is_project():
            self.parameters["controls"] = self.session.project.controls
        self.lastIter = -1
        self.code = str(self.widget().get_text())
        # setCode set lastIterationNb to zero
        self.lsys.setCode(self.code, self.parameters)
        self.step()
