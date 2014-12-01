
class ContextualMenu(object):

    name = 'ContextualMenu'
    alias = 'Contextual Menu'

    def __call__(self):
        from openalea.oalab.gui.menu import ContextualMenu
        return ContextualMenu

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None

        if applet is None or mainwindow is None:
            return
