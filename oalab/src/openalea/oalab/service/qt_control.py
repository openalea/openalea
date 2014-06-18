from openalea.vpltk.qt import QtGui
from openalea.oalab.service import interface as s_interface
from openalea.vpltk.plugin import iter_plugins

from openalea.oalab.session.session import Session
session = Session()

def discover_qt_controls():
    return [plugin for plugin in iter_plugins('oalab.qt_control', debug=session.debug_plugins)]

def qt_editor(control, shape=None, preferred=None):
    iname = s_interface.get_name(control.interface)
    widget_plugins = qt_widget_plugins(iname)
    widget_class = None

    if preferred:
        # Load widget specified with control
        for plugin in widget_plugins:
            if preferred == plugin.name:
                widget_class = plugin.load()
                break
    else:
        # Load first editor
        for plugin in widget_plugins:
            if 'responsive' in plugin.edit_shape or shape in plugin.edit_shape:
                widget_class = plugin.load()
                break

    if widget_class:
        widget = None
        if issubclass(widget_class, QtGui.QWidget):
            widget = widget_class()
        else:
            widget = widget_class.edit(control, shape)
        if widget is not None:
            widget.set(control)
            widget.show()
        return widget

def qt_viewer(control, shape=None):
    pass

def qt_painter(control, shape=None, preferred=None):
    cname = control.interface.__class__.__name__
    widget_plugins = qt_widget_plugins(cname)
    widget_class = None
    if preferred:
        # Load widget specified with control
        for plugin in widget_plugins:
            if preferred == plugin.name and plugin.paint :
                widget_class = plugin.load()
                return widget_class.paint(control, shape)

    # Load first editor
    for plugin in widget_plugins:
        if plugin.paint:
            widget_class = plugin.load()
            return widget_class.paint(control, shape)

def edit(control):
    import sys
    if 'PyQt4.QtGui' in sys.modules or 'PySide.QtGui' in sys.modules:
        from openalea.vpltk.qt import QtGui
        if QtGui.QApplication.instance():
            return qt_editor(control)
    else:
        raise NotImplementedError, 'Only Qt editors are supported'


def qt_widget_plugins(iname=None):
    """
    if iname is None, returns {'iname':[widget_plugin1, widget_plugin2, ...]}
    else: returns widget plugins for interface iname
    """
    if iname is None:
        plugins = discover_qt_controls()
        widget_plugins = {}
        for plugin in plugins :
            for iname in plugin.controls:
                widget_plugins.setdefault(iname, []).append(plugin)
        return widget_plugins
    else:
        widget_plugins = qt_widget_plugins()
        try:
            return widget_plugins[iname]
        except KeyError:
            return []

