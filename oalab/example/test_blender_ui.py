

from openalea.vpltk.qt import QtGui
from openalea.oalab.gui.splittablewindow import TestMainWin


if __name__ == '__main__':

    instance = QtGui.QApplication.instance()

    if instance is None:
        app = QtGui.QApplication([])
    else:
        app = instance

    oalab_conf = ({0: [1, 2], 2: [3, 4], 3: [5, 6], 6: [7, 8]},
                  {0: None, 1: 0, 2: 0, 3: 2, 4: 2, 5: 3, 6: 3, 7: 6, 8: 6},
                  {0: {'amount': 0.0645446507515473, 'splitDirection': 2},
                   1: {'widget': {'applet': ['ContextualMenu'], 'position': 0}},
                   2: {'amount': 0.75, 'splitDirection': 2},
                   3: {'amount': 0.2, 'splitDirection': 1},
                   4: {'widget': {'applet': ['ShellWidget', u'Logger', u'HistoryWidget'],
                                  'position': 0}},
                   5: {'widget': {'applet': ['ProjectManager',
                                             'PkgManagerWidget',
                                             'ControlManager',
                                             'World'],
                                  'position': 0}},
                   6: {'amount': 0.6, 'splitDirection': 1},
                   7: {'widget': {'applet': ['EditorManager'], 'position': 0}},
                   8: {'widget': {'applet': ['VtkViewer', 'LineageViewer', 'HelpWidget'],
                                  'position': 0}}})

    tissuelab_conf = ({0: [1, 2], 2: [3, 4], 3: [5, 6], 4: [7, 8], 7: [11, 12], 8: [9, 10]},
                      {0: None, 1: 0, 2: 0, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 8, 10: 8, 11: 7, 12: 7},
                      {0: {'amount': 0.0645446507515473, 'splitDirection': 2},
                       1: {'widget': {'applet': [u'ContextualMenu'], 'position': 0}},
                       2: {'amount': 0.1609375, 'splitDirection': 1},
                       3: {'amount': 0.4850467289719626, 'splitDirection': 2},
                       4: {'amount': 0.7436216552582452, 'splitDirection': 1},
                       5: {'widget': {'applet': [u'ProjectManager'], 'position': 0}},
                       6: {'widget': {'applet': [u'ControlManager',
                                                 u'World',
                                                 u'PkgManagerWidget',
                                                 u'Plot2d'],
                                      'position': 0}},
                       7: {'amount': 0.7252336448598131, 'splitDirection': 2},
                       8: {'amount': 0.4803738317757009, 'splitDirection': 2},
                       9: {'widget': {'applet': [u'VtkViewer', u'LineageViewer'], 'position': 0}},
                       10: {'widget': {'applet': [u'Viewer3D', u'Plot2d'], 'position': 0}},
                       11: {'widget': {'applet': [u'EditorManager'], 'position': 0}},
                       12: {'widget': {'applet': [u'ShellWidget',
                                                  u'HistoryWidget',
                                                  u'HelpWidget',
                                                  u'Logger'],
                                       'position': 2}}})

    def hello_world():
        print 'Hello OpenAleaLab world'

    from openalea.core.service.plugin import PIM
    PIM.debug = True
    mw = TestMainWin(tests=[hello_world])

    mw.resize(1024, 768)
    mw.showMaximized()
    mw.show()
    mw.set_edit_mode(False)

    mw.initialize()

    if instance is None:
        app.exec_()
