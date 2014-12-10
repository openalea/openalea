
##############################
## Don't forget to define  control n !
##############################

from openalea.plantgl.all import Sphere, Translated, Box

class IntSphere(object):
    def __init__(self, pos_x):
        self.pos_x = pos_x

    def __call__(self, r):
        sphere =Sphere(r/10.)
        return Translated(self.pos_x,0,0,sphere)

class IntCube(object):
    def __init__(self, pos_x):
        self.pos_x = pos_x

    def __call__(self, r):
        sphere =Box(r/10., r/10., r/10.)
        return Translated(self.pos_x,0,0,sphere)

world.clear()
for i in range(n):
    if i%2:
        transform = IntSphere
    else:
        transform = IntCube
    print(transform)
    world.add(i, transform=transform(i))

world.add(2, transform=transform(-1))
world.add(2, transform=transform(-2))