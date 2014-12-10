# -*- python -*-
#
#       Visualea Manager applet
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#                       Guillaume Baty <guillaume.baty@inria.fr>
#                       Christophe Pradal <christophe.pradal@inria.fr>
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
__revision__ = "$Id : "

DEBUG = False

import types
import sys

from openalea.oalab.model.visualea import VisualeaModel, VisualeaFile
from openalea.visualea.graph_operator import GraphOperator
from openalea.visualea import dataflowview
from openalea.core.compositenode import CompositeNodeFactory
from openalea.oalab.service.help import display_help
from openalea.oalab.service.plot import get_plotters
from openalea.core.service.model import to_model

from openalea.oalab.gui.paradigm.controller import ParadigmController


def actions(self):
    """
    :return: list of actions to set in the menu.
    """
    return self._actions


def mainMenu(self):
    """
    :return: Name of menu tab to automatically set current when current widget
    begin current.
    """
    return "Project"


def _display_help(self):
    """
    Method to display help
    """
    doc = self.applet.model.get_documentation()
    if not doc:
        doc = """
<H1>Visualea</H1>

More informations: http://openalea.gforge.inria.fr/doc/openalea/visualea/doc/_build/html/contents.html
"""
    display_help(doc)


VIEWER3D_SET = False


def _set_viewer3d():
    viewernode = sys.modules.get('openalea.plantgl.wralea.visualization.viewernode')
    plotters = get_plotters()
    if plotters and viewernode:
        viewer = plotters[0]
        viewernode.registerPlotter(viewer)


class VisualeaModelController(ParadigmController):
    default_name = VisualeaModel.default_name
    default_file_name = VisualeaModel.default_file_name
    pattern = VisualeaModel.pattern
    extension = VisualeaModel.extension
    icon = VisualeaModel.icon
    mimetype_model = VisualeaModel.mimetype
    mimetype_data = VisualeaFile.mimetype

    def instantiate_widget(self):
        self._widget = dataflowview.GraphicalGraph.create_view(self.model._workflow, clone=True)
        self._clipboard = CompositeNodeFactory("Clipboard")

        from openalea.core.service.ipython import interpreter
        interp = interpreter()

        GraphOperator.globalInterpreter = interp
        self._operator = GraphOperator(graph=self.model._workflow,
                                       graphScene=self._widget.scene(),
                                       clipboard=self._clipboard,
                                       )
        self._widget.mainMenu = types.MethodType(mainMenu, self._widget)
        self._widget.applet = self
        self._widget._actions = None

        methods = {}
        methods['actions'] = actions
        methods['mainMenu'] = mainMenu
        methods['display_help'] = _display_help

        self._widget = adapt_widget(self._widget, methods)

        if not VIEWER3D_SET:
            _set_viewer3d()

        # todo: use services
        self.widget().scene().focusedItemChanged.connect(self.item_focus_change)

        return self.widget()

    def item_focus_change(self, scene, item):
        """
        Set doc string in Help widget when focus on node changed
        """
        assert isinstance(item, dataflowview.vertex.GraphicalVertex)
        txt = item.vertex().get_tip()
        # todo: use services
        display_help(txt)

    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget

    def widget_value(self):
        return self.model.repr_code()

    def execute(self):
        return self.model.execute()

    def namespace(self, **kwargs):
        from openalea.core.service.ipython import interpreter
        project_ns = ParadigmController.namespace(self, **kwargs)
        interp = interpreter()
        shell_ns = interp.user_ns
        ns = {}
        ns.update(shell_ns)
        ns.update(project_ns)
        return ns

    def init(self, *args, **kwargs):
        # todo : register plotter
        if not VIEWER3D_SET:
            _set_viewer3d()

        return ParadigmController.init(self, *args, **kwargs)


def adapt_widget(widget, methods):
    method_list = ['actions',  'mainMenu', 'display_help']

    def check():
        for m in method_list:
            if m not in methods:
                raise NotImplementedError(m)
    check()
    for m in method_list:
        widget.__setattr__(m, types.MethodType(methods[m], widget))
    return widget
