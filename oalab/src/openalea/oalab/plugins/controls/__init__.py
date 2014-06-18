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

from openalea.oalab.plugins.control import ControlWidgetSelectorPlugin
from openalea.deploy.shared_data import shared_data
import openalea.oalab
"""
class PluginIntSpinBox(ControlWidgetSelectorPlugin):

    controls = ['IInt']
    name = 'IntSpinBox'
    required = ['IInt.min', 'IInt.max']
    edit_shape = ['line', 'small']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.control.widgets import IntSpinBox
        return IntSpinBox

class PluginIntSlider(ControlWidgetSelectorPlugin):

    controls = ['IInt']
    name = 'IntSlider'
    required = ['IInt.min', 'IInt.max']
    edit_shape = ['line', 'small']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.control.widgets import IntSlider
        return IntSlider
"""

class PluginIntWidgetSelector(ControlWidgetSelectorPlugin):

    controls = ['IInt']
    name = 'IntWidgetSelector'
    required = ['IInt.min', 'IInt.max']
    edit_shape = ['responsive']
    icon_path = shared_data(openalea.oalab, 'icons/IntWidgetSelector_hline.png')

    @classmethod
    def load(cls):
        from openalea.oalab.plugins.controls.selectors import IntWidgetSelector
        return IntWidgetSelector


class PluginBoolWidgetSelector(ControlWidgetSelectorPlugin):

    controls = ['IBool']
    name = 'BoolWidgetSelector'
    edit_shape = ['responsive']
    icon_path = shared_data(openalea.oalab, 'icons/BoolCheckBox.png')

    @classmethod
    def load(cls):
        from openalea.oalab.plugins.controls.widgets import BoolCheckBox
        return BoolCheckBox

class PluginFloatWidgetSelector(ControlWidgetSelectorPlugin):

    controls = ['IFloat']
    name = 'FloatWidgetSelector'
    edit_shape = ['large', 'hline']

    @classmethod
    def load(cls):
        from openalea.oalab.plugins.controls.visualea_widgets import FloatWidget
        return FloatWidget

class PluginDateTimeWidgetSelector(ControlWidgetSelectorPlugin):

    controls = ['IDateTime']
    name = 'DateTimeSelector'
    edit_shape = ['large', 'hline']

    @classmethod
    def load(cls):
        from openalea.oalab.plugins.controls.visualea_widgets import DateTimeWidget
        return DateTimeWidget

PluginOpenAleaLabWidgetSelectors = [
    PluginBoolWidgetSelector,
    PluginIntWidgetSelector
]

PluginVisualeaWidgetSelectors = [
    PluginFloatWidgetSelector,
    PluginDateTimeWidgetSelector
    ]
