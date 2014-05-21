
__all__ = ["edit_qt", "edit_notebook", "edit_bash", "control"]


from openalea.oalab.control.control import SYNCHRO_AUTO

def discover_controls():
    # Must move to entry_points oalab.control
    from openalea.oalab.control.plugins import *
    controls = [
        PluginIIntControl,
        PluginColorListControl,
        ]

    _controls = {}

    for control in controls:
        _controls[control.interface] = control

    return _controls

def _discover_editors(control, plugins):
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
    from openalea.oalab.control.plugins import *
    plugins = [
       PluginIntSlider,
       PluginIntSpinBox,
       PluginColorListWidget,
    ]
    return _discover_editors(control, plugins)

def discover_bash_controls():
    # Must move to entry_points oalab.bash_control
    from openalea.oalab.control.plugins import *
    plugins = [
       PluginIntIPython,
    ]
    return _discover_editors(control, plugins)

def discover_notebook_controls():
    # Must move to entry_points oalab.notebook_control
    from openalea.oalab.control.plugins import *
    plugins = [
        PluginIntNotebook,
                        ]
    return _discover_editors(control, plugins)



def _edit(control, synchro_mode, discover):
    """
    Hard coded example. Must be replaced by a function handling plugins and
    lack of plugins
    """
    editors = discover()

    classes = []
    cname = control.__class__.__name__
    for editor in editors[cname]:
        classes.append(editor.load())

    widget = classes[0]()
    widget.edit(control)
    return widget


def edit_qt(control, synchro_mode=SYNCHRO_AUTO):
    return _edit(control, synchro_mode, discover_qt_controls)

def edit_notebook(control, synchro_mode=SYNCHRO_AUTO):
    return _edit(control, synchro_mode, discover_notebook_controls)

def edit_bash(control, synchro_mode=SYNCHRO_AUTO):
    return _edit(control, synchro_mode, discover_bash_controls)

def edit(control, synchro_mode=SYNCHRO_AUTO):
    import sys
    if 'PyQt4.QtGui' in sys.modules or 'PySide.QtGui' in sys.modules:
        from openalea.vpltk.qt import QtGui
        if QtGui.QApplication.instance():
            return edit_qt(control, synchro_mode)
    return edit_notebook(control, synchro_mode)

def control(variable):
    """
    Hard coded example. Must be replaced by a function handling plugins and
    lack of plugins
    """
    interfaces = {
        int:'IInt',
        float:'IFloat'
    }
    controls = discover_controls()
    if type(variable) in interfaces:
        interface = interfaces[type(variable)]
        control_plugin = controls[interface]
        control = control_plugin.load()()
        control.set_value(variable)
        return control
    else:
        raise ValueError, 'No controls for %s' % type(variable)
