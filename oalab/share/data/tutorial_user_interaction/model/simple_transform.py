
from openalea.plantgl.all import Translated, Sphere

def point(i):
    return Translated(i, 0, 0, Sphere(1))

world.clear()
for i in range(10):
	world.add(-50+i**2, transform=point)
