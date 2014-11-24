from openalea.vpltk.qt import QtGui, QtCore
import sqlite3
from openalea.core.path import path
from openalea.core import settings
import subprocess
import time


def search_trace(composite_node, package, workspace, parent=None):
    """
    Search an execution trace of dataflow
    
    :param composite_node:
    :param package:
    :param workspace:
    """
    from openalea.core.provenance import db_connexion
    # @Moussa : This is here that you interrogate the database
    # print composite_node, package, workspace
    #cur = db_connexion()
    # Fake results:
    #seach in database specification and all trace for this Composite_node, package and workspace.
    nameval=workspace+"."+package+"."+composite_node
    cur=db_connexion()
    #cur.close()
    #cur=db_connexion()
    #createtimeval=time.strftime("%a, %d-%m-%Y %H:%M:%S", time.localtime())
    creatimeval="02-05-1988"
    descriptionval='sdfsqsd'
    useridval=1
    print nameval
    #data=[(creatimeval,nameval,descriptionval,useridval)]
    #for tu in data:
    #      cur.execute("INSERT INTO CompositeNode(CompositeNodeid,creatime,name,description,userid) VALUES(NULL,?,?,?,?)",tu)
    cur.execute("SELECT * FROM CompositeNode where name=? ",(nameval,))
    #cur.execute("SELECT * FROM CompositeNode")
    print 'Affichage de tous les compositeNode'
    for row in cur:
        #CompositeNodeidval=cur.fetchone()[0]
        CompositeNodeidval=row[0]
        date=row[1]
    cur.execute("SELECT * FROM CompositeNode where name=? ",(nameval,))
    for l in cur:
        print(l)
    #CompositeNodeidVal=res.fetchone()
    #print 'la valeur de CompositeNodeidVal est :',CompositeNodeidVal[0]
    print 'Affichages de toutes les traces de CompositeNode'
    #print cur.fetchone()[0]
    #CompositeNodeidval=1
    print CompositeNodeidval
    #CompositeNodeidVal=1
    cur.execute("SELECT * FROM CompositeNodeExec where CompositeNodeid=? ",(CompositeNodeidval,))
    i=0
    #myid=[]
    for rows in cur:
        print(l)
    #    myid[i]=rows[0]
        date2=rows[1]
        i=i+1
    #    print myid[i] 
    print 'Affichage de toutes les executions de noeud associees a cette trace'
    CompositeNodeExecidval=1
    cur.execute("SELECT * FROM NodeExec where CompositeNodeExecid=? ",(CompositeNodeExecidval,))
    for l in cur:
        print(l)
    #print 'Affichage de tous les arcs associees a cette trace'
    #cur.execute("SELECT * FROM elt_connection where CompositeNodeid=? ",(CompositeNodeidval,))
    #for l in cur:
    #    print(l)
    #print 'Affichage de tous les arcs associees a cette trace'
    #cur.execute("SELECT * FROM Node")
    #print 'Affichage de tous les nodes'
    #for l in cur:
    #    print(l)
    #cur.execute("SELECT * FROM CompositeNodeExec")
    #print 'Affichage de tous les CompositeNodeExec'
    #for l in cur:
    #    print(l)
    #seach in database specification and all trace for this Composite_node, package and workspace.
    nameval=workspace+"."+package+"."+composite_node
    # cur = db_connexion()
    #cur.execute("SELECT * FROM CompositeNode where name=? ",nameval)
    # cur.execute("SELECT * FROM CompositeNode")
    # for l in cur:
       # print(l)

    value1 = 0
    value2 = 1
    value3 = 2
    value4 = 100
    value5 = 1000
    # Faire la recherche dans la base de donnees pour rechercher le composite_node le package et le workfspace
    # Concatener le composite_node, le package et le workspace pour avoir le name du workflow
    # select * from 
    result = [["specification", date, CompositeNodeidval], ["Execution 1", date2, value2], ["Execution 2", "date", value3], ["Execution 3", "date", value4], ["Execution 4", "date", value5]]
    
    prov_widget = ProvenanceViewerWidget(composite_node, package, workspace, result, parent=parent)
    print composite_node
    print package
    print workspace
    print 'helo'
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
            btn.category = exe
            btn.clicked.connect(self.show_provenance)
            layout.addWidget(btn, i, 2)
            i += 1
    
    def show_provenance(self):
        from openalea.core.provenance import db_connexion
        cur=db_connexion()
        sender = self.sender()
        category = sender.category
        value = sender.prov
        if "spec" in category:
            # Launch Visualea
            #pass
            print value
            cur.execute("SELECT * FROM CompositeNode where CompositeNodeid=? ",(value,))
            for l in cur:
                print(l)
        else:
            # Launch Graphviz
            print value
            cur.execute("SELECT * FROM CompositeNodeExec where CompositeNodeExecid=? ",(value,))
            for l in cur:
                print(l)
            cur.execute("SELECT * FROM NodeExec where CompositeNodeExecid=? ",(value,))
            for l in cur:
                print(l)
            #cd='chdir("C:/Program Files/Graphviz2.38/bin")'
            
            cmd = "gvedit.exe"
            subprocess.call(cd)
            subprocess.call(cmd)
        
class ProvenanceSelectorWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ProvenanceSelectorWidget, self).__init__(parent)
        layout = QtGui.QFormLayout(self)

        layout.addRow(QtGui.QLabel("<H2>Search an execution trace of dataflow</H2>"))
        
        self.c_n = QtGui.QLineEdit("")
        layout.addRow("Select Composite Node", self.c_n)

        self.pkg = QtGui.QLineEdit("")
        layout.addRow("Select Package", self.pkg)
        
        self.workspace = QtGui.QLineEdit("")
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
