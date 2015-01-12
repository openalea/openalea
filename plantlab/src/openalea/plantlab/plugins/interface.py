from openalea.plantlab.interface import *


class PlantGLOAInterfacePlugin(object):

    def __call__(self):

        all = [IColorList, IMaterialList, ICurve2D, IQuantisedFunction, IPatch]
        return all