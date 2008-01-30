# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
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
################################################################################


__doc__="""
Python code editor
"""

__license__= "CeCILL V2"
__revision__=" $Id$"


from PyQt4 import QtCore, QtGui
import os



class PythonCodeEditor(QtGui.QWidget):
    """ Simple Python code editor """

    def __init__(self, parent=None):
        
        QtGui.QWidget.__init__(self, parent)

        self.textedit = self.get_editor()

        vboxlayout = QtGui.QVBoxLayout(self)
        vboxlayout.setMargin(1)
        vboxlayout.setSpacing(1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(1)
        self.hboxlayout.setSpacing(1)
        self.applybut = QtGui.QPushButton("Apply changes", self)
        self.hboxlayout.addWidget(self.applybut)

        self.savbut = QtGui.QPushButton("Save changes", self)
        self.hboxlayout.addWidget(self.savbut)
        vboxlayout.addLayout(self.hboxlayout)
        vboxlayout.addWidget(self.textedit)


        self.label = QtGui.QLabel("")
        vboxlayout.addWidget(self.label)

        self.savescut = QtGui.QShortcut( QtGui.QKeySequence(QtGui.QKeySequence.Save), self)
        self.connect(self.savescut, QtCore.SIGNAL("activated()"), self.save_changes)
        self.connect(self.savbut, QtCore.SIGNAL("clicked()"), self.save_changes)
        self.connect(self.applybut, QtCore.SIGNAL("clicked()"), self.apply_changes)


        

    def get_editor(self):
        """
        Return an editor object based on QScintilla if available.
        Else, return a standard editor.
        """

        try:
            from PyQt4.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
            
            textedit = QsciScintilla(self)
            textedit.setAutoIndent(True)
            textedit.setAutoCompletionThreshold(2)
            textedit.setAutoCompletionSource(QsciScintilla.AcsDocument)

            # API
            lex = QsciLexerPython(textedit)
            textedit.setLexer(lex)

#             apis = QsciAPIs(lex)
#             apis.prepare()
            
            textedit.setMinimumWidth(250)
            textedit.setMinimumHeight(250)
            
        except ImportError:
            textedit = QtGui.QTextEdit(self)
            textedit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
            textedit.setMinimumWidth(200)
            textedit.setMinimumHeight(200)

        return textedit


    def setText(self, str):
        """ Set the text of the editor """

        try:
            self.textedit.setText(str)
        except:
            self.textedit.setPlainText(str)


    def getText(self):
        """ Return editor text """
        try:
            return self.textedit.text()
        except:
            return self.textedit.toPlainText()
        

    def edit_file(self, filename):
        """ Open file in the editor """
        
        if(filename):
            filename = os.path.abspath(filename)

        self.filename = filename

        try:
            f = open(filename, 'r')
            self.textedit.setText(f.read())
            self.label.setText("File : " + filename)
            f.close()
            self.savbut.setEnabled(True)
            self.applybut.setEnabled(False)


        except Exception, e:
            print e
            self.src = None
            self.applybut.setEnabled(False)
            self.savbut.setEnabled(False)
            self.textedit.setText(" Sources are not available...")


    def edit_module(self, module):
        """ Edit the source file of a python module """

        self.module = module
        if(not module):  
            self.applybut.setEnabled(False)
            return
            
        import inspect
        filename =  inspect.getsourcefile(module)
        self.edit_file(filename)

        self.savbut.setEnabled(True)
        self.applybut.setEnabled(True)


    def apply_changes(self):
        """ Reload file """

        if(self.module):
            newsrc = str(self.getText())
            exec newsrc in self.module.__dict__


    def save_changes(self):
        """ Save module """
        if(not os.access(self.filename, os.W_OK)):
            ret = QtGui.QMessageBox.warning(self, "Cannot write file %s", self.filename)
            return
            
            
        try:
            f = open(self.filename, 'w')
            f.write(str(self.getText()))
            self.label.setText("Write file : " + self.filename)
        finally:
            f.close()
            
            



class NodeCodeEditor(PythonCodeEditor):
    """ Default node editor """

    def __init__(self, factory, parent=None):
        
        PythonCodeEditor.__init__(self, parent)

        self.factory = factory
        self.src = None

        self.edit_class(factory)
        


    def edit_class(self, nodefactory):
        """ Open class source in editor """
        
        try:
            self.src = nodefactory.get_node_src()
            self.textedit.setText(self.src)
            self.label.setText("Module : " + self.factory.nodemodule_path)
        except Exception, e:
            print e
            self.src = None
            self.applybut.setEnabled(False)
            self.savbut.setEnabled(False)
            self.textedit.setText(" Sources are not available...")
            

    def apply_changes(self):
        """ Apply """
        self.src = str(self.getText())
        if(self.src != self.factory.get_node_src()):
            self.factory.apply_new_src(self.src)


    def save_changes(self):
        """ Save module """

        ret = QtGui.QMessageBox.question(self, "Save",
                                         "Modification will be written in the module\n"+
                                         "Continue ?\n",
                                         QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,)

        if(ret == QtGui.QMessageBox.No): return

        module_name = self.factory.nodemodule_name
        newsrc = str(self.getText())

        self.factory.save_new_src(newsrc)



