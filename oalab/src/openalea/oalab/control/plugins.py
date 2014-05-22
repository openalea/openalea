"""
plugin.py

NO IMPORTS
return IntSpinBox is normally replaced by module path.
load uses Plugin.load to reach real class
"""

class ControlWidgetPlugin():
    controls = []
    name = 'ControlWidget'
    required = []
    supported = []

    @classmethod
    def load(cls):
        raise NotImplementedError

class PluginIntSpinBox(ControlWidgetPlugin):

    controls = ['IIntControl']
    name = 'IntSpinBox'
    required = ['MaximumRestriction', 'MinimumRestriction']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import IntSpinBox
        return IntSpinBox

class PluginIntSlider(ControlWidgetPlugin):

    controls = ['IIntControl']
    name = 'IntSlider'
    required = ['MaximumRestriction', 'MinimumRestriction']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import IntSlider
        return IntSlider

class PluginIntIPython(ControlWidgetPlugin):

    controls = ['IIntControl']
    name = 'IntIPython'
    supported = ['MaximumRestriction', 'MinimumRestriction']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import IntIPython
        return IntIPython


class PluginIntNotebook(ControlWidgetPlugin):

    controls = ['IIntControl']
    name = 'IntNotebook'
    required = ['MaximumRestriction', 'MinimumRestriction']


    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import IntNotebook
        return IntNotebook


class PluginColorListWidget(ControlWidgetPlugin):
    controls = ['ColorListControl']
    name = 'ColorListWidget'

    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import ColorListWidget
        return ColorListWidget


class PluginIIntControl(object):
    interface = "IInt"
    control = "IIntControl"
    @classmethod
    def load(cls):
        from openalea.oalab.control.stdcontrol import IIntControl
        return IIntControl


class PluginColorListControl(object):
    interface = "IColorList"
    control = "ColorListControl"
    @classmethod
    def load(cls):
        from openalea.oalab.control.stdcontrol import ColorListControl
        return ColorListControl
