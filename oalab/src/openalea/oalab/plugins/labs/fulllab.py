from openalea.vpltk.plugin import iter_plugins

class FullLab(object):

    name = 'full'

    def __call__(self, mainwin):
        for plugin in iter_plugins('oalab.applet'):
            mainwin.add_plugin(plugin())
