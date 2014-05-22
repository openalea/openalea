
__all__ = ["edit_qt", "edit_notebook", "edit_bash", "control"]

class IColorList(object):
    """

    IIntControl is a Control with this specific method:
        - set_range(range), with range a couple of int.
    """
    interface = 'IColorList'

    def default(self):
        """
        Reinitialize control to default value
        """
        from openalea.plantgl.all import Material, Color3
        value = [
            Material("Color_0"),
            Material("Color_0", Color3(65, 45, 15)), # Brown
            Material("Color_2", Color3(30, 60, 10)), # Green
            Material("Color_3", Color3(60, 0, 0)), # Red
            Material("Color_4", Color3(60, 60, 15)), # Yellow
            Material("Color_5", Color3(0, 0, 60)), # Blue
            Material("Color_6", Color3(60, 0, 60)), # Purple
            ]
        return value


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



def _edit(control, discover):
    """
    Hard coded example. Must be replaced by a function handling plugins and
    lack of plugins
    """
    editors = discover()

    classes = []
    cname = control.interface.__class__.__name__
    for editor in editors[cname]:
            classes.append(editor.load())

    widget = classes[0]()
    widget.edit(control)
    return widget


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

def control(variable):
    """
    Hard coded example. Must be replaced by a function handling plugins and
    lack of plugins
    """
    from openalea.oalab.control.control import Control
    from openalea.core.interface import IInt

    type_to_iname = {
        int:'IInt',
        float:'IFloat'
    }

    iname_to_interface = {
        'IInt':IInt,
        'IColorList':IColorList
                          }

    if type(variable) in type_to_iname:
        iname = type_to_iname[type(variable)]
        control = Control(iname_to_interface[iname])
        control.set_value(variable)
        return control
    else:
        raise ValueError, 'No controls for %s' % type(variable)
