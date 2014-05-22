
from openalea.core.observer import Observed

SYNCHRO_AUTO = 1 # Control is always synchronized with editor
SYNCHRO_NEVER = 2 # Control is never synchronize. Developper must do it manually
SYNCHRO_ON_CLOSE = 3 # Control is synchronized when editor is deleted or closed
SYNCHRO_ON_APPLY = 3 # Control is synchronized when user clicks on OK or Apply

class Restriction(object):
    pass

class Control(Observed):
    def __init__(self):
        Observed.__init__(self)
        self.name = "default"
        self.default()
        self._restrictions = []

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

    def check(self, value):
        txt = 'value = %r does not respect restrictions: ' % (value)
        ok = True
        for restriction in self._restrictions:
            if not restriction.check(value):
                ok = False
                txt += '\n  - %s' % restriction
        if not ok:
            raise ValueError, txt

    def add_restriction(self, restriction):
        self._restrictions.append(restriction)

    def clear_restrictions(self):
        for i in range(len(self._restrictions)):
            self._restrictions.pop()

    def restriction(self, name):
        for restriction in self._restrictions:
            if restriction.__class__.__name__ == name:
                return restriction

    def _get_restriction_names(self):
        return sorted([r.__class__.__name__ for r in self._restrictions])

    restriction_names = property(fget=_get_restriction_names)
