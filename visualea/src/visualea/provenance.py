from openalea.vpltk.qt import QtGui, QtCore


def search_trace(composite_node, package, workspace, parent=None):
    """
    Search an execution trace of dataflow
    
    :param composite_node:
    :param package:
    :param workspace:
    """
    # @Moussa : This is here that you interrogate the database
    # print composite_node, package, workspace
    
    
    
    
    
    # Fake results:
    value1 = 0
    value2 = 1
    value3 = 5
    value4 = 10
    value5 = 42
    result = [["spec1", "date1", value1], ["exec1", "date2", value2], ["exec2", "date3", value3], ["spec2", "date4", value4], ["exec3", "date5", value5]]
    
    prov_widget = ProvenanceViewerWidget(composite_node, package, workspace, result, parent=parent)
    
    dialog = ModalDialog(prov_widget)
    dialog.show()
    dialog.raise_()
    dialog.exec_()


class ProvenanceViewerWidget(QtGui.QWidget):
    def __init__(self, composite_node, package, workspace, traces, parent=None):
        super(ProvenanceViewerWidget, self).__init__(parent)
        
        layout = QtGui.QGridLayout(self)
        label = QtGui.QLabel("Result of research from composite node " +composite_node+ " in package " + package + " with workspace " + workspace +" .")
        layout.addWidget(label, 0, 0, 1, -1)

        i = 1
        for trace in traces:
            exe, date, value = trace
            layout.addWidget(QtGui.QLabel(exe), i, 0)
            layout.addWidget(QtGui.QLabel(date), i, 1)
            btn = QtGui.QPushButton("show", parent=self)
            btn.prov = value
            btn.clicked.connect(self.show_provenance)
            layout.addWidget(btn, i, 2)
            i += 1
    
    def show_provenance(self):
        sender = self.sender()
        print sender.prov
        
class ProvenanceSelectorWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ProvenanceSelectorWidget, self).__init__(parent)
        layout = QtGui.QFormLayout(self)
        # c_n_list = ["A","B","C"]
        # pkgs_list = ["a","b","c"]
        # workspace_list = ["1","2","3"]
        
        layout.addRow(QtGui.QLabel("<H2>Search an execution trace of dataflow</H2>"))
        
        self.c_n = QtGui.QLineEdit("")
        # self.c_n = QtGui.QComboBox()
        # self.c_n.addItems(c_n_list)
        layout.addRow("Select Composite Node", self.c_n)

        self.pkg = QtGui.QLineEdit("")
        # self.pkg = QtGui.QComboBox()
        # self.pkg.addItems(pkgs_list)
        layout.addRow("Select Package", self.pkg)
        
        self.workspace = QtGui.QLineEdit("")
        # self.workspace = QtGui.QComboBox()
        # self.workspace.addItems(workspace_list)
        layout.addRow("Select Workspace", self.workspace)
        
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
        cn = prov_widget.c_n.text()
        pkg = prov_widget.pkg.text()
        wk = prov_widget.workspace.text()
        
        search_trace(cn, pkg, wk)
        # print prov_widget.c_n.currentText()
        # print prov_widget.pkg.currentText()
        # print prov_widget.workspace.currentText()

if( __name__ == "__main__"):
    main()
