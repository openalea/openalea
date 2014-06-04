import copy

from openalea.core.observer import Observed, AbstractListener
from openalea.core.singleton import Singleton
from openalea.oalab.control.control import Control

class ControlManager(Observed, AbstractListener):

    __metaclass__ = Singleton

    def __init__(self):
        Observed.__init__(self)
        AbstractListener.__init__(self)
        self._controls = {}
        self._tagged_controls = {}

    def control(self, uid, tag=None):
        return self.controls(tag)[uid]

    def add_control(self, control, tag=None):
        """
        :param control: Control object or tuple(name, interface, widget). widget can be None
        :param tag: If tag is specified, link control to this tag, else control is global to all tags in current project.
        """
        assert isinstance(control, Control)

        self.initialise(control)
        if tag is None:
            self._controls[control.name] = control
            self.notify_listeners(('global_control_changed', control))
        else:
            if tag not in self._tagged_controls:
                self._tagged_controls[tag] = {}
            self._tagged_controls[tag][control.name] = control
            self.notify_listeners(('tag_control_changed', (control, tag)))

        self.notify_listeners(('state_changed', (control, tag)))

    def namespace(self, tag=None):
        """
        Returns namespace (dict control name -> value).
        :param tag: returns namespace corresponding to given tag. Default, returns global namespace
        """
        ns = {}
        for name, control in self.controls(tag).iteritems():
            ns[name] = copy.deepcopy(control.value)
        return ns

    @property
    def global_controls(self):
        return self._controls

    @property
    def tagged_controls(self):
        return self._tagged_controls

    def controls(self, tag=None):
        if tag is None:
            return self._controls
        elif tag is False:
            return {}
        else:
            return self._tagged_controls[tag]

    def notify(self, sender, event):
        if isinstance(sender, Control):
            signal, data = event
            if signal == 'value_changed':
                self.notify_listeners(('control_value_changed', (sender, data)))

def control_dict():
    """
    Get the controls from the control manager in a dictionary (key = name, value = object)

    :return: dict of controls
    """
    cm = ControlManager()
    controls = cm.namespace()
    print controls
    return controls
