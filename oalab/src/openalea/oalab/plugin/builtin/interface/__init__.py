
from openalea.core.plugin import PluginDef


@PluginDef
class OpenAleaLabInterfacePlugin(object):

    def __call__(self):

        from openalea.oalab.plugin.applet import IApplet
        from openalea.oalab.interface import IColormap, IIntRange

        return [IColormap, IIntRange, IApplet]
