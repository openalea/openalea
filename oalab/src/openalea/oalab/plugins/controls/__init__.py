# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
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

class ControlWidgetPlugin():
    controls = []
    name = 'ControlWidget'

    edit_shape = [] # ['large', 'line', 'thumbnail']
    view_shape = [] # ['large', 'line', 'thumbnail']
    create_shape = [] # ['large', 'line', 'thumbnail']
    paint = False

    @classmethod
    def load(cls):
        raise NotImplementedError

class PluginIntSpinBox(ControlWidgetPlugin):

    controls = ['IInt']
    name = 'IntSpinBox'
    required = ['IInt.min', 'IInt.max']
    edit_shape = ['line', 'thumbnail']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.control.widgets import IntSpinBox
        return IntSpinBox

class PluginIntSlider(ControlWidgetPlugin):

    controls = ['IInt']
    name = 'IntSlider'
    required = ['IInt.min', 'IInt.max']
    edit_shape = ['line', 'thumbnail']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.control.widgets import IntSlider
        return IntSlider

class PluginColorListWidget(ControlWidgetPlugin):
    controls = ['IColorList']
    name = 'ColorListWidget'
    paint = True

    @classmethod
    def load(cls):
        from openalea.oalab.gui.control.widgets import ColorListWidget
        return ColorListWidget


class PluginCurve2DWidget(ControlWidgetPlugin):
    controls = ['ICurve2D']
    name = 'Curve2DWidget'
    paint = True

    @classmethod
    def load(cls):
        from openalea.oalab.gui.control.widgets import Curve2DWidget
        return Curve2DWidget
