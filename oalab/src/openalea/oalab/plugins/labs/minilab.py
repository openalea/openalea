from openalea.vpltk.plugin import iter_plugins, check_dependencies

class MiniLab(object):

    name = 'mini'
    applets = ['EditorManager']

    def __call__(self, mainwin):
        session = mainwin.session
        for plugin in iter_plugins('oalab.applet', debug=session.debug_plugins):
            if plugin.name in self.applets:
                if check_dependencies(plugin):
                    mainwin.add_plugin(plugin())
