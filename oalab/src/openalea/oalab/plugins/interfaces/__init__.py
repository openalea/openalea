
class OpenAleaLabInterfacePlugin(object):
    name = 'OpenAleaLabInterfacePlugin'

    def __call__(self):

        from openalea.core.plugin.applet import IApplet
        #from openalea.oalab.interfaces.types import IColorList, ICurve2D

        all = [IApplet]
        return all


class ColormapInterfacePlugin(object):
    name = 'ColormapInterfacePlugin'

    def __call__(self):

        from openalea.oalab.plugins.interface import IColormap, IIntRange

        all = [IColormap, IIntRange]
        return all
