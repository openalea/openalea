
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
        PluginIntSlider, PluginIntSpinBox, PluginColorListWidget)
    plugins = [
       PluginIntSlider,
       PluginIntSpinBox,
       PluginColorListWidget,
    ]
    return _discover_editors(plugins)

def discover_bash_controls():
    # Must move to entry_points oalab.bash_control
    from openalea.oalab.plugins.controls import PluginIntIPython
    plugins = [
       PluginIntIPython,
    ]
    return _discover_editors(plugins)

def discover_notebook_controls():
    # Must move to entry_points oalab.notebook_control
    from openalea.oalab.plugins.controls import *
    plugins = [
        PluginIntNotebook,
                        ]
    return _discover_editors(plugins)



def _edit(control, discover):
    """
    Hard coded example. Must be replaced by a function handling plugins and
    lack of plugins
    """
    editors = discover()
    cname = control.interface.__class__.__name__
    widget = None
    if control.widget:
        # Load widget specified with control
        for editor in editors[cname]:
            if control.widget == editor.name:
                widget = editor.load()()
                break
    else:
        # Load first editor
        for editor in editors[cname]:
            widget = editor.load()()
            break

    if widget:
        widget.edit(control)
        return widget
    else :
        raise ValueError, 'No editors for %s' % control


def edit_qt(control):
    return _edit(control, discover_qt_controls)

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
