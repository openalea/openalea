
class OpenAleaLabInterfacePlugin(object):

    def __call__(self):

        from openalea.oalab.plugins.applet import IApplet
        #from openalea.oalab.interfaces.types import IColorList, ICurve2D

        all = [IApplet]
        return all

