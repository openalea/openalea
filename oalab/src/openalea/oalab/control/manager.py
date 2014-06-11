import copy

from openalea.core.observer import Observed, AbstractListener
from openalea.core.singleton import Singleton
from openalea.oalab.control.control import Control

class ControlContainer(Observed, AbstractListener):

    def __init__(self):
        Observed.__init__(self)
        AbstractListener.__init__(self)
        self._controls = {}

    def control(self, uid):
        try:
            return self.controls()[uid]
        except KeyError:
            return None

    def add_control(self, control):
        """
        :param control: Control object or tuple(name, interface, widget). widget can be None
        :param tag: If tag is specified, link control to this tag, else control is global to all tags in current project.
        """
        assert isinstance(control, Control)
        if control.name in self._controls:
            raise NameError, 'Control %s is yet registered' % control.name

        control.register_listener(self)
        self._controls[control.name] = control
        self.notify_listeners(('state_changed', (control)))

    def remove_control(self, control):
        """
        :param control: Control object or tuple(name, interface, widget). widget can be None
        :param tag: If tag is specified, link control to this tag, else control is global to all tags in current project.
        """
        assert isinstance(control, Control)
        if control.name in self._controls:
            control.unregister_listener(self)
            del self._controls[control.name]
            self.notify_listeners(('state_changed', (control)))

    def namespace(self):
        """
        Returns namespace (dict control name -> value).
        :param tag: returns namespace corresponding to given tag. Default, returns global namespace
        """
        ns = {}
        for name, control in self.controls().iteritems():
            ns[name] = copy.deepcopy(control.value)
        return ns

    def controls(self):
        return self._controls

    def notify(self, sender, event):
        if isinstance(sender, Control):
            signal, data = event
            if signal == 'value_changed':
                self.notify_listeners(('control_value_changed', (sender, data)))

class ControlManager(ControlContainer):
    __metaclass__ = Singleton

def control_dict():
    """
    Get the controls from the control manager in a dictionary (key = name, value = object)

    :return: dict of controls
    """
    cm = ControlManager()
    controls = cm.namespace()
    return controls
