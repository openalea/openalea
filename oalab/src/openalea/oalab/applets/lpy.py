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
from openalea.oalab.control.picklable_curves import geometry_2_piklable_geometry
from openalea.lpy import Lsystem, AxialTree, registerPlotter
from openalea.lpy.gui import documentation as doc_lpy
from openalea.lpy.__lpy_kernel__ import LpyParsing
from openalea.lpy.gui.objectmanagers import get_managers
from openalea.lpy.gui.scalar import ProduceScalar
from openalea.core import logger

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
            functions = context['__functions__']
            for n,c in functions: c.name = n
            functions = [ c for n,c in functions ]
            funcmanager = managers['Function']
            geoms +=  [(funcmanager,func) for func in functions]
        if context.has_key('__curves__') and lpy_code_version <= 1.0 :
            curves = context['__curves__']
            for n,c in curves: c.name = n
            curves = [ c for n,c in curves ]
            curvemanager = managers['Curve2D']
            geoms += [ (curvemanager,curve) for curve in curves ]
        if context.has_key('__parameterset__'):
            for panelinfo,objects in context['__parameterset__']:
                for typename,obj in objects:
                    visualparameters.append((managers[typename],obj))
        
        controls["color map"] = context.turtle.getColorList()
        for scalar in scalars:
        	controls[unicode(scalar.name)] = scalar
        for (manager, geom) in geoms:
            if geom != list():
                new_obj,new_name = geometry_2_piklable_geometry(manager, geom)
                controls[new_name] = new_obj
        for (manager, geom) in visualparameters:
            if geom != list():
                new_obj,new_name = geometry_2_piklable_geometry(manager, geom)
                controls[new_name] = new_obj
                
        return new_script, controls

class LPyApplet(object):   
    default_name = "L-System"
    default_file_name = "script.lpy"
    pattern = "*.lpy"
    extension = "lpy"
    icon = ":/lpy_images/resources/lpy/logo.png"
    
    def __init__(self, session, controller, parent=None, name="script.lpy", script=""):
        super(LPyApplet, self).__init__()
        logger.debug("init LPyApplet")
        self._widget = Editor(session=session, controller=controller, parent=parent)
        Highlighter(self._widget.editor, lexer=LPyLexer())
        logger.debug("Begin Highlight inside LPyApplet")
        self._widget.applet = self
        self.session = session
        self.controller = controller
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
            controller.project_manager._load_control()
        
        self.widget().set_text(script)
        self.lsystem = Lsystem()
        self.code = str()
        self.axialtree = AxialTree()

        registerPlotter(self.controller.applets['Viewer3D'])
        
        # Link with color map from application
        if self.session.project.controls.has_key("color map"):    
            i = 0
            for color in self.session.project.controls["color map"] :
                self.lsystem.context().turtle.setMaterial(i, color)
                i += 1
        
        self.session.interpreter.locals['lsystem'] = self.lsystem

        ## TODO : 
        #self.session.interpreter.locals['lstring'] =       
        
    def focus_change(self):
        """
        Set doc string in Help widget when focus changed
        """
        txt = doc_lpy.getSpecification()
        self.controller.applets['Help'].setText(txt)
         
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
            interp = self.controller.shell.get_interpreter()
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
            
        self.lsystem.setCode(code, self.parameters)
        self.axialtree = self.lsystem.iterate()
        
        new_scene = self.lsystem.sceneInterpretation(self.axialtree)
        scene_name = self.context["scene_name"]
        self.controller.scene[scene_name] = new_scene
        self.controller.applets['Viewer3D'].update_radius()
        
    def step(self, i=None):
        """
        Increase current lsystem from one step
        If you set i, lsystem will go to step number i.
        """
        
        # Get code from application
        code = str(self.widget().get_text())

        # If code has changed since the last step
        if code != self.code:
            # /!\ setCode method set the getLastIterationNb to zero
            # So, if you change code, next step will do a 'reinit()'
            self.parameters.update(self.session.project.controls)
            for parameter in self.parameters:
                if hasattr(self.parameters[parameter], "value"):
                    self.parameters[parameter] = self.parameters[parameter].value
            self.lsystem.setCode(code, self.parameters)
            self.code = code
            
        # if you are at derivation length, reinit
        if self.lsystem.getLastIterationNb() >= self.lsystem.derivationLength -1 :
            i = 0
        # clasical case: evolve one step
        if i is None:
            self.axialtree = self.lsystem.iterate(self.lsystem.getLastIterationNb()+2)    
        # if you set i to a number, directly go to this step.
        # it is used with i=0 to reinit
        else:
            self.axialtree = self.lsystem.iterate(i)    

        new_scene = self.lsystem.sceneInterpretation(self.axialtree)
        if new_scene:
            self.controller.scene[self.context["scene_name"]] = new_scene
        
    def stop(self):
        # TODO : to implement
        # print "stop lpy"
        #self.lsystem.early_return = True
        #self.lsystem.forceRelease()
        pass

    def animate(self):
        # Get code from application
        code = str(self.widget().get_text())
        self.parameters.update(self.session.project.controls)
        for parameter in self.parameters:
            if hasattr(self.parameters[parameter], "value"):
                self.parameters[parameter] = self.parameters[parameter].value    
        self.lsystem.setCode(code, self.parameters)
        self.step()
        self.lsystem.animate()
        self.controller.applets['Viewer3D'].update_radius()

    def reinit(self):
        self.step(0)

