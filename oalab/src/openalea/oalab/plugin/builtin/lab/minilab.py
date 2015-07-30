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


@PluginDef
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

    layout = {
        "children": {
            "0": [
                1,
                2
            ],
            "1": [
                5,
                6
            ],
            "6": [
                7,
                8
            ]
        },
        "interface": "ISplittableUi",
        "parents": {
            "0": None,
            "1": 0,
            "2": 0,
            "5": 1,
            "6": 1,
            "7": 6,
            "8": 6
        },
        "properties": {
            "0": {
                "amount": 0.7214854111405835,
                "splitDirection": 2
            },
            "1": {
                "amount": 0.06027060270602706,
                "splitDirection": 2
            },
            "2": {
                "widget": {
                    "applets": [
                        {
                            "ep": "oalab.applet",
                            "interface": "IPluginInstance",
                            "name": "ShellWidget",
                            "properties": {
                                "title": False,
                                "toolbar": False
                            }
                        }
                    ],
                    "interface": "IAppletContainer",
                    "properties": {
                        "position": 0
                    }
                }
            },
            "5": {
                "widget": {
                    "applets": [
                        {
                            "ep": "oalab.applet",
                            "interface": "IPluginInstance",
                            "name": "ContextualMenu",
                            "properties": {
                                "style": 0,
                                "title": False,
                                "toolbar": False
                            }
                        }
                    ],
                    "interface": "IAppletContainer",
                    "properties": {
                        "position": 0
                    }
                }
            },
            "6": {
                "amount": 0.15572916666666667,
                "splitDirection": 1
            },
            "7": {
                "widget": {
                    "applets": [
                        {
                            "ep": "oalab.applet",
                            "interface": "IPluginInstance",
                            "name": "ProjectManager",
                            "properties": {
                                "title": False,
                                "toolbar": False
                            }
                        }
                    ],
                    "interface": "IAppletContainer",
                    "properties": {
                        "position": 0
                    }
                }
            },
            "8": {
                "widget": {
                    "applets": [
                        {
                            "ep": "oalab.applet",
                            "interface": "IPluginInstance",
                            "name": "EditorManager",
                            "properties": {
                                "title": False,
                                "toolbar": False
                            }
                        }
                    ],
                    "interface": "IAppletContainer",
                    "properties": {
                        "position": 0
                    }
                }
            }
        }
    }

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
