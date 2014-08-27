from openalea.vpltk.plugin import iter_plugins, check_dependencies


class FullLab(object):
    name = 'full'

    def __call__(self, mainwin):
        from openalea.oalab.session.session import Session
        session = Session()
        for plugin in iter_plugins('oalab.applet', debug=session.debug_plugins):
            if check_dependencies(plugin):
                mainwin.add_plugin(plugin())
        mainwin.initialize()
