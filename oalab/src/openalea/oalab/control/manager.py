import copy

from openalea.core.observer import Observed
from openalea.core.singleton import Singleton
from openalea.oalab.control.control import Control

class ControlManager(Observed):

    __metaclass__ = Singleton

    def __init__(self):
        Observed.__init__(self)
        self._global_controls = {}
        self._model_controls = {}

    def control(self, uid, model=None):
        return self.controls(model)[uid]

    def add_control(self, control, model=None):
        """
        :param control: Control object or tuple(name, interface, widget). widget can be None
        :param model: If model is specified, link control to this model, else control is global to all models in current project.
        """
        assert isinstance(control, Control)

        if model is None:
            self._global_controls[control.name] = control
            self.notify_listeners(('global_control_changed', control))
        else:
            if model not in self._model_controls:
                self._model_controls[model] = {}
            self._model_controls[model][control.name] = control
            self.notify_listeners(('model_control_changed', (control, model)))

        self.notify_listeners(('state_changed', (control, model)))

    def namespace(self, model=None):
        """
        Returns namespace (dict control name -> value).
        :param model: returns namespace corresponding to given model. Default, returns global namespace
        """
        ns = {}
        for name, control in self.controls(model).iteritems():
            ns[name] = copy.deepcopy(control.value)
        return ns

    @property
    def global_controls(self):
        return self._global_controls

    @property
    def model_controls(self):
        return self._model_controls

    def controls(self, model=None):
        if model is None:
            return self._global_controls
        elif model is False:
            return {}
        else:
            return self._model_controls[model]


def control_dict():
    """
    Get the controls from the control manager in a dictionary (key = name, value = object)

    :return: dict of controls
    """
    cm = ControlManager()
    controls = cm.namespace()
    return controls