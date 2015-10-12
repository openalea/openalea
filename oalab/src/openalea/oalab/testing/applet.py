
from openalea.oalab.widget.splittablewindow import OALabMainWin
from openalea.vpltk.qt import QtCore, QtGui
from openalea.core.service.ipython import interpreter
from openalea.core.service.plugin import (plugin_instance_exists, plugin_instance,
                                          plugin_instances, plugins, debug_plugins)
from openalea.core.util import camel_case_to_lower


class TestMainWin(OALabMainWin):

    def __init__(self, layout=None, **kwds):
        """
        tests: list of function runnable in shell (name changed to run_<funcname>)
        layout_file
        """
        OALabMainWin.__init__(self, layout=layout, **kwds)

        self.interp = interpreter()
        self.interp.user_ns['mainwin'] = self
        self.interp.user_ns['splittable'] = self.splittable
        self.interp.user_ns['debug'] = self.debug
        self.interp.user_ns['QtCore'] = QtCore
        self.interp.user_ns['QtGui'] = QtGui

        def applet(name):
            return plugin_instance('oalab.applet', name)

        def applets(name):
            return plugin_instances('oalab.applet', name)

        self.interp.user_ns['applet'] = applet
        self.interp.user_ns['applets'] = applets

        print 'VARIABLES AVAILABLE IN SHELL ...'

        print '\nAPPLICATION:'
        print '  - mainwin'
        print '  - splittable'
        print '  - QtCore'
        print '  - QtGui'

        print '\nAPPLETS:'
        for plugin in plugins('oalab.applet'):
            if plugin_instance_exists('oalab.applet', plugin.name):
                varname = camel_case_to_lower(plugin.name)
                self.interp.user_ns['plugin_%s' % varname] = plugin
                self.interp.user_ns[varname] = plugin_instance('oalab.applet', plugin.name)
                print '  -', varname

        print '\nFUNCTIONS:'
        for f in kwds.pop('tests', []):
            self.interp.user_ns['run_%s' % f.__name__] = f
            f.func_globals['ns'] = self.interp.user_ns
            print '  - run_%s' % f.__name__

        self.resize(QtCore.QSize(800, 600))

    def debug(self):
        debug_plugins(True)


class TestApplet(TestMainWin):

    def __init__(self, applet, **kwds):
        layout = dict(children={0: [1, 2]},
                      parents={0: None, 1: 0, 2: 0},
                      properties={0: {'amount': 0.5, 'splitDirection': 1},
                                  1: {'widget': {'applets': [{'name': applet}]}},
                                  2: {'widget': {'applets': [{'name': 'ShellWidget'}]}},
                                  }
                      )

        TestMainWin.__init__(self, layout, **kwds)
        self.resize(1024, 768)
        self.show()

        self.initialize()


class TestTwoApplets(TestMainWin):

    def __init__(self, applet1, applet2, **kwds):
        layout = {
            "children": {
                "0": [
                    1,
                    2
                ],
                "1": [
                    3,
                    4
                ]
            },
            "parents": {
                "0": None,
                "1": 0,
                "2": 0,
                "3": 1,
                "4": 1
            },
            "properties": {
                "0": {"amount": 0.5, "splitDirection": 2},
                "1": {"amount": 0.25, "splitDirection": 1},
                "2": {"widget": {"applets": [{"name": "ShellWidget"}]}},
                "3": {"widget": {"applets": [{"name": applet1}]}},
                "4": {"widget": {"applets": [{"name": applet2}]}}
            }
        }

        TestMainWin.__init__(self, layout, **kwds)
        self.resize(1024, 768)
        self.show()

        self.initialize()


class TestNApplets(TestMainWin):

    def __init__(self, applets, **kwds):
        applets = [{'name': applet} for applet in applets]
        layout = dict(children={0: [1, 2]},
                      parents={0: None, 1: 0, 2: 0},
                      properties={0: {'amount': 0.5, 'splitDirection': 1},
                                  1: {'widget': {'applets': applets}},
                                  2: {'widget': {'applets': [{'name': 'ShellWidget'}]}},
                                  }
                      )

        TestMainWin.__init__(self, layout, **kwds)
        self.resize(1024, 768)
        self.show()

        self.initialize()


def test_applet(*args, **kwds):
    instance = QtGui.QApplication.instance()

    if instance is None:
        app = QtGui.QApplication([])
    else:
        app = instance

    if len(args) == 1:
        mw = TestApplet(*args, **kwds)
    elif len(args) == 2:
        mw = TestTwoApplets(*args, **kwds)
    else:
        mw = TestNApplets(args, **kwds)
    mw.show()

    if instance is None:
        return app.exec_()
