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


################################################################################
# Manual definition of Qt control widgets from openalea node widgets
################################################################################

from openalea.oalab.plugin.oalab.control import ControlWidgetSelectorPlugin
from openalea.deploy.shared_data import shared_data
import openalea.oalab

from openalea.core.plugin import PluginDef

"""
class PluginIntSpinBox(ControlWidgetSelectorPlugin):

    controls = ['IInt']
    name = 'IntSpinBox'
    required = ['IInt.min', 'IInt.max']
    edit_shape = ['line', 'small']

    def __call__(self):
        from openalea.oalab.control.widgets import IntSpinBox
        return IntSpinBox

class PluginIntSlider(ControlWidgetSelectorPlugin):

    controls = ['IInt']
    name = 'IntSlider'
    required = ['IInt.min', 'IInt.max']
    edit_shape = ['line', 'small']

    def __call__(self):
        from openalea.oalab.control.widgets import IntSlider
        return IntSlider
"""


@PluginDef
class PluginIntWidgetSelector(ControlWidgetSelectorPlugin):

    controls = ['IInt']
    label = 'Integer editor'
    required = ['IInt.min', 'IInt.max']
    edit_shape = ['responsive']
    icon_path = shared_data(openalea.oalab, 'icons/IntWidgetSelector_hline.png')

    def __call__(self):
        from openalea.oalab.control.selector import IntWidgetSelector
        return IntWidgetSelector


@PluginDef
class PluginFloatWidgetSelector(ControlWidgetSelectorPlugin):

    controls = ['IFloat']
    label = 'Float editor'
    required = ['IFloat.min', 'IFloat.max', 'IFloat.step']
    edit_shape = ['responsive']
    icon_path = shared_data(openalea.oalab, 'icons/IntWidgetSelector_hline.png')

    def __call__(self):
        from openalea.oalab.control.selector import FloatWidgetSelector
        return FloatWidgetSelector


@PluginDef
class PluginIntRangeWidgetSelector(ControlWidgetSelectorPlugin):

    controls = ['IIntRange']
    label = 'Int Range editor'
    required = ['IIntRange.min', 'IIntRange.max']
    edit_shape = ['responsive']

    def __call__(self):
        from openalea.oalab.control.selector import IntRangeWidgetSelector
        return IntRangeWidgetSelector


@PluginDef
class PluginColormapWidgetSelector(ControlWidgetSelectorPlugin):

    controls = ['IColormap']
    label = 'Colormap editor'
    required = []
    edit_shape = ['responsive']
    paint = True

    def __call__(self):
        from openalea.oalab.control.selector import ColormapWidgetSelector
        return ColormapWidgetSelector


@PluginDef
class PluginBoolWidgetSelector(ControlWidgetSelectorPlugin):

    controls = ['IBool']
    edit_shape = ['responsive']

    def __call__(self):
        from openalea.oalab.widget.control import BoolCheckBox
        return BoolCheckBox


@PluginDef
class PluginStringWidgetSelector(ControlWidgetSelectorPlugin):

    controls = ['IStr']
    edit_shape = ['hline', 'large', 'small']

    def __call__(self):
        from openalea.oalab.widget.control import StrLineEdit
        return StrLineEdit
