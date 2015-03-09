# -*- python -*-
# -*- coding: utf8 -*-
#
#       OpenAlea.OALab
#
#       Copyright 2014 INRIA - CIRAD - INRA
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

import copy

from openalea.core.observer import Observed, AbstractListener, lock_notify
from openalea.core.singleton import Singleton
from .control import Control


class Follower(AbstractListener):

    def __init__(self, name, func):
        AbstractListener.__init__(self)
        self._old_value = None
        self.name = name
        self.callback = func
        self._listen = True

    def ignore_events(self):
        self._listen = False

    def follow_events(self):
        self._listen = True

    @lock_notify
    def notify(self, sender, event):
        if self._listen is False:
            return

        if event:
            signal, data = event
            if signal == 'control_value_changed':
                control, value = data
                if control.name == self.name and value != self._old_value:
                    old_value = self._old_value
                    self._old_value = value
                    self.callback(old_value, value)


class ControlContainer(Observed, AbstractListener):

    def __init__(self):
        Observed.__init__(self)
        AbstractListener.__init__(self)
        self.follower = {}
        self._controls = []

    def control(self, name=None, uid=None):
        """
        Return all control with name "name".
        If no control found, returns None, if only one found, returns it else return a list
        of control.

        If uid is passed, returns corresponding control or None if not found. 
        If uid is passed, it never returns a list as uid is unique.
        """
        if name is None and uid is None:
            return [control for control in self._controls]
        elif name is None and uid:
            for control in self._controls:
                if str(id(control)) == str(uid):
                    return control
        elif name and uid is None:
            controls = []
            for control in self._controls:
                if control.name == name:
                    controls.append(control)
            if len(controls) == 0:
                return None
            elif len(controls) == 1:
                return controls[0]
            else:
                return controls
        else:
            return self.control(None, uid)

    def add(self, name, **kwds):
        """
        Convenience method to create a control and add it to container.
        See :class:`~openealea.core.control.control.Control`.

        >>> container = ControlContainer()
        >>> container.add('i', interface='IInt', value=1)

        :param name: Control name
        :param kwds: Control keywords like interface, value, ...
        """
        control = Control(name, **kwds)
        self.add_control(control)
        return control

    def update(self, dic):
        """
        Update controls with dict values.
        If a name is not referenced in ControlContainer, nothing is done.

        .. note::
            Example:

            Let "container" a Container with one control "a" with value 1::

                container:
                    - a:IInt = 1

            after container.update({'a':2, 'b':3}) we get

                container:
                    - a:IInt = 2

        :param dic: :obj:`dict` name -> value
        """
        for name, value in dic.items():
            control = self.control(name=name)
            if control is None:
                continue
            control.value = value

    def add_control(self, control):
        """
        :param control: Control object
        """
        assert isinstance(control, Control)
        if control not in self._controls:
            self._controls.append(control)
        control.register_listener(self)
        self.notify_listeners(('state_changed', (control)))

    def remove_control(self, control):
        """
        :param control: Control object
        """
        assert isinstance(control, Control)
        if control in self._controls:
            self._controls.remove(control)
            control.unregister_listener(self)
            self.notify_listeners(('state_changed', (control)))

    def clear(self):
        # make a copy of the list, required by for loop
        for control in list(self._controls):
            self.remove_control(control)

    def namespace(self, interface=None):
        """
        Returns namespace (dict control name -> value).
        :param tag: returns namespace corresponding to given tag.
                    Default, returns global namespace
        """
        ns = {}
        for control in self.controls():
            if interface is None:
                ns[control.name] = copy.deepcopy(control.value)
            else:
                from openalea.core.service.interface import interface_name
                if interface_name(control.interface) == interface:
                    ns[control.name] = copy.deepcopy(control.value)
        return ns

    def changed(self):
        """
        Like :meth:`~openealea.core.control.manager.ControlContainer.namespace` but
        dictionnary contains only controls with value different than default value.
        """
        dic = {}
        for control in self._controls:
            if control.value != control.default:
                dic[control.name] = control.value
        return dic

    def controls(self):
        """
        Returns a list of :class:`~openealea.core.control.control.Control` objects.
        """
        return list(self._controls)

    def notify(self, sender, event):
        if isinstance(sender, Control):
            signal, data = event
            if signal == 'value_changed':
                self.notify_listeners(
                    ('control_value_changed', (sender, data)))
            if signal == 'name_changed':
                self.notify_listeners(('control_name_changed', (sender, data)))

    def __contains__(self, key):
        for control in self.controls():
            if key == control.name:
                return True
        return False

    def disable_followers(self):
        for follower in self.follower.values():
            follower.ignore_events()

    def enable_followers(self):
        for follower in self.follower.values():
            follower.follow_events()

    def register_follower(self, name, func):
        if name in self.follower:
            self.unregister_follower(name)
        follower = Follower(name, func)
        self.register_listener(follower)
        self.follower[name] = follower

    @classmethod
    def unregister_follower(self, name):
        if name in self.follower:
            self.unregister_listener(self.follower[name])
            del self.follower[name]


class ControlManager(ControlContainer):
    __metaclass__ = Singleton


def control_dict():
    """
    Get the controls from the control manager in a dictionary
    (key = name, value = object)

    :return: dict of controls
    """
    cm = ControlManager()
    controls = cm.namespace()
    return controls
