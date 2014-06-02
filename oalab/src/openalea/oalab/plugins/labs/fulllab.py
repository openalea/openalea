from openalea.vpltk.plugin import iter_plugins

class FullLab(object):

    name = 'full'

    def __call__(self, mainwin):
        plugins = []
        for plugin in iter_plugins('oalab.applet'):
            plug = plugin()
            plugins.append(plug)
            mainwin.add_plugin(plug)

        for plugin in plugins:
            instance = plugin.instance()
            if hasattr(instance, "initialize"):
                instance.initialize()