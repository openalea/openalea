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
# from openalea.oalab.model.model import Model
from openalea.core.model import Model
from openalea.oalab.model.parse import parse_doc, parse_lpy, OutputObj, InputObj, get_docstring, prepare_inputs
from openalea.oalab.control.picklable_curves import geometry_2_piklable_geometry
from openalea.lpy import Lsystem, AxialTree
from openalea.lpy.__lpy_kernel__ import LpyParsing
from openalea.lpy.gui.objectmanagers import get_managers
from openalea.lpy.gui.scalar import ProduceScalar
from openalea.lpy.gui import documentation as doc_lpy
import collections
import types


def get_default_text():
    return """Axiom:

derivation length: 1

production:

interpretation:

endlsystem
"""


def adapt_axialtree(axialtree, lsystem):
    """
    Adapat an axialtree to be viewable in the world (add a method _repr_geom_)

    :param axialtree: axialtree to adapt
    :param lsystem: lsystem that can be used to create the 3d representation of axialtree
    :return: adapted axialtree
    """
    def repr_geom(self):
        return self.__scene

    scene = lsystem.sceneInterpretation(axialtree)
    axialtree.__scene = scene
    axialtree._repr_geom_ = types.MethodType(repr_geom, axialtree)

    return axialtree


class LsysObj(object):
    def __init__(self, lsystem, axialtree, name=""):
        """
        Object that can be interpreted in the world.

        It contain the lsystem, the resulting axiatree and a name.
        The lsysytem and the axialtree are used to convert object into PlantGL scene with _repr_geom_ method.
        """
        self.lsystem = lsystem
        self.axialtree = axialtree
        self.name = name

    def _repr_geom_(self):
        return self.lsystem.sceneInterpretation(self.axialtree)


