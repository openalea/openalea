from openalea.deploy.shared_data import shared_data
import openalea.mtg
from openalea.mtg import *

data = shared_data(openalea.mtg)

################################################################################
# 1. Object is directly compatible with viewer. Nothing to do
################################################################################

# Create object (big tree)
g2 = MTG(data / 'agraf.mtg')
dressing_data2 = dresser.DressingData(DiameterUnit=15)
pf2 = PlantFrame(g2, TopDiameter='TopDia', DressingData=dressing_data2)
pgl_scene = pf2.plot(gc=True, display=False)

# Add it to world
world['obj1'] = pgl_scene

################################################################################
# 2. Object is not directly compatible but provides
# a method (_repr_geom_) to convert himself to a compatible type
# (Currently PlantGL geometry, shape or scene)
################################################################################

# object type (generally defined in a separated module)
from openalea.plantgl.all import Box


class MyBox(object):

    def __init__(self, lx, ly, lz):
        self.lx = lx
        self.ly = ly
        self.lz = lz

    def _repr_geom_(self):
        """
        Returns an object compatible with "geom" viewer
        """
        return Box(self.lx, self.ly, self.lz)


# Create object (box)
b = MyBox(50, 40, 40)
# Add it to world
world['obj2'] = b

################################################################################
# 3. Object is not compatible and cannot convert himself to a compatible one.
# In this case, we define an adapter and register it.
# Once registered, Viewer can use it automatically
# Here, adapter is defined and register in module but that could be done via plugins.
################################################################################

# Define and register adapter. (generally defined in a separated plugin)
from openalea.oalab.service.geometry import register_shape3d


def to_shape3d(obj):
    if isinstance(obj, PlantFrame):
        return pf.plot(gc=True, display=False)
register_shape3d(PlantFrame, to_shape3d)

# Create object (small tree)
g = MTG(data / 'noylum2.mtg')
dressing_data = dresser.DressingData(DiameterUnit=10)
pf = PlantFrame(g, TopDiameter='TopDia', DressingData=dressing_data)

# Add it to world
world['obj3'] = pf
world['obj3'].displayed = True
world['obj3'].repr = 'geom'

world['i1'] = 1


def init():
    del world['i1'], world['obj1'], world['obj2'], world['obj3']
