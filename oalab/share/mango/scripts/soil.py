"""Add a soil to the scene
"""
from openalea.plantgl.all import *
import numpy as np

size = 1000.

heights=(np.random.random_sample((size,size))*.1).tolist()
grid = Shape(Translated((-size/2.,-size/2.,0), ElevationGrid(heights)), Material(Color3(149,109,0)))

scene['grid'] = grid