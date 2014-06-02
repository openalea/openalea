
from openalea.core.interface import IInterface

class IColorList(IInterface):
    """

    IIntControl is a Control with this specific method:
        - set_range(range), with range a couple of int.
    """
    interface = 'IColorList'
    def __init__(self):
        self.value = self.default()

    def __repr__(self):
        return 'IColorList'

    def default(self):
        """
        Reinitialize control to default value
        """
        from openalea.plantgl.all import Material, Color3
        value = [
            Material("Color_0"),
            Material("Color_0", Color3(65, 45, 15)), # Brown
            Material("Color_2", Color3(30, 60, 10)), # Green
            Material("Color_3", Color3(60, 0, 0)), # Red
            Material("Color_4", Color3(60, 60, 15)), # Yellow
            Material("Color_5", Color3(0, 0, 60)), # Blue
            Material("Color_6", Color3(60, 0, 60)), # Purple
            ]
        return value
