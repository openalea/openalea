
class MiniLab(object):

    name = 'mini'
    alias = 'IPython'
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
