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

import types
from copy import copy

from openalea.core.data import Data
from openalea.core.model import Model
from openalea.lpy import Lsystem, AxialTree
from openalea.lpy.__lpy_kernel__ import LpyParsing
from openalea.lpy.gui.objectmanagers import get_managers
from openalea.lpy.gui.scalar import ProduceScalar
from openalea.oalab.model.parse import parse_doc, InputObj, OutputObj, get_docstring, prepare_inputs
from openalea.plantlab.parse_model import parse_lpy
from openalea.plantlab.picklable_curves import geometry_2_piklable_geometry


def get_default_text():
    return """Axiom:

derivation length: 1

production:

interpretation:

endlsystem
"""

DEFAULT_DOC = """
<H1><IMG SRC=%s
 ALT="icon"
 HEIGHT=25
 WIDTH=25
 TITLE="Python logo">LPy code</H1>
"""


def adapt_axialtree(axialtree, lsystem):
    """
    Adapat an axialtree to be viewable in the world (add a method _repr_geom_)

    :param axialtree: axialtree to adapt
    :param lsystem: lsystem that can be used to create the 3d representation of axialtree
    :return: adapted axialtree
    """
    if hasattr(axialtree, '_repr_geom_'):
        return

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

from openalea.core.model import PythonModel


class LPyFile(Data):
    default_name = "LSystem"
    default_file_name = "script.lpy"
    pattern = "*.lpy"
    extension = "lpy"
    icon = ":/images/resources/logo.png"
    mimetype = "text/vnd-lpy"


class LPyModel(PythonModel):
    dtype = 'LSystem'
    mimetype = 'text/vnd-lpy'

    def __init__(self, *args, **kwargs):
        PythonModel.__init__(self, *args, **kwargs)
        if self.name is None:
            self.name = 'LPyModel'
        self._step = 1
        self.lsystem = Lsystem()
        self.axialtree = AxialTree()
        self.scene_name = self.name + '_scene'

        from openalea.lpy import registerPlotter
        from openalea.oalab.service.plot import get_plotters

        plotters = get_plotters()
        if len(plotters):
            registerPlotter(plotters[0])

    def __copy__(self):
        m = PythonModel.__copy__(self)
        m.set_code(self._initial_code)
        m.lsystem = self.lsystem
        m.axialtree = self.axialtree
        m.scene_name = self.scene_name
        return m

    def init(self, *args, **kwds):
        self._step = 1

        self._push_ns()
        self._fill_namespace(*args, **kwds)

        # BEGIN ACTUAL CODE RUN
        self.lsystem.setCode(str(self.code), self._ns)
        if "axiom" in self._ns:
            self.lsystem.axiom = self._ns['axiom']
        elif "lstring" in self._ns:
            self.lsystem.axiom = self._ns['lstring']
        self.axialtree = self.lsystem.axiom
        # END ACTUAL CODE RUN

        self._populate_ns()
        self._pop_ns()

        return self.output_from_ns(self._ns)

    def output_from_ns(self, namespace):
        # get outputs from namespace
        outputs = []
        if self.outputs_info:
            if len(self.outputs_info) > 0:
                for outp in self.outputs_info:
                    if outp.name.lower() in ["axialtree", "lstring"]:
                        outputs.append(self.axialtree)
                    elif outp.name.lower() == "lsystem":
                        outputs.append(self.lsystem)
                    elif outp.name.lower() == "scene":
                        outputs.append(self.lsystem.sceneInterpretation(self.axialtree))
                    elif outp.name in namespace:
                        outputs.append(namespace[outp.name])
                    else:
                        continue
                    # Add output to namespace
                    # if output is not in namespace, this line is not run (see "continue" above)
                    self._ns[outp.name] = outputs[-1]

        if len(outputs) == 0:
            return None
        elif len(outputs) == 1:
            return outputs[0]
        else:
            return outputs

    def run(self, *args, **kwds):
        nstep = kwds.pop('nstep', None)
        self.init(*args, **kwds)

        if nstep is None:
            self.axialtree = self.lsystem.iterate()
        else:
            self.axialtree = self.lsystem.iterate(nstep)

        self.lsystem.context().getNamespace(self._ns)
        self.outputs = self.output_from_ns(self._ns)
        return self.outputs

    def step(self, *args, **kwds):
        nstep = kwds.pop('nstep', None)

        if self._step > self.lsystem.derivationLength:
            self._step = 0

        if nstep is None:
            self.axialtree = self.lsystem.iterate(self._step)
        else:
            self.axialtree = self.lsystem.iterate(nstep)

        self.outputs = self.output_from_ns(self._ns)

        self._step += 1
        return self.outputs

    def animate(self, *args, **kwds):
        self.init()
        self.axialtree = self.lsystem.animate()
        self.outputs = self.output_from_ns(self._ns)
        self._step = self.lsystem.derivationLength + 1
        return self.outputs

    def set_code(self, code):
        """
        Set the content and parse it to get docstring, inputs and outputs info, some methods
        """
        self._initial_code, control = import_lpy_file(code)
        self._doc = get_docstring(code)
        docstring = parse_lpy(code)
        if docstring is not None:
            model, self.inputs_info, self.outputs_info = parse_doc(docstring)

        # Default input
        if self.inputs_info == []:
            self.inputs_info = [InputObj('lstring:IStr')]
        # Default output
        if self.outputs_info == []:
            self.outputs_info = [OutputObj("lstring:IStr")]

    def _set_code(self, code):
        self.set_code(code)

    def _set_axialtree(self, axialtree):
        self._axialtree = adapt_axialtree(axialtree, self.lsystem)

    code = property(fget=lambda self: self._initial_code, fset=_set_code)
    axialtree = property(fget=lambda self: self._axialtree, fset=_set_axialtree)


def import_lpy_file(script):
    """
    Extract from an "old style" LPy file script part (str) and associated control (dict).
    Permit compatibility between LPy and OALab.

    :param: script to filter (str)
    :return: lpy script (str) without end begining with "###### INITIALISATION ######"
    and a dict which contain the control (dict)
    """
    control = dict()

    if script is None:
        script = ""
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
            scalars = [ProduceScalar(v) for v in scalars_]
        if context.has_key('__functions__') and lpy_code_version <= 1.0:
            functions = context['__functions__']
            for n, c in functions:
                c.name = n
            functions = [c for n, c in functions]
            funcmanager = managers['Function']
            geoms += [(funcmanager, func) for func in functions]
        if context.has_key('__curves__') and lpy_code_version <= 1.0:
            curves = context['__curves__']
            for n, c in curves:
                c.name = n
            curves = [c for n, c in curves]
            curvemanager = managers['Curve2D']
            geoms += [(curvemanager, curve) for curve in curves]
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
