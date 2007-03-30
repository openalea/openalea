# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
Python code editor
"""

__license__= "CeCILL V2"
__revision__=" $Id$"




from PyQt4 import QtCore, QtGui



class NodeCodeEditor(QtGui.QWidget):
    """ Default node editor """

    def __init__(self, parent):
        
        QtGui.QWidget.__init__(self, parent)
        

        self.src = None
        self.textedit = QtGui.QTextEdit(self)
        self.textedit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textedit.setMinimumWidth(500)
        self.textedit.setMinimumHeight(400)
        vboxlayout = QtGui.QVBoxLayout(self)
        vboxlayout.setMargin(3)
        vboxlayout.setSpacing(5)
        hboxlayout = QtGui.QHBoxLayout()
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)
        but1 = QtGui.QPushButton("Apply changes", self)
        but2 = QtGui.QPushButton("Save changes", self)
        hboxlayout.addWidget(but1)
        hboxlayout.addWidget(but2)
        vboxlayout.addLayout(hboxlayout)
        vboxlayout.addWidget(self.textedit)

        self.connect(but1, QtCore.SIGNAL("clicked()"), self.apply_changes)
        self.connect(but2, QtCore.SIGNAL("clicked()"), self.save_changes)


    def edit_class(self, nodefactory):
        """
        Open class source in editor,
        """
        self.factory = nodefactory
        self.module = nodefactory.get_node_module()

        import inspect
        try:
            # get the code
            self.cl = self.module.__dict__[nodefactory.nodeclass_name]
            self.src = inspect.getsource(self.cl)
            self.textedit.setPlainText(self.src)
        except:
            self.textedit.setPlainText(" Sources are not available...")
            self.src = None
            

    def apply_changes(self):
        self.src = str(self.textedit.toPlainText())

        # Run src
        exec self.src in self.module.__dict__
             


    def save_changes(self):
        """ Save module """

        ret = QtGui.QMessageBox.question(self, "Save",
                                         "Modification will be written in the module\n"+
                                         "Continue ?\n",
                                         QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,)

        if(ret == QtGui.QMessageBox.No): return

        module_name = self.factory.nodemodule_name
        newsrc = str(self.textedit.toPlainText())

        # Run src
        exec newsrc in self.module.__dict__

        # get the module code
        import inspect
        modulesrc = inspect.getsource(self.module)
        # replace old code with new one
        modulesrc = modulesrc.replace(self.src, newsrc)
        print modulesrc
        # write file
        file = open(self.factory.nodemodule_path, 'w')
        file.write(modulesrc)
        file.close()
        self.factory.force_reload()



