
from openalea.core.service.interface import interface_class, interface_name
from openalea.core.plugin import iter_plugins
from openalea.core.control.control import Control

from openalea.core.observer import AbstractListener

from openalea.oalab.control.widget import AbstractControlWidget


class NotebookControlWidget(AbstractControlWidget):

    def __init__(self, notebookclass=None, **kwargs):
        AbstractControlWidget.__init__(self)
        self._w = notebookclass(**kwargs)

    def apply(self, control):
        control.value = self._w.value

    def autoapply(self, control, auto=True):
        if auto is True:
            self._control_out = control
            self._w.on_trait_change(self.on_widget_value_changed, 'value')

    def reset(self, value=None, *kargs):
        """
        Reset widget to default values.
        """
        if value is None:
            value = self.traits()['value'].default_value
        self._w.value = value

    def on_value_changed(self, *args, **kwargs):
        """
        Method called when value changed.
        This method generally read control and refresh view if :term:`auto-read mode` is enabled.
        """
        self._w.value = self._control_in.value

    def on_widget_value_changed(self, name, value):
        self._control_out.value = self._w.value

    def setValue(self, value):
        """
        Change widget value.
        If your class derivates from an third-party widget, it is sometime necessary
        to adapt control value type to widget supported type.
        Example unicode to QString in pyqt API v1.
        """
        self._w.value = value

    def value(self, interface=None):
        """
        Returns widget value.
        If your class derivates from an third-party widget, it is sometime necessary
        to adapt widget value type to control type.
        If widget supports more than one interface, returned value depends on given interface.
        If none, returns widget preferred type.
        """
        return self._w.value

    def _ipython_display_(self):
        return self._w._ipython_display_()

from IPython.html import widgets
available_widgets = {
    'IInt': [widgets.IntSliderWidget],
    'IStr': [widgets.HTMLWidget],
    'IBool': [widgets.CheckboxWidget],
}

preferred_widgets = {
    'IInt': {
        'slider': widgets.IntSliderWidget,
        'progress': widgets.IntProgressWidget
    },

    'IStr': {
        'html': widgets.HTMLWidget,
        'latex': widgets.LatexWidget,
        'text': widgets.TextWidget,
        'text area': widgets.TextareaWidget
    },

    'IBool': {
        'checkbox': widgets.CheckboxWidget
    },

}


def notebook_editor(control, shape=None, preferred=None, preferences=None):
    iname = interface_name(control.interface)
    notebookclass = None
    if preferred:
        notebookclass = preferred
    elif preferences and iname in preferences:
        notebookclass = preferences[iname].value
    elif iname in preferred_widgets:
        notebookclass = preferred_widgets[iname].values()[0]

    if notebookclass:
        widget = NotebookControlWidget(notebookclass=notebookclass)
        widget.set(control)
        return widget


def select_default_widgets():
    from IPython.display import display
    box = widgets.ContainerWidget(description="Select default widgets")
    dic = {}
    children = []
    for iname, widget_dict in preferred_widgets.iteritems():
        iclass = interface_class(iname)
#         for name, notebookclass in widgets.iteritems():
        values = widget_dict
        widget = widgets.SelectWidget(description=iclass.__alias__, values=values)
        children.append(widget)
        dic[iname] = widget
    box.children = children
    box.set_css('border', "1px solid")
    display(box)
    return dic
