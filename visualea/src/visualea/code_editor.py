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
        self.textedit = self.get_editor()

        vboxlayout = QtGui.QVBoxLayout(self)
        vboxlayout.setMargin(3)
        vboxlayout.setSpacing(5)
        hboxlayout = QtGui.QHBoxLayout()
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)
        self.but1 = QtGui.QPushButton("Apply changes", self)
        self.but2 = QtGui.QPushButton("Save changes", self)
        hboxlayout.addWidget(self.but1)
        hboxlayout.addWidget(self.but2)
        vboxlayout.addLayout(hboxlayout)
        vboxlayout.addWidget(self.textedit)

        self.label = QtGui.QLabel("")
        vboxlayout.addWidget(self.label)

        self.connect(self.but1, QtCore.SIGNAL("clicked()"), self.apply_changes)
        self.connect(self.but2, QtCore.SIGNAL("clicked()"), self.save_changes)
        

    def get_editor(self):
        """
        Return an editor object based on QScintilla if available.
        Else, return a standard editor.
        """

        try:
            from PyQt4.Qsci import QsciScintilla, QsciLexerPython
            
            textedit = QsciScintilla()
            textedit.setLexer(QsciLexerPython())
            textedit.setMinimumWidth(500)
            textedit.setMinimumHeight(400)

            
        except:
            textedit = QtGui.QTextEdit(self)
            textedit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
            textedit.setMinimumWidth(500)
            textedit.setMinimumHeight(400)

        return textedit

    def setText(self, str):
        """ Set the text of the editor """

        try:
            self.textedit.setText(str)
        except:
            self.textedit.setPlainText(str)


    def text():
        """ Return editor text """
        try:
            return self.textedit.text()
        except:
            return self.textedit.toPlainText()
        

    def edit_class(self, nodefactory):
        """
        Open class source in editor,
        """
        self.factory = nodefactory
        try:
            self.src = nodefactory.get_node_src()
            self.textedit.setText(self.src)
            self.label.setText("Module : " + self.factory.nodemodule_path)
        except:
            self.src = None
            self.but1.setEnabled(False)
            self.but2.setEnabled(False)
            self.textedit.setText(" Sources are not available...")
            

    def apply_changes(self):
        
        self.src = str(self.text())
        self.factory.apply_new_src(self.src)


    def save_changes(self):
        """ Save module """

        ret = QtGui.QMessageBox.question(self, "Save",
                                         "Modification will be written in the module\n"+
                                         "Continue ?\n",
                                         QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,)

        if(ret == QtGui.QMessageBox.No): return

        module_name = self.factory.nodemodule_name
        newsrc = str(self.text())

        self.factory.save_new_src(newsrc)



