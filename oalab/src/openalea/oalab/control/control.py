
from openalea.core.observer import Observed

SYNCHRO_AUTO = 1 # Control is always synchronized with editor
SYNCHRO_NEVER = 2 # Control is never synchronize. Developper must do it manually
SYNCHRO_ON_CLOSE = 3 # Control is synchronized when editor is deleted or closed
SYNCHRO_ON_APPLY = 3 # Control is synchronized when user clicks on OK or Apply

class Control(Observed):
    def __init__(self):
        Observed.__init__(self)
        self.name = "default"
        self.default()

    def notify_change(self):
        self.notify_listeners(('ValueChanged', self._value))

    def rename(self, name):
        self.name = name

    def default(self):
        raise NotImplementedError

    def value(self):
        return self._value

    def set_value(self, value):
        """
        A deep copy of value must be saved in _value.
        Original one is stored in _user_value.
        """
        raise NotImplementedError
