
from openalea.oalab.world import World, WorldObject


def test_world_objects():
    world = World()
    wo = WorldObject(name='o', data=1)
    assert wo.name == 'o'
    assert wo.data == 1
