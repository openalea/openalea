from openalea.core.plugin import PluginDef


def connect(old, new, sender_str, receiver_str, existing_connections):
    sender_name, signal_name = sender_str.split(':')
    receiver_name, slot_name = receiver_str.split(':')

    if old == new:
        return
    if new not in (sender_name, receiver_name):
        return

    signals = []
    slots = []

    from openalea.core.service.plugin import plugin_instance_exists, plugin_instances

    if plugin_instance_exists('oalab.applet', sender_name):
        for sender in plugin_instances('oalab.applet', sender_name):
            if hasattr(sender, signal_name):
                signals.append(getattr(sender, signal_name))

    if plugin_instance_exists('oalab.applet', receiver_name):
        for receiver in plugin_instances('oalab.applet', receiver_name):
            if hasattr(receiver, slot_name):
                slots.append(getattr(receiver, slot_name))

    if signals and slots:
        for i, signal in enumerate(signals):
            for j, slot in enumerate(slots):
                connection = '%s_%d -> %s_%d' % (sender_str, i, receiver_str, j)
                if connection not in existing_connections:
                    signal.connect(slot)
                    existing_connections.append(connection)
                else:
                    pass


class MiniLab(object):
    state = 'stopped'
    existing_connections = []  # list to store all created connections
    connections = []

    name = 'mini'
    label = 'IPython'
    icon = 'oxygen_utilities-terminal.png'
    applets = ['EditorManager']

    # NEW LAYOUT API
    menu_names = ('File', 'Edit', 'Help')

    layout = {'parents': {0: None, 1: 0, 2: 0, 3: 1, 4: 1},
              'properties': {0: {u'amount': 0.6957746478873239,
                                 u'splitDirection': 2},
                             1: {u'amount': 0.15247108307045215,
                                 u'splitDirection': 1},
                             2: {u'widget': {'applets': [{'name': u'ShellWidget'}],
                                             'properties': {}}},
                             3: {u'widget': {'applets': [{'name': u'ProjectManager'}],
                                             'properties': {}}},
                             4: {u'widget': {'applets': [{'name': u'EditorManager'}],
                                             'properties': {}}}},
              'children': {0: [1, 2], 1: [3, 4]}}

    def __call__(self, mainwin=None):
        if mainwin is None:
            return self.__class__
        # Load, create and place applets in mainwindow
        for name in self.applets:
            mainwin.add_plugin(name=name)
        # Initialize all applets
        mainwin.initialize()

    @classmethod
    def _connect(cls, old, new, sender, receiver):
        connect(old, new, sender, receiver, cls.existing_connections)

    @classmethod
    def connect_applet(cls, old, new):
        for connection in cls.connections:
            cls._connect(old, new, *connection)

    @classmethod
    def start(cls, *args, **kwds):
        cls.state = "started"

    @classmethod
    def initialize(cls, *args, **kwds):
        from openalea.core.service.plugin import plugin_instance_exists, plugin_instance
        if plugin_instance_exists('oalab.applet', 'ProjectManager'):
            from openalea.core.service.project import default_project
            project_applet = plugin_instance('oalab.applet', 'ProjectManager')
            project = default_project()
            project_applet.set_project(project)

        cls.state = "initialized"

    @classmethod
    def readytoclose(cls, *args, **kwds):
        return True

    @classmethod
    def finalize(cls, *args, **kwds):
        cls.state = "finalized"

    @classmethod
    def stop(cls, *args, **kwds):
        cls.state = "stopped"


@PluginDef
class IPythonLab(MiniLab):
    name = 'ipython'
