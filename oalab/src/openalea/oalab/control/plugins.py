"""
plugin.py

NO IMPORTS
return IntSpinBox is normally replaced by module path.
load uses Plugin.load to reach real class
"""

class PluginIntSpinBox(object):
    controls = ['IIntControl']
    name = 'IntSpinBox'

    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import IntSpinBox
        return IntSpinBox

class PluginIntSlider(object):
    controls = ['IIntControl']
    name = 'IntSlider'

    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import IntSlider
        return IntSlider

class PluginIntIPython(object):
    controls = ['IIntControl']
    name = 'IntIPython'

    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import IntIPython
        return IntIPython


class PluginIntNotebook(object):
    controls = ['IIntControl']
    name = 'IntNotebook'

    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import IntNotebook
        return IntNotebook


class PluginColorListWidget(object):
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
