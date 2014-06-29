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
           "new", "get", "get_control",
           "register", "unregister",
           "clear_ctrl_manager",
           "save_controls", "load_controls"
           ]


from openalea.vpltk.plugin import iter_plugins

from openalea.oalab.control.control import Control
from openalea.oalab.control.manager import ControlManager

def discover_bash_controls():
    # Must move to entry_points oalab.bash_control
    plugins = []
    return plugins

def discover_notebook_controls():
    # Must move to entry_points oalab.notebook_control
    plugins = []
    return plugins

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

