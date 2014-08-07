from openalea.deploy.shared_data import shared_data
import openalea.mtg
from openalea.mtg import *

data = shared_data(openalea.mtg)

g = MTG(data/'noylum2.mtg')

dressing_data = dresser.DressingData(DiameterUnit=10)
pf = PlantFrame(g,TopDiameter='TopDia',DressingData = dressing_data)

world['lpy_scene'] = pf.plot(gc=True, display=False)

def init():
  del world['lpy_scene']
