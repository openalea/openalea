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

from openalea.oalab.plugins.control import ControlWidgetPlugin
from openalea.deploy.shared_data import shared_data
import openalea.oalab
"""
class PluginIntSpinBox(ControlWidgetPlugin):

    controls = ['IInt']
    name = 'IntSpinBox'
    required = ['IInt.min', 'IInt.max']
    edit_shape = ['line', 'small']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.control.widgets import IntSpinBox
        return IntSpinBox

class PluginIntSlider(ControlWidgetPlugin):

    controls = ['IInt']
    name = 'IntSlider'
    required = ['IInt.min', 'IInt.max']
    edit_shape = ['line', 'small']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.control.widgets import IntSlider
        return IntSlider
"""

class PluginIntWidgetSelector(ControlWidgetPlugin):

    controls = ['IInt']
    name = 'IntWidgetSelector'
    required = ['IInt.min', 'IInt.max']
    edit_shape = ['responsive']
    icon_path = shared_data(openalea.oalab, 'icons/IntWidgetSelector_hline.png')

    @classmethod
    def load(cls):
        from openalea.oalab.plugins.controls.selectors import IntWidgetSelector
        return IntWidgetSelector


class PluginBoolWidgetSelector(ControlWidgetPlugin):

    controls = ['IBool']
    name = 'BoolWidgetSelector'
    edit_shape = ['responsive']
    icon_path = shared_data(openalea.oalab, 'icons/BoolCheckBox.png')

    @classmethod
    def load(cls):
        from openalea.oalab.plugins.controls.widgets import BoolCheckBox
        return BoolCheckBox

