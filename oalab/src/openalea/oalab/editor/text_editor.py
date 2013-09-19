# -*- python -*-
# 
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = ""

from openalea.vpltk.qt import QtCore, QtGui
from openalea.core.path import path
from openalea.oalab.editor.search import SearchWidget
from openalea.oalab.editor.completion import DictionaryCompleter
from openalea.core import logger
from openalea.core import settings


class RichTextEditor(QtGui.QWidget):
    def __init__(self, session, parent=None):
        super(RichTextEditor, self).__init__(parent)
        
        self.completer = DictionaryCompleter(session=session, parent=self)
        self.editor = TextEditor(session=session, parent=self)
        self.editor.setCompleter(self.completer)
        
        self.search_widget = SearchWidget(parent=self,session=session )
        
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.editor)
        self.layout.addWidget(self.search_widget)
        self.setLayout(self.layout)
        
        self.search_widget.hide()

    def actions(self):
        """
        :return: list of actions to set in the menu.
        """
        return None

    def mainMenu(self):
        return "Simulation"
        
    def set_text(self, txt):
        """
        Set text in the editor
        
        :param text: text you want to set 
        """
        self.editor.set_text(txt)
        
        
    set_script = set_text
    
    def get_selected_text(self):
        return self.editor.get_selected_text()
    
    def get_text(self, start='sof', end='eof'):
        """
        Return a part of the text.
        
        :param start: is the begining of what you want to get
        :param end: is the end of what you want to get
        :return: text which is contained in the editor between 'start' and 'end'
        """
        return self.editor.get_text(start='sof', end='eof')
        
    def save(self, name=None):
        self.editor.save(name)
    
    def comment(self):
        self.editor.comment()
    
    def uncomment(self):
        self.editor.uncomment()
        
    def search(self):
        if self.search_widget.hiden:
            self.search_widget.show()
            #self.search_widget.raise_()
            self.search_widget.hiden = False
        else:
            self.search_widget.hide()
            self.search_widget.hiden = True