class LPyModel(Model):
    default_name = "LSystem"
    default_file_name = "script.lpy"
    pattern = "*.lpy"
    extension = "lpy"
    icon = ":/images/resources/logo.png"
    mimetype = "text/vnd-lpy"

    def __init__(self, **kwargs):
        super(LPyModel, self).__init__(**kwargs)
        self.temp_axiom = None
        self.second_step = False # Hack, see self.step
        # dict is mutable... It is useful if you want change scene_name inside application
        self.context = dict()
        self.scene_name = self.filename + "_scene"
        self.context["scene_name"] = self.scene_name
        self.lsystem = Lsystem()
        self.axialtree = AxialTree()
        self.axialtree = adapt_axialtree(self.axialtree, self.lsystem)
        # TODO: update control of the project with new ones

        from openalea.lpy import registerPlotter
        from openalea.oalab.service.plot import get_plotters

        plotters = get_plotters()
        if len(plotters):
            registerPlotter(plotters[0])
        # print "p: ", plotters

        # for plotter in plotters:
        #     print "plotter: ", plotter
        #     registerPlotter(plotter)

        # If path doesn't exists, that means all content is in memory (passed in constructor for example)
        # So we need to parse it
        if not self.exists():
            self.parse()

    def get_documentation(self):
        """
        :return: a string with the documentation of the model
        """
        self.read()
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

    def run(self, *args, **kwargs):
        """
        execute entire model
        """
        # TODO: get control from application and set them into self.context
        ns = self._prepare_namespace()
        self._set_inputs(*args, **kwargs)
        self.inputs.update(ns)

        self.context.update(self.inputs)
        self.lsystem.setCode(str(self.code), self.context)
        if self.temp_axiom is not None:
            self.lsystem.axiom = self.temp_axiom
            self.temp_axiom = None

        self.axialtree = self.lsystem.iterate()

        self.lsystem.context().getNamespace(self.context)

        self._set_output_from_ns(self.context)

        # new_scene = self.lsystem.sceneInterpretation(self.axialtree)
        if "scene_name" in self.context:
            self.scene_name = self.context["scene_name"]

        self.axialtree = adapt_axialtree(self.axialtree, self.lsystem)

        return self.outputs

    def init(self, *args, **kwargs):
        """
        go back to initial step
        """
        self.step(i=0, *args, **kwargs)
        return self.outputs

    def step(self, i=None, *args, **kwargs):
        """
        execute only one step of the model
        """
        ns = self._prepare_namespace()
        self._set_inputs(*args, **kwargs)
        self.inputs.update(ns)
        self.context.update(self.inputs)

        default_text = """Lsystem:
Axiom:
derivation length: 1
production:
endlsystem"""
        current_text = str(self.lsystem.code())

        # If never initialized
        # if self.code.replace(' ','') != self.lsystem.code().replace(' ',''):
        if current_text.replace(' ','') == default_text.replace(' ',''):
            self.lsystem.setCode(str(self.code), self.context)
            if self.temp_axiom is not None:
                self.lsystem.axiom = self.temp_axiom
                self.temp_axiom = None

        # if you are at derivation length, re-init
        if self.lsystem.getLastIterationNb() >= self.lsystem.derivationLength - 1:
            i = 0
            self.second_step = False
        # clasical case: evolve one step
        if i is None:
            # Warning: getLastIterationNb return 0,0,1,2,3,4,...
            # Hack: after the first "0" we put second_step to True
            # So iterations are 0, 1, 2, 3, 4, ...
            # Hack
            if self.second_step:
                self.axialtree = self.lsystem.iterate(self.lsystem.getLastIterationNb() + 2)
            else:
                self.axialtree = self.lsystem.iterate(self.lsystem.getLastIterationNb() + 1)
                self.second_step = True
        # if you set i to a number, directly go to this step.
        # it is used with i=0 to init
        else:
            self.axialtree = self.lsystem.iterate(i)

        self.lsystem.context().getNamespace(self.context)

        self._set_output_from_ns(self.context)

        # new_scene = self.lsystem.sceneInterpretation(self.axialtree)
        if "scene_name" in self.context:
            self.scene_name = self.context["scene_name"]

        self.axialtree = adapt_axialtree(self.axialtree, self.lsystem)

        return self.outputs

    def stop(self, *args, **kwargs):
        """
        stop execution
        """
        # TODO : to implement
        self.axialtree = adapt_axialtree(self.axialtree, self.lsystem)

        return self.outputs

    def animate(self, *args, **kwargs):
        """
        run model step by step
        """
        self._set_inputs(*args, **kwargs)
        self.context.update(self.inputs)
        self.step(*args, **kwargs)
        self.axialtree = self.lsystem.animate()

        self.lsystem.context().getNamespace(self.context)

        self._set_output_from_ns(self.context)

        if "scene_name" in self.context:
            self.scene_name = self.context["scene_name"]

        self.axialtree = adapt_axialtree(self.axialtree, self.lsystem)

        return self.outputs

    def _set_output_from_ns(self, namespace):
        # get outputs from namespace
        if self.outputs_info:
            self.outputs = []
            if len(self.outputs_info) > 0:
                for outp in self.outputs_info:
                    if outp.name.lower() in ["axialtree", "lstring"]:
                        self._outputs.append(self.axialtree)
                    elif outp.name.lower() == "lsystem":
                        self._outputs.append(self.lsystem)
                    elif outp.name.lower() == "scene":
                        self._outputs.append(self.lsystem.sceneInterpretation(self.axialtree))
                    elif outp.name in namespace:
                        self._outputs.append(namespace[outp.name])

    def parse(self):
        """
        Set the content and parse it to get docstring, inputs and outputs info, some methods
        """
        self._content, control = import_lpy_file(self._content)
        content = self._content
        self._doc = get_docstring(content)
        docstring = parse_lpy(content)
        if docstring is not None:
            model, self.inputs_info, self.outputs_info = parse_doc(docstring)

        # Default input
        # if self.inputs_info == []:
        #     self.inputs_info = [InputObj('lstring:IStr=""')]
        # Default output
        if self.outputs_info == []:
            self.outputs_info = [OutputObj("lstring:IStr")]


    def _set_inputs(self, *args, **kwargs):
        self.inputs = prepare_inputs(self.inputs_info, name=self.filename, *args, **kwargs)
        if "axiom" in self.inputs.keys():
            self.temp_axiom = self.inputs["axiom"]
            del self.inputs["axiom"]
        if "lstring" in self.inputs.keys():
            self.temp_axiom = self.inputs["lstring"]
            del self.inputs["lstring"]

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
