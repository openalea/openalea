# -*- python -*-
#
#       OpenAlea.SecondNature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "CeCILL v2"
__revision__ = " $Id$ "


from openalea.vpltk.qt import QtGui, QtCore


class DataEditorSelector(QtGui.QDialog):
    def __init__(self, items, parent=None):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowOkButtonHint|
                                             QtCore.Qt.WindowCancelButtonHint)
        self.setWindowTitle("Select a tool")
        self.__l = QtGui.QVBoxLayout()
        self.__itemList = QtGui.QListWidget()
        self.__buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                                QtGui.QDialogButtonBox.Cancel)
        self.__l.addWidget(self.__itemList)
        self.__l.addWidget(self.__buttons)
        self.setLayout(self.__l)
        self.__itemList.addItems(items)
        self.__buttons.accepted.connect(self.accept)
        self.__buttons.rejected.connect(self.reject)

    def get_selected(self):
        return self.__itemList.currentItem().text()


    @staticmethod
    def mime_type_handler(formats, applet=True):
        from openalea.secondnature.applets import AppletFactoryManager
        from openalea.secondnature.data    import DataFactoryManager

        formats = map(str, formats)
        if applet:
            handlers = AppletFactoryManager().get_handlers_for_mimedata(formats)
        else:
            handlers = DataFactoryManager().get_handlers_for_mimedata(formats)

        nbHandlers = len(handlers)
        if nbHandlers == 0:
            return
        elif nbHandlers == 1:
            fac = handlers[0]
        elif nbHandlers > 1:
            selector = DataEditorSelector( [h.name for h in handlers] )
            if selector.exec_() == QtGui.QDialog.Rejected:
                return
            else:
                facName = selector.get_selected()
                fac = filter(lambda x: x.name == facName, handlers)[0]
        return fac

