

from openalea.core.world import World, WorldObject
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
                          values={0: {0: self.world, 1: None, 2: obj}}
                          )
        attribute_dict = dict(name='attr1', value=1, interface='IInt', label="Attribute 1")
        final_dict = dict(name='attr1', value=1, interface='IInt', label="Attribute 1", constraints=None)
        obj.set_attribute(**attribute_dict)
        events = ev.events
        self.check_events(events,
                          names=['world_object_item_changed'],
                          values={0: {0: self.world, 1: obj, 2: "attribute", 3: None, 4: final_dict}}
                          )
        assert obj['attr1'] == attribute_dict['value']
