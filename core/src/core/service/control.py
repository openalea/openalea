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
           "create_control",
           "get_control",
           "group_controls",
           "new_control",
           "register_control",
           "unregister_control",
           ]


from openalea.core.plugin import iter_plugins
from openalea.core.control.control import Control
from openalea.core.control.manager import ControlManager, ControlContainer

def create_control(name, iname=None, value=None, constraints=None):
    """
    Create a new Control object.
    This object is local and standalone.
    To track it, use register service.
    """
    if iname is None and value is None:
        raise ValueError, 'You must define a least a value or an interface'
    control = Control(name, iname, value, constraints=constraints)
    return control

def register_control(control):
    """
    Ask application to track control.
    """
    cm = ControlManager()
    cm.add_control(control)

def unregister_control(control):
    """
    Ask application to stop tracking control.
    """
    cm = ControlManager()
    cm.remove_control(control)

def new_control(name, iname=None, value=None, constraints=None):
    """
    Create a new tracked control.
    """
    control = create_control(name, iname, value, constraints)
    register_control(control)
    return control

def get_control(name):
    """
    Get a tracked control by name.
    If multiple control with same name exists, returns a list of controls.
    """
    cm = ControlManager()
    return cm.control(name)

def group_controls(control_list):
    container = ControlContainer()
    for control in control_list:
        container.add_control(control)
    return container
