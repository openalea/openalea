
from openalea.core.observer import Observed

import copy
import inspect

def deepcopy(value):
    # Will become a service
    return copy.deepcopy(value)

class Control(Observed):
    def __init__(self, interface, name='default'):
        Observed.__init__(self)
        if inspect.isclass(interface):
            interface = interface()
        self._interface = interface
        self.name = name
        self.default()

    def __str__(self):
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
        self._value = deepcopy(value)
        self.notify_change()

    def check(self, value):
        pass

    interface = property(fget=lambda self:self._interface)
