
class OpenAleaLabInterfacePlugin(object):
    name = 'OpenAleaLabInterfacePlugin'

    def __call__(self):

        from openalea.core.plugin.applet import IApplet
        #from openalea.oalab.interfaces.types import IColorList, ICurve2D

        all = [IApplet]
        return all

