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

from openalea.plantlab.picklable_curves import geometry_2_piklable_geometry
from openalea.oalab.session.session import Session
from openalea.lpy import Lsystem
from openalea.lpy.__lpy_kernel__ import LpyParsing
from openalea.lpy.gui.objectmanagers import get_managers
from openalea.lpy.gui.scalar import ProduceScalar
from openalea.plantlab.lpy import LPyModel, LPyFile
from openalea.oalab.service.help import display_help
import types

from openalea.oalab.gui.paradigm.python import PythonModelController


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


class LPyModelController(PythonModelController):
    default_name = LPyFile.default_name
    default_file_name = LPyFile.default_file_name
    pattern = LPyFile.pattern
    extension = LPyFile.extension
    icon = LPyFile.icon
    mimetype_data = LPyFile.mimetype
    mimetype_model = LPyModel.mimetype

    def __init__(self, **kwds):
        PythonModelController.__init__(self, **kwds)
        self.session = Session()

    def _default_editor(self):
        from openalea.oalab.editor.text_editor import RichTextEditor as Editor
        from openalea.oalab.editor.highlight import Highlighter
        editor = Editor(parent=self.parent)
        Highlighter(editor.editor)
        return editor

    def focus_change(self):
        """
        Set doc string in Help widget when focus changed
        """
        doc = self.model.get_documentation()
        display_help(doc)

    def update_world(self):
        # TODO: remove this hard link!
        # Update world ?
        world = self.session.world
        world[self.model.scene_name] = self.model.axialtree

    def namespace(self, **kwargs):
        ns = PythonModelController.namespace(self, **kwargs)
        # Extract one colorlist to set as THE colormap.
        # In case of ambiguity, select the one whose the name contains lpy.
        # Else select a random one.

        def select_colormap():
            # @GBY must move to plantgl or lpy
            from openalea.core.control.manager import ControlManager
            from openalea.plantgl.oaplugins.controls import to_material
            controls = ControlManager().namespace(interface='IColorList')
            for v in controls.values():
                return to_material(v)

        materials = select_colormap()
        if materials:
            for i, mat in enumerate(materials):
                self.model.lsystem.context().turtle.setMaterial(i, mat)
        ns['colormap'] = materials
        return ns

    def run(self, *args, **kwargs):
        ret = PythonModelController.run(self, *args, **kwargs)
        self.update_world()
        return ret

    def step(self, i=None, *args, **kwargs):
        self.apply()
        ret = self.model.step(i=i, *args, **kwargs)
        self.update_world()
        return ret

    def stop(self, *args, **kwargs):
        ret = PythonModelController.stop(self, *args, **kwargs)
        self.update_world()
        return ret

    def animate(self, *args, **kwargs):
        ret = PythonModelController.animate(self, *args, **kwargs)
        self.update_world()
        return ret

    def init(self, *args, **kwargs):
        ret = PythonModelController.init(self, *args, **kwargs)
        self.update_world()
        return ret

    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget
