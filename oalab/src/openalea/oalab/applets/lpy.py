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
from openalea.oalab.project.widgets import geometry_2_piklable_geometry
from openalea.lpy import Lsystem, AxialTree, registerPlotter
from openalea.lpy.gui import documentation as doc_lpy
from openalea.lpy.__lpy_kernel__ import LpyParsing
from openalea.lpy.gui.objectmanagers import get_managers
from openalea.lpy.gui.scalar import ProduceScalar
from openalea.core import logger

from copy import deepcopy

def get_default_text():
    return """Axiom: 

derivation length: 1

production:

interpretation:

endlsystem
"""

def import_lpy_file(script):
    """
    Extract from an "old style" LPy file script part (str) and associated controls (dict).
    Permit compatibility between LPy and OALab.
    
    :param: script to filter (str)
    :return: lpy script (str) without end begining with "###### INITIALISATION ######"
    and a dict which contain the controls (dict)
    """
    new_context = dict()
    controls = dict()

    if script is None: script = ""
    beginTag = LpyParsing.InitialisationBeginTag
    if not beginTag in script:
        return str(script), controls
    else:
        txts = str(script).split(beginTag)
        new_script = txts[0]
        context_to_translate = txts[1]
        context = Lsystem().context()
        try:
            context.initialiseFrom(beginTag+context_to_translate)
        except:
            logger.warning("Can't decode lpy file")
           
        managers = get_managers()
        visualparameters = []
        scalars = []
        functions = []
        curves = []
        geoms = []
        
        lpy_code_version = 1.0
        if context.has_key('__lpy_code_version__'):
            lpy_code_version = context['__lpy_code_version__']
        if context.has_key('__scalars__'):
            scalars_ = context['__scalars__']   
            scalars = [ ProduceScalar(v) for v in scalars_ ]            
        if context.has_key('__functions__') and lpy_code_version <= 1.0 :
            functions_ = context['__functions__']
            for n,c in functions_: c.name = n
            functions = [ c for n,c in functions ]
            funcmanager = managers['Function']
            geoms +=  [ ({'name':'Functions'}, [(funcmanager,func) for n,func in functions]) ]
        if context.has_key('__curves__') and lpy_code_version <= 1.0 :
            curves_ = context['__curves__']
            for n,c in curves_: c.name = n
            curves = [ c for n,c in curves ]
            curvemanager = managers['Curve2D']
            geoms += [ ({'name':'Curve2D'}, [(curvemanager,curve) for n,curve in curves]) ]
        if context.has_key('__parameterset__'):
            for panelinfo,objects in context['__parameterset__']:
                for typename,obj in objects:
                    visualparameters.append((managers[typename],obj))
        
        controls["color map"] = context.turtle.getColorList()
        for scalar in scalars:
        	controls[unicode(scalar.name)] = scalar
        for (manager, geom) in geoms:
            new_obj,new_name = geometry_2_piklable_geometry(manager, geom)
            controls[new_name] = new_obj
        for (manager, geom) in visualparameters:
            new_obj,new_name = geometry_2_piklable_geometry(manager, geom)
            controls[new_name] = new_obj
                
        return new_script, controls

class LPyApplet(object):
    def __init__(self, session, name="script.lpy", script=""):
        super(LPyApplet, self).__init__()
        logger.debug("init LPyApplet")
        self._widget = Editor(session=session)
        Highlighter(self._widget.editor, lexer=LPyLexer())
        logger.debug("Begin Highlight inside LPyApplet")
        self._widget.applet = self
        self.session = session
        self.name = name
        
        # dict is mutable =D
        # Usefull if you want change scene_name inside application
        self.parameters = dict()
        self.context = dict()
        self.context["scene_name"] = "lpy_scene"
        
        if script == "":
            script = get_default_text()

        script, controls = import_lpy_file(script)
        if self.session.project is not None:
            self.session.project.controls.update(controls)
            # for parameter in self.parameters:
                # if hasattr(self.parameters[parameter], "value"):
                    # self.parameters[parameter] = self.parameters[parameter].value
            session.project_widget._load_control()
        
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
        if self.session.project.controls.has_key("color map"):    
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
            #user_ns = self.session.interpreter.user_ns
            interp.runcode(code)

    def run(self):
        """
        Run/iterate all the code (LPy and not PYTHON).
        """
        # Get code from application
        code = str(self.widget().get_text())
        # Get controls
        self.parameters.update(self.session.project.controls)
        for parameter in self.parameters:
            if hasattr(self.parameters[parameter], "value"):
                self.parameters[parameter] = self.parameters[parameter].value
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
            self.parameters.update(self.session.project.controls)
            for parameter in self.parameters:
                if hasattr(self.parameters[parameter], "value"):
                    self.parameters[parameter] = self.parameters[parameter].value
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
        self.parameters.update(self.session.project.controls)
        for parameter in self.parameters:
            if hasattr(self.parameters[parameter], "value"):
                self.parameters[parameter] = self.parameters[parameter].value    
        self.lsys.setCode(code, self.parameters)
        self.step()
        self.lsys.animate()

    def reinit(self):
        self.parameters.update(self.session.project.controls)
        for parameter in self.parameters:
            if hasattr(self.parameters[parameter], "value"):
                self.parameters[parameter] = self.parameters[parameter].value    
        self.lastIter = -1
        self.code = str(self.widget().get_text())
        # setCode set lastIterationNb to zero
        self.lsys.setCode(self.code, self.parameters)
        self.step()
