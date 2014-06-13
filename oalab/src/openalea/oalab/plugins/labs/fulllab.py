from openalea.vpltk.plugin import iter_plugins


class FullLab(object):
    name = 'full'

    def __call__(self, mainwin):
        plugins_used = []
        session = mainwin.session
        plugins_to_use = [plug for plug in iter_plugins('oalab.applet', debug=session.debug_plugins)]

        # Set editor manager, because it is used by other plugins
        for plugin in plugins_to_use:
            if plugin.name == "EditorManager":
                plug = plugin()
                plugins_used.append(plug)
                mainwin.add_plugin(plug)

        # Set other plugins
        for plugin in plugins_to_use:
            plug = plugin()
            if plugin.name not in [plu.name for plu in plugins_used]:
                plugins_used.append(plug)
                mainwin.add_plugin(plug)

        # Initialize all plugins
        for plugin in plugins_used:
            instance = plugin.instance()
            if hasattr(instance, "initialize"):
                instance.initialize()
