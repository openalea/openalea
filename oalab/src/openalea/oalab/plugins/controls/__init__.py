
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
        from openalea.oalab.gui.control.widgets import IntSpinBox
        return IntSpinBox

class PluginIntSlider(ControlWidgetPlugin):

    controls = ['IInt']
    name = 'IntSlider'
    required = ['IInt.min', 'IInt.max']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.control.widgets import IntSlider
        return IntSlider

# class PluginIntSpinBox2(ControlWidgetPlugin):
#
#     controls = ['IInt']
#     name = 'IntSpinBox2'
#     required = ['IInt.min', 'IInt.max']
#
#     @classmethod
#     def load(cls):
#         from openalea.oalab.gui.control.widgets import IntSpinBox2
#         return IntSpinBox2

class PluginIntIPython(ControlWidgetPlugin):

    controls = ['IInt']
    name = 'IntIPython'
    required = ['IInt.min', 'IInt.max']

    @classmethod
    def load(cls):
        from openalea.oalab.gui.control.widgets import IntIPython
        return IntIPython


class PluginIntNotebook(ControlWidgetPlugin):

    controls = ['IInt']
    name = 'IntNotebook'
    required = ['IInt.min', 'IInt.max']


    @classmethod
    def load(cls):
        from openalea.oalab.gui.control.widgets import IntNotebook
        return IntNotebook


class PluginColorListWidget(ControlWidgetPlugin):
    controls = ['IColorList']
    name = 'ColorListWidget'

    @classmethod
    def load(cls):
        from openalea.oalab.gui.control.widgets import ColorListWidget
        return ColorListWidget

