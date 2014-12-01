

from openalea.vpltk.qt import QtGui
from openalea.oalab.gui.splittablewindow import TestMainWin


if __name__ == '__main__':

    instance = QtGui.QApplication.instance()

    if instance is None:
        app = QtGui.QApplication([])
    else:
        app = instance

    tissuelab_conf = ({0: [1, 2], 2: [3, 4], 3: [5, 6], 4: [7, 8], 7: [11, 12], 8: [9, 10]},
                      {0: None, 1: 0, 2: 0, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 8, 10: 8, 11: 7, 12: 7},
                      {0: {'amount': 0.04774535809018567, 'splitDirection': 2},
                       1: {'widget':
                           {'applets': [
                               {'name': u'ContextualMenu'}],
                            'properties': {'position': 0}
                            }},
                       2: {'amount': 0.1609375, 'splitDirection': 1},
                       3: {'amount': 0.4850467289719626, 'splitDirection': 2},
                       4: {'amount': 0.6540136901057871, 'splitDirection': 1},
                       5: {'widget':
                           {'applets': [
                               {'name': u'ProjectManager'}],
                            'properties': {'position': 0}
                            }},
                       6: {'widget':
                           {'applets': [
                               {'name': u'ControlManager'},
                               {'name': u'World'},
                               {'name': u'PkgManagerWidget'}],
                            'properties': {'position': 0}
                            }},
                       7: {'amount': 0.7252336448598131, 'splitDirection': 2},
                       8: {'amount': 0.4803738317757009, 'splitDirection': 2},
                       9: {'widget':
                           {'applets': [
                               {'name': u'LineageViewer'},
                               {'name': u'FigureWidget'},
                               {'name': u'FigureWidget'}],
                            'properties': {'position': 2}
                            }},
                       10: {'widget':
                            {'applets': [
                                {'name': u'Viewer3D'},
                                {'name': u'VtkViewer'}],
                             'properties': {'position': 2}}},
                       11: {'widget':
                            {'applets': [
                                {'name': u'EditorManager'}],
                             'properties': {'position': 0}}},
                       12: {'widget':
                            {'applets': [
                                {'name': u'ShellWidget'},
                                {'name': u'HistoryWidget'},
                                {'name': u'HelpWidget'},
                                {'name': u'Logger'}],
                             'properties': {'position': 2}
                             }}
                       })

    def hello_world():
        print 'Hello OpenAleaLab world'

    from openalea.core.service.plugin import PIM
    PIM.debug = True
    TestMainWin.DEFAULT_LAYOUT = tissuelab_conf
    mw = TestMainWin(tests=[hello_world])

    mw.resize(1024, 768)
    mw.showMaximized()
    mw.show()
    mw.set_edit_mode(False)

    mw.initialize()

    if instance is None:
        app.exec_()