class TextEditor(QtGui.QTextEdit):
    def __init__(self, session, parent=None):
        super(TextEditor, self).__init__(parent)
        self.session = session
        self.indentation = "    "
        self.completer = None

    def actions(self):
        """
        :return: list of actions to set in the menu.
        """
        return None

    def mainMenu(self):
        return "Simulation"        
        
    def set_text(self, txt):
        """
        Set text in the editor
        
        :param text: text you want to set 
        """
        self.setText(txt)
        
        
    set_script = set_text
    
    def get_selected_text(self):
        cursor = self.textCursor()
        txt = cursor.selectedText()
        return txt
    
    def get_text(self, start='sof', end='eof'):
        """
        Return a part of the text.
        
        :param start: is the begining of what you want to get
        :param end: is the end of what you want to get
        :return: text which is contained in the editor between 'start' and 'end'
        """
        return self.toPlainText()
        
    def save(self, name=None):
        """
        Save current file.
        
        :param name: name of the file to save.
        If not name, self.name is used.
        If self.name is not setted and name is not give in parameter,
        a File Dialog is opened.
        """
        if name:
            self.name = name
            
        if not self.name:
            temp_path = path(settings.get_project_dir())
            self.name = QtGui.QFileDialog.getSaveFileName(self, 'Select name to save the file', 
                temp_path)

        # print "save text", name
        txt = self.get_full_text()
        project = self.session.project
        
        if self.session.current_is_project():
            project.scripts[self.name] = txt
            project._save_scripts()
            
        elif self.session.current_is_script():
            # Save a script outside a project
            fname = project.fname
            f = open(fname, "w")
            code = project.value
            code_enc = code.encode("utf8","ignore") 
            f.write(code_enc)
            f.close()

    def keyPressEvent(self,event):
        # Auto-indent
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            super(TextEditor, self).keyPressEvent(event)
            self.returnEvent()
            return
        
        elif self.completer and self.completer.popup().isVisible():
            if event.key() in (
            QtCore.Qt.Key_Enter,
            QtCore.Qt.Key_Return,
            QtCore.Qt.Key_Escape,
            QtCore.Qt.Key_Tab,
            QtCore.Qt.Key_Backtab):
                event.ignore()
                return

        ## has ctrl-E been pressed??
        isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier and
                      event.key() == QtCore.Qt.Key_E)
        if (not self.completer or not isShortcut):
            QtGui.QTextEdit.keyPressEvent(self, event)

        ## ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier ,
                QtCore.Qt.ShiftModifier)
        if ctrlOrShift and event.text() is str():
            # ctrl or shift key on it's own
            return

        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=" #end of word

        hasModifier = ((event.modifiers() != QtCore.Qt.NoModifier) and
                        not ctrlOrShift)

        completionPrefix = self.textUnderCursor()

        f = eow.find(event.text()[-1])
        if f == -1:
            finded = False
        else:
            finded = True

        if (not isShortcut and (hasModifier or (event.text() is str()) or
        len(completionPrefix) < 3 or finded)):
            self.completer.popup().hide()
            return

        if (completionPrefix != self.completer.completionPrefix()):
            self.completer.setCompletionPrefix(completionPrefix)
            popup = self.completer.popup()
            popup.setCurrentIndex(
                self.completer.completionModel().index(0,0))
         
        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0)
            + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr) ## popup it up!

    ####################################################################
    #### Auto Indent (cf lpycodeeditor)
    ####################################################################
    def returnEvent(self):
        cursor = self.textCursor()
        beg = cursor.selectionStart()
        end = cursor.selectionEnd()
        if beg == end:
            pos = cursor.position()
            ok = cursor.movePosition(QtGui.QTextCursor.PreviousBlock,QtGui.QTextCursor.MoveAnchor)
            if not ok: return
            txtok = True
            txt = ''
            while txtok:
                ok = cursor.movePosition(QtGui.QTextCursor.NextCharacter,QtGui.QTextCursor.KeepAnchor)
                if not ok: break
                txt2 = str(cursor.selection().toPlainText())
                txtok = (txt2[-1] in ' \t')
                if txtok:
                    txt = txt2
            cursor.setPosition(pos)
            ok = cursor.movePosition(QtGui.QTextCursor.PreviousBlock,QtGui.QTextCursor.MoveAnchor)
            if ok:
                ok = cursor.movePosition(QtGui.QTextCursor.EndOfBlock,QtGui.QTextCursor.MoveAnchor)
                if ok:
                    txtok = True
                    while txtok:
                        ok = cursor.movePosition(QtGui.QTextCursor.PreviousCharacter,QtGui.QTextCursor.KeepAnchor)
                        if not ok: break
                        txt2 = str(cursor.selection().toPlainText())
                        txtok = (txt2[0] in ' \t')
                        if not txtok:
                            if txt2[0] == ':':
                                txt += self.indentation
            cursor.setPosition(pos)
            cursor.joinPreviousEditBlock()
            cursor.insertText(txt)
            cursor.endEditBlock()
            
    ####################################################################
    #### (Un)Tab (cf lpycodeeditor)
    #### TODO
    ####################################################################
    #def tab(self, initcursor = None):
        #if initcursor == False:
            #initcursor = None
        #cursor = self.textCursor() if initcursor is None else initcursor
        #beg = cursor.selectionStart()
        #end = cursor.selectionEnd()
        #pos = cursor.position()
        #if not initcursor : cursor.beginEditBlock()
        #cursor.setPosition(beg,QtGui.QTextCursor.MoveAnchor)
        #cursor.movePosition(QtGui.QTextCursor.StartOfBlock,QtGui.QTextCursor.MoveAnchor)
        #while cursor.position() <= end :
            #if self.replaceTab:
                #cursor.insertText(self.indentation)
                #end+=len(self.indentation)
            #else:
                #cursor.insertText('\t')
                #end+=1
            #oldpos = cursor.position()
            #cursor.movePosition(QtGui.QTextCursor.NextBlock,QtGui.QTextCursor.MoveAnchor)
            #if cursor.position() == oldpos:
                #break
        #if not initcursor : cursor.endEditBlock()
        #cursor.setPosition(pos,QtGui.QTextCursor.MoveAnchor)
    #def untab(self):
        #cursor = self.textCursor()
        #beg = cursor.selectionStart()
        #end = cursor.selectionEnd()
        #pos = cursor.position()
        #cursor.beginEditBlock()
        #cursor.setPosition(beg,QtGui.QTextCursor.MoveAnchor)
        #cursor.movePosition(QtGui.QTextCursor.StartOfBlock,QtGui.QTextCursor.MoveAnchor)
        #while cursor.position() <= end:
            #cursor.movePosition(QtGui.QTextCursor.NextCharacter,QtGui.QTextCursor.KeepAnchor)
            #if cursor.selectedText() == '\t':
                #cursor.deleteChar()
            #else:
                #for i in xrange(len(self.indentation)-1):
                    #b = cursor.movePosition(QtGui.QTextCursor.NextCharacter,QtGui.QTextCursor.KeepAnchor)
                    #if not b : break
                #if cursor.selectedText() == self.indentation:
                    #cursor.removeSelectedText()                    
            #end-=1
            #cursor.movePosition(QtGui.QTextCursor.Down,QtGui.QTextCursor.MoveAnchor)
            #cursor.movePosition(QtGui.QTextCursor.StartOfBlock,QtGui.QTextCursor.MoveAnchor)
        #cursor.endEditBlock()
        #cursor.setPosition(pos,QtGui.QTextCursor.MoveAnchor)
        
    ####################################################################
    #### (Un)Comment (cf lpycodeeditor)
    ####################################################################
    def comment(self):
        cursor = self.textCursor()
        beg = cursor.selectionStart()
        end = cursor.selectionEnd()
        pos = cursor.position()
        cursor.beginEditBlock() 
        cursor.setPosition(beg,QtGui.QTextCursor.MoveAnchor)
        cursor.movePosition(QtGui.QTextCursor.StartOfBlock,QtGui.QTextCursor.MoveAnchor)
        while cursor.position() <= end:
            cursor.insertText('#')
            oldpos = cursor.position()
            cursor.movePosition(QtGui.QTextCursor.NextBlock,QtGui.QTextCursor.MoveAnchor)
            if cursor.position() == oldpos:
                break
            end+=1
        cursor.endEditBlock()
        cursor.setPosition(pos,QtGui.QTextCursor.MoveAnchor)
    def uncomment(self):
        cursor = self.textCursor()
        beg = cursor.selectionStart()
        end = cursor.selectionEnd()
        pos = cursor.position()
        cursor.beginEditBlock()
        cursor.setPosition(beg,QtGui.QTextCursor.MoveAnchor)
        cursor.movePosition(QtGui.QTextCursor.StartOfBlock,QtGui.QTextCursor.MoveAnchor)
        while cursor.position() <= end:
            cursor.movePosition(QtGui.QTextCursor.NextCharacter,QtGui.QTextCursor.KeepAnchor)
            if True:
                if cursor.selectedText() == '#':
                        cursor.deleteChar()
                        cursor.movePosition(QtGui.QTextCursor.NextBlock,QtGui.QTextCursor.MoveAnchor)
                end-=1
        cursor.endEditBlock()
        cursor.setPosition(pos,QtGui.QTextCursor.MoveAnchor)

    ####################################################################
    #### Completer
    ####################################################################
    def setCompleter(self, completer):
        logger.debug("set completer " + str(completer))
        if self.completer:
            self.disconnect(self.completer, 0, self, 0)
        if not completer:
            return
        
        completer.setWidget(self)
        completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer = completer
        logger.debug("selfcompleter " + str(self.completer))
        QtCore.QObject.connect(self.completer, QtCore.SIGNAL("activated(const QString&)"),self.insertCompletion)
        logger.debug("completer connected")

    def insertCompletion(self, completion):
        logger.debug("insert completion")
        tc = self.textCursor()
        extra = (len(completion) -
            len(self.completer.completionPrefix()))
        tc.movePosition(QtGui.QTextCursor.Left)
        tc.movePosition(QtGui.QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)
        logger.debug("inserted completion")

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        QtGui.QTextEdit.focusInEvent(self, event)
        
#http://web.njit.edu/all_topics/Prog_Lang_Docs/html/qt/qtextbrowser.html
#http://qt.developpez.com/doc/3.3/qtextbrowser/

# keep in mind QTextBrowser to embed notebook !!!!
# cmd = "ipython notebook"
# http://127.0.0.1:8888/
        
