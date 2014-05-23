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

    def new_control(self, name, value):
        from openalea.oalab.service.interface import get_interface
        control = Control(name, get_interface(type(value)))
        control.set_value(value)
        self.add_control(control)
        return control

    def add_control(self, control):
        """
        :param control: Control object or tuple(name, interface, widget). widget can be None
        """
        if not isinstance(control, Control):
            control = Control(*control)

        self._controls[control.name] = control
        self.notify_listeners(('ControlManagerChanged', None))

    controls = property(fget=lambda self:self._controls)
