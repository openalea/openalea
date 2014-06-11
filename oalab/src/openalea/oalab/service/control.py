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

__all__ = [
           "qt_widget_plugins",
           "edit", "qt_editor", "qt_painter",
           "new", "get", "get_control",
           "clear_ctrl_manager", "register_control", 
           "save_controls", "load_controls"
           ]

from openalea.vpltk.qt import QtGui

from openalea.oalab.control.control import Control
from openalea.oalab.control.manager import ControlManager

def discover_qt_controls():
    # Must move to entry_points oalab.qt_control
    from openalea.oalab.plugins.controls import (
#         PluginIntSlider,
#         PluginIntSpinBox,
        PluginBoolWidgetSelector,
        PluginIntWidgetSelector,
        PluginColorListWidget,
        PluginCurve2DWidget
        )
    plugins = [
#        PluginIntSlider,
#        PluginIntSpinBox,
       PluginColorListWidget,
       PluginCurve2DWidget,
       PluginIntWidgetSelector,
       PluginBoolWidgetSelector,
    ]
    return plugins

def discover_bash_controls():
    # Must move to entry_points oalab.bash_control
    plugins = []
    return plugins

def discover_notebook_controls():
    # Must move to entry_points oalab.notebook_control
    plugins = []
    return plugins

def qt_editor(control, shape=None, preferred=None):
    cname = control.interface.__class__.__name__
    widget_plugins = qt_widget_plugins(cname)
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


def create(name, iname=None, value=None, constraints=None):
    """
    Create a new Control object.
    This object is local and standalone.
    To track it, use register service.
    """
    if iname is None and value is None:
        raise ValueError, 'You must define a least a value or an interface'
    control = Control(name, iname, value, constraints=constraints)
    return control

def register(control):
    """
    Ask application to track control.
    """
    cm = ControlManager()
    cm.add_control(control)

def unregister(control):
    """
    Ask application to stop tracking control.
    """
    cm = ControlManager()
    cm.remove_control(control)

def new(name, iname=None, value=None, constraints=None):
    """
    Create a new tracked control.
    """
    control = create(name, iname, value, constraints)
    register(control)
    return control

def get(name):
    """
    Get a tracked control by name.
    If multiple control with same name exists, returns a list of controls.
    """
    cm = ControlManager()
    return cm.control(name)


def get_control(name):
    return get(name)


def save_controls(controls, filepath):
    """
    Save controls on disk.

    :param controls: controls objects
    :param filepath: complete path of file which will contain controls
    :return: True if success.
    """
    # TODO
    # @GBY
    pass


def load_controls(filepath):
    """
    Get controls from disk.

    :param filename: complete path of file which contain controls
    :return: controls objects
    """
    # TODO
    # @GBY
    pass


def clear_ctrl_manager():
    """
    Empty the control manager
    """
    # TODO
    # @GBY

