
from openalea.core.observer import Observed
from openalea.oalab.service.interface import get_interface

import copy
import inspect

class Control(Observed):
    def __init__(self, name, interface, value=None, widget=None, constraints=None):
        Observed.__init__(self)
        if isinstance(interface, basestring):
            interface = get_interface(interface)
        if constraints is None:
            constraints = {}
        if inspect.isclass(interface):
            interface = interface(**constraints)
        self._interface = interface
        self.name = name
        self.widget = widget
        self.default()
        if value:
            self._value = value

    def __repr__(self):
        return 'Control(%r, name=%r)' % (self._interface, self.name)

    def notify_change(self):
        self.notify_listeners(('ValueChanged', self._value))

    def rename(self, name):
        self.name = name

    def default(self):
        self._value = self._interface.default()

    def value(self):
        return self._value

    def set_value(self, value):
        """
        A deep copy of value must be saved in _value.
        Original one is stored in _user_value.
        """
        self._value = copy.deepcopy(value)
        self._user_value = value
        self.notify_change()

    def check(self, value):
        pass

    interface = property(fget=lambda self:self._interface)
