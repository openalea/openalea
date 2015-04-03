

from openalea.oalab.world import World, WorldObject
from openalea.core.unittest_tools import TestCase, EventTracker

ev = EventTracker()


class WorldTest(TestCase):

    def setUp(self):
        ev.events
        self.world = World()
        self.world.register_listener(ev)

    def tearDown(self):
        self.world.unregister_listener(ev)
        ev.events
        del self.world

    def test_world_objects(self):
        wo = WorldObject(name='o', data=1)
        assert wo.name == 'o'
        assert wo.data == 1

    def test_world(self):
        obj = self.world.add(1, 'a')
        events = ev.events
        self.check_events(events,
                          names=['world_object_changed'],
                          values={0: {1: self.world, 2: None, 3: obj}}
                          )