class LPyApplet2(object):
    def __init__(self, session, controller, parent=None, name="script.lpy", script=""):
        super(LPyApplet2, self).__init__()
        logger.debug("init LPyApplet")
        self.name = name
        self.intrepreter = session.interpreter
        # dict is mutable =D
        # Usefull if you want change scene_name inside application
        self.parameters = dict()
        self.parameters["scene_name"] = "lpy_scene"
        self.lsystem = Lsystem()
        self.axialtree = AxialTree()
        
        script, controls = import_lpy_file(script)
        self.code = script
        if self.code == "":
            self.code = get_default_text()
        self.parameters.update(controls)   
        
    def focus_change(self):
        """
        Set doc string in Help widget when focus changed
        """
        txt = doc_lpy.getSpecification()
        return txt
        
    def run_selected_part(self, txt):
        """
        Run selected code like a PYTHON code (not LPy code).
        If nothing selected, run like LPy (not Python).
        """       
        if len(txt) == 0:
            self.run()
        else:
            self.interpreter.runcode(txt)

    def run(self):
        """
        Run/iterate all the code (LPy and not PYTHON).
        """
        for parameter in self.parameters:
            if hasattr(self.parameters[parameter], "value"):
                self.parameters[parameter] = self.parameters[parameter].value
        
        self.lsystem.setCode(self.code, self.parameters)
        self.axialtree = self.lsystem.iterate()
        new_scene = self.lsystem.sceneInterpretation(self.axialtree)
        scene_name = self.parameters["scene_name"]
        
        return scene_name, new_scene
        
    def step(self, i=None):
        """
        Increase current lsystem from one step
        If you set i, lsystem will go to step number i.
        """
        for parameter in self.parameters:
            if hasattr(self.parameters[parameter], "value"):
                self.parameters[parameter] = self.parameters[parameter].value

        self.lsystem.setCode(self.code, self.parameters)

        # if you are at derivation length, reinit
        if self.lsystem.getLastIterationNb() >= self.lsystem.derivationLength -1 :
            i = 0
        # clasical case: evolve one step
        if i is None:
            self.axialtree = self.lsystem.iterate(self.lsystem.getLastIterationNb()+2)    
        # if you set i to a number, directly go to this step.
        # it is used with i=0 to reinit
        else:
            self.axialtree = self.lsystem.iterate(i)                

        new_scene = self.lsystem.sceneInterpretation(self.axialtree)
        scene_name = self.parameters["scene_name"]
        
        return scene_name, new_scene
        
    def stop(self):
        # TODO : to implement
        #self.lsystem.early_return = True
        #self.lsystem.forceRelease()
        pass

    def animate(self):
        # Get code from application
        for parameter in self.parameters:
            if hasattr(self.parameters[parameter], "value"):
                self.parameters[parameter] = self.parameters[parameter].value    
        self.lsystem.setCode(code, self.parameters)
        scene_name, new_scene = self.step()
        self.lsystem.animate()
        return scene_name, new_scene

    def reinit(self):
        return self.step(0)
