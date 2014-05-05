#######################
#Duplicate the tree several times.
#######################
from openalea.plantgl.all import *

import numpy as np
from random import sample

name = "mangotree"
tree = world[name]

iter = 0
nb_step = 20

def duplicate(plant, nb_plants=nb_step, nx=10, ny=10):
  global iter, nb_step
  
  box = BoundingBox(plant)
  x, y, z = box.getSize()

  xstep = x*nx/nb_plants/10
  ystep = y*ny/nb_plants/10
  
  xmax = xstep * nx
  ymax = ystep * ny
  
  pts = sample([(i*xstep-xmax/2,j*ystep-ymax/2,0 ) for i in range(nx) for j in range(ny)], nb_plants)
  
  """
  x_step = nx/(x)
  y_step = ny/(y)
  
  dXmin, dXmax = -nx/2., nx/2.
  dYmin, dYmax = -nx/2., nx/2.
  
  nb_x = int(x_step)
  nb_y = int(y_step)
  print x_step, y_step
  pts = sample([(dXmin+i*x_step/2., dYmin+j*y_step/2.,0 ) for i in range(nx) for j in range(ny)], nb_plants)
    """
  for k,pt in enumerate(pts):
    world['%s_%d'%(name,(k+iter))] = Scene([Shape(Translated(pt,sh.geometry),sh.appearance) for sh in tree])

def step():
  global iter, nb_step
  if iter < nb_step:
    duplicate(tree, 1)
    iter += 1
  else:
    init()
  
def animate():
  global iter, nb_step
  if nb_step <= iter:
    init()
  
  for i in range(nb_step - iter):
    step()

def init():
  global iter
  iter = 0
  world.block()
  for plant_name in world:
    if plant_name[-1].isdigit():
      del world[plant_name]
  world.release()

def run():
  world.block()
  animate()
  world.release()
  
run()
