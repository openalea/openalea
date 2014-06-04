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
           "qt_editors",
           "edit", "edit_qt", "edit_notebook", "edit_bash",
           "register_control", "get_control"
           ]

def _discover_editors(plugins):
    _editors = {}
    for editor in plugins:
        for control in editor.controls:
            if control in _editors :
                _editors[control].append(editor)
            else:
                _editors[control] = [editor]
    return _editors


def discover_qt_controls():
    # Must move to entry_points oalab.qt_control
    from openalea.oalab.plugins.controls import (
        PluginIntSlider, PluginIntSpinBox, PluginColorListWidget, PluginCurve2DWidget)
    plugins = [
       PluginIntSlider,
       PluginIntSpinBox,
       PluginColorListWidget,
       PluginCurve2DWidget,
    ]
    return _discover_editors(plugins)

def discover_bash_controls():
    # Must move to entry_points oalab.bash_control
    plugins = []
    return _discover_editors(plugins)

def discover_notebook_controls():
    # Must move to entry_points oalab.notebook_control
    plugins = []
    return _discover_editors(plugins)

def _edit(control, discover):
    """
    Hard coded example. Must be replaced by a function handling plugins and
    lack of plugins
    """
    editors = discover()
    cname = control.interface.__class__.__name__
    widget_class = None
    if control.widget:
        # Load widget specified with control
        for editor in editors[cname]:
            if control.widget == editor.name:
                widget_class = editor.load()
                break
    else:
        # Load first editor
        for editor in editors[cname]:
            widget_class = editor.load()
            break

    if widget_class:
        widget = widget_class.edit(control)
        widget.set(control)
        widget.show()
        return widget
    else :
        raise ValueError, 'No editors for %s' % control


def edit_qt(control, shape=None):
    editors = discover_qt_controls()
    cname = control.interface.__class__.__name__
    widget_class = None
    if control.widget:
        # Load widget specified with control
        for editor in editors[cname]:
            if control.widget == editor.name:
                widget_class = editor.load()
                break
    else:
        # Load first editor
        for editor in editors[cname]:
            widget_class = editor.load()
            break

    if widget_class:
        widget = widget_class.edit(control, shape)
        if widget is not None:
            widget.set(control)
            widget.show()
        return widget
    else :
        raise ValueError, 'No editors for %s' % control

def qt_paint_function(control):
    editors = discover_qt_controls()
    cname = control.interface.__class__.__name__
    widget_class = None
    if control.widget:
        # Load widget specified with control
        for editor in editors[cname]:
            if control.widget == editor.name and editor.paint :
                widget_class = editor.load()
                return widget_class.paint

    # Load first editor
    for editor in editors[cname]:
        if editor.paint:
            widget_class = editor.load()
            return widget_class.paint

def edit_notebook(control):
    return _edit(control, discover_notebook_controls)

def edit_bash(control):
    return _edit(control, discover_bash_controls)

def edit(control):
    import sys
    if 'PyQt4.QtGui' in sys.modules or 'PySide.QtGui' in sys.modules:
        from openalea.vpltk.qt import QtGui
        if QtGui.QApplication.instance():
            return edit_qt(control)
    return edit_notebook(control)

def qt_editors(iname):
    controls = discover_qt_controls()
    return controls[iname]

def register_control(name, value):
    from openalea.oalab.control.manager import ControlManager
    return ControlManager().new_control(name, value)

def get_control(name):
    from openalea.oalab.control.manager import ControlManager
    return ControlManager().control(name)
