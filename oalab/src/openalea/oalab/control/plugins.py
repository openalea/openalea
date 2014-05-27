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
    tags = [
      'treeview-ready', # Can be embeded in a treeview (defines a paint method and is enough small)
      'thumbnail-ready' # Can generate a thumbnail
      'wide-widget' # Wide widget, generally
      ]

    @classmethod
    def load(cls):
        raise NotImplementedError

class PluginIntSpinBox(ControlWidgetPlugin):

    controls = ['IInt']
    name = 'IntSpinBox'
    required = ['IInt.min', 'IInt.max']


    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import IntSpinBox
        return IntSpinBox

class PluginIntSlider(ControlWidgetPlugin):

    controls = ['IInt']
    name = 'IntSlider'
    required = ['IInt.min', 'IInt.max']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import IntSlider
        return IntSlider

class PluginIntIPython(ControlWidgetPlugin):

    controls = ['IInt']
    name = 'IntIPython'
    required = ['IInt.min', 'IInt.max']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import IntIPython
        return IntIPython


class PluginIntNotebook(ControlWidgetPlugin):

    controls = ['IInt']
    name = 'IntNotebook'
    required = ['IInt.min', 'IInt.max']


    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import IntNotebook
        return IntNotebook


class PluginColorListWidget(ControlWidgetPlugin):
    controls = ['IColorList']
    name = 'ColorListWidget'

    @classmethod
    def load(cls):
        from openalea.oalab.gui.stdcontrolwidget import ColorListWidget
        return ColorListWidget

