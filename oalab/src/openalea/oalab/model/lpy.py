# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
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
from openalea.oalab.model.model import Model
from openalea.oalab.control.picklable_curves import geometry_2_piklable_geometry
from openalea.lpy import Lsystem, AxialTree
from openalea.lpy.__lpy_kernel__ import LpyParsing
from openalea.lpy.gui.objectmanagers import get_managers
from openalea.lpy.gui.scalar import ProduceScalar
from openalea.lpy.gui import documentation as doc_lpy


def get_default_text():
    return """Axiom:

derivation length: 1

production:

interpretation:

endlsystem
"""


class LPyModel(Model):
    default_name = "LSystem"
    default_file_name = "script.lpy"
    pattern = "*.lpy"
    extension = "lpy"
    icon = ":/images/resources/logo.png"

    def __init__(self, name="script.lpy", code=None, inputs=[], outputs=[]):
        super(LPyModel, self).__init__()
        if code == "":
            code = get_default_text()

        # dict is mutable... It is useful if you want change scene_name inside application
        self.parameters = dict()
        self.context = dict()
        self.context["scene_name"] = "lpy_scene"
        self.lsystem = Lsystem()
        self.axialtree = AxialTree()
        self.code, control = import_lpy_file(code)
        # TODO: update control of the project with new ones

        self.lsystem.setCode(self.code, self.parameters)

    def get_documentation(self):
        """
        :return: a string with the documentation of the model
        """
        if self._doc:
            return self._doc
        else:
            return """
<H1><IMG SRC=""" + str(self.icon) + """
 ALT="icon"
 HEIGHT=25
 WIDTH=25
 TITLE="LPy logo">L-Py</H1>""" + doc_lpy.getSpecification()[13:]

    def repr_code(self):
        """
        :return: a string representation of model to save it on disk
        """
        return self.code

    def run(self, interpreter=None):
        """
        execute model thanks to interpreter
        """
        # TODO: get control from application and set them into self.parameters
        self.lsystem.setCode(self.code)
        self.axialtree = self.lsystem.iterate()
        return self.axialtree

    def reset(self, interpreter=None):
        """
        go back to initial step
        """
        return self.step(interpreter, 0)

    def step(self, interpreter=None, i=None):
        """
        execute only one step of the model
        """
        # if you are at derivation length, re-init
        if self.lsystem.getLastIterationNb() >= self.lsystem.derivationLength - 1:
            i = 0
        # clasical case: evolve one step
        if i is None:
            self.axialtree = self.lsystem.iterate(self.lsystem.getLastIterationNb() + 2)
        # if you set i to a number, directly go to this step.
        # it is used with i=0 to reinit
        else:
            self.axialtree = self.lsystem.iterate(i)
        return self.axialtree

    def stop(self, interpreter=None):
        """
        stop execution
        """
        # TODO : to implement
        pass

    def animate(self, interpreter=None):
        """
        run model step by step
        """
        self.step(interpreter)
        return self.lsystem.animate()


def get_default_text():
    return """Axiom:

derivation length: 1

production:

interpretation:

endlsystem
"""


def import_lpy_file(script):
    """
    Extract from an "old style" LPy file script part (str) and associated control (dict).
    Permit compatibility between LPy and OALab.

    :param: script to filter (str)
    :return: lpy script (str) without end begining with "###### INITIALISATION ######"
    and a dict which contain the control (dict)
    """
    control = dict()

    if script is None: script = ""
    beginTag = LpyParsing.InitialisationBeginTag
    if not beginTag in script:
        return str(script), control
    else:
        txts = str(script).split(beginTag)
        new_script = txts[0]
        context_to_translate = txts[1]
        context = Lsystem().context()
        context.initialiseFrom(beginTag + context_to_translate)

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
            for n, c in functions: c.name = n
            functions = [ c for n, c in functions ]
            funcmanager = managers['Function']
            geoms += [(funcmanager, func) for func in functions]
        if context.has_key('__curves__') and lpy_code_version <= 1.0 :
            curves = context['__curves__']
            for n, c in curves: c.name = n
            curves = [ c for n, c in curves ]
            curvemanager = managers['Curve2D']
            geoms += [ (curvemanager, curve) for curve in curves ]
        if context.has_key('__parameterset__'):
            for panelinfo, objects in context['__parameterset__']:
                for typename, obj in objects:
                    visualparameters.append((managers[typename], obj))

        control["color map"] = context.turtle.getColorList()
        for scalar in scalars:
        	control[unicode(scalar.name)] = scalar
        for (manager, geom) in geoms:
            if geom != list():
                new_obj, new_name = geometry_2_piklable_geometry(manager, geom)
                control[new_name] = new_obj
        for (manager, geom) in visualparameters:
            if geom != list():
                new_obj, new_name = geometry_2_piklable_geometry(manager, geom)
                control[new_name] = new_obj

        return new_script, control