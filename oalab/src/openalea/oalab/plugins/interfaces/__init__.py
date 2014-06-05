
class OpenAleaLabInterfacePlugin(object):

    def __call__(self):

        from openalea.oalab.plugins.applet import IApplet
        from openalea.oalab.interfaces.types import IColorList, ICurve2D
        from openalea.core.interface import IInt, IBool

        all = [IApplet, IColorList, IInt, IBool, ICurve2D]
        return all

