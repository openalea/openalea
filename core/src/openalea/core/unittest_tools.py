
import unittest
from openalea.core.observer import AbstractListener


class EventTracker(AbstractListener):

    def __init__(self, debug=False):
        AbstractListener.__init__(self)
        self.debug = debug
        self._events = []

    def notify(self, sender, event=None):
        if self.debug:
            print sender, event
        self._events.append((sender, event))

    @property
    def events(self):
        lst = self._events
        self._events = []
        return lst


class TestCase(unittest.TestCase):

    def check_events(self, events, names=None, values=None):
        """
        values:
        dict {idx:[val, val2]}
        """
        ev_names = [event[1][0] for event in events]
        ev_args = [event[1][1] for event in events]
        self.assertListEqual(ev_names, names)
        if values:
            for event_idx, event in values.items():
                for arg_idx, arg in event.items():
                    self.assertEqual(ev_args[event_idx][arg_idx], arg)
