"""
input = nb_plants = 3, world_object=None
output = canopy_scene
"""
from openalea.plantgl.all import *

sx = sy = 30
nb_plants = int(nb_plants)
print nb_plants

def transform(scene):
    tr = [(i*sx, j*sy,0) for i in range(0,nb_plants) for j in range(0,nb_plants)]    
    sc = Scene()
    for t in tr:
        sc+= Scene([Shape(Translated(t,sh.geometry), sh.appearance) for sh in scene])
    return sc

_sc = world_object.obj._repr_geom_()

canopy_scene = transform(_sc)
print 'LENGTH'
print len(canopy_scene)    