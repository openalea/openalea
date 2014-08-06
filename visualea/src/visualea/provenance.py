from openalea.vpltk.qt import QtGui, QtCore


class ProvenanceSelectorWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ProvenanceSelectorWidget, self).__init__(parent)
        layout = QtGui.QGridLayout(self)
        
        c_n_list = ["A","B","C"]
        pkgs_list = ["a","b","c"]
        workspace_list = ["1","2","3"]
        
        layout.addWidget(QtGui.QLabel("Select Composite Node"), 0, 0)
        # self.c_n = QtGui.QLineEdit("")
        # layout.addWidget(self.c_n, 0, 1)
        self.c_n = QtGui.QComboBox()
        self.c_n.addItems(c_n_list)
        layout.addWidget(self.c_n, 0, 1)

        layout.addWidget(QtGui.QLabel("Select Package"), 1, 0)
        # self.pkg = QtGui.QLineEdit("")
        # layout.addWidget(self.pkg, 1, 1)
        self.pkg = QtGui.QComboBox()
        self.pkg.addItems(pkgs_list)
        layout.addWidget(self.pkg, 1, 1)
        
        layout.addWidget(QtGui.QLabel("Select Workspace"), 2, 0)
        # self.workspace = QtGui.QLineEdit("")
        # layout.addWidget(self.workspace, 2, 1)
        self.workspace = QtGui.QComboBox()
        self.workspace.addItems(workspace_list)
        layout.addWidget(self.workspace, 2, 1)

        
class ModalDialog(QtGui.QDialog):
    def __init__(self, widget, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setModal(True)

        _bbox = QtGui.QDialogButtonBox
        bbox = _bbox(_bbox.Ok | _bbox.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)

        ok = bbox.button(_bbox.Ok)
        ok.setDefault(True)

        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.addWidget(widget)
        layout.addWidget(bbox)
        
        
def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    prov_widget = ProvenanceSelectorWidget()
    
    dialog = ModalDialog(prov_widget)
    dialog.show()
    dialog.raise_()
    app.exec_()
    
    if dialog.exec_():
        # print prov_widget.c_n.text()
        # print prov_widget.pkg.text()
        # print prov_widget.workspace.text()
        print prov_widget.c_n.currentText()
        print prov_widget.pkg.currentText()
        print prov_widget.workspace.currentText()

if( __name__ == "__main__"):
    main()
