import copy

from openalea.core.observer import Observed
from openalea.core.singleton import Singleton
from openalea.oalab.control.control import Control

class ControlManager(Observed):

    __metaclass__ = Singleton

    def __init__(self):
        Observed.__init__(self)
        self._controls = {}

    def control(self, uid):
        return self._controls[uid]

    def add_control(self, control):
        """
        :param control: Control object or tuple(name, interface, widget). widget can be None
        """
        assert isinstance(control, Control)

        self._controls[control.name] = control
        self.notify_listeners(('state_changed', None))

    def namespace(self):
        ns = {}
        for name, control in self._controls.iteritems():
            ns[name] = copy.deepcopy(control.value)
        return ns

    controls = property(fget=lambda self:self._controls)
