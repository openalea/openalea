# Header
""" Control

"""
from openalea.core.observer import Observed
from openalea.oalab.service.interface import get_interface

import copy
import inspect

class Control(Observed):
    """ TODO

    """
    def __init__(self, name, interface, value=None, widget=None, constraints=None):
        """

        """
        Observed.__init__(self)

        self.name = name
        self.widget = widget

        self._interface = get_interface(interface, constraints)

        self._value = value 
        if value is None: 
            self._value = self.default_value(self._interface)  

    def __repr__(self):
        # TODO: CPL : Update the function
        return 'Control(name=%r, %r)' % (self._interface, self.name)

    def notify_change(self):
        self.notify_listeners(('ValueChanged', self._value))

    def rename(self, name):
        self.name = name

    @staticmethod
    def default_value(interface):
        return interface.default()

    def value(self):
        return self._value

    def set_value(self, value):
        """
        A deep copy of value must be saved in _value.
        Original one is stored in _user_value.
        """
        # TODO: CPL: To discuss !!!!
        #self._value = copy.deepcopy(value)
        #self._user_value = value
        self.notify_change()

    def check(self, value):
        pass

    @property
    def interface(self):
        return self._interface
 