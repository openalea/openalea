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
This module implements a QT4 python interpreter widget.
It is inspired bu PyCute : http://gerard.vermeulen.free.fr
"""

__license__= "CeCILL V2"
__revision__=" $Id$"


import os, sys
from PyQt4 import QtCore, QtGui, Qsci


from QSci import QsciScintilla, QsciLexerPython

class SciShell(QsciScintilla):

    """
    SciShell is a Python shell based in QScintilla.
    """
    
    def __init__(self, interpreter, message="", log='', parent=None):
        """Constructor.
        @param interpreter : InteractiveInterpreter in which
        the code will be executed

        @param message : welcome message string
        
        @param  'parent' : specifies the parent widget.
        If no parent widget has been specified, it is possible to
        exit the interpreter by Ctrl-D.
        """

        QsciScintilla.__init__(self, parent)
        self.interpreter = interpreter

        # user interface setup
        self.setAutoIndent(True)
        self.setAutoCompletionThreshold(-1)
        self.setAutoCompletionSource(QsciScintilla.AcsDocument)
        # Lexer
        self.setLexer(QsciLexerPython(self))


        # # capture all interactive input/output 
        sys.stdout   = self
        sys.stderr   = MultipleRedirection((sys.stderr, self))
        sys.stdin    = self

        
        # last line + last incomplete lines
        self.line    = QtCore.QString()
        self.__lines   = []
        # the cursor position in the last line
        self.point   = 0
        # flag: the interpreter needs more input to run the last lines. 
        self.more    = 0
        # flag: readline() is being used for e.g. raw_input() and input()
        self.reading = 0
        # history
        self.history = []
        self.pointer = 0
        self.cursor_pos   = 0


        # interpreter prompt.
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "

        # interpreter banner
        self.write('The shell running Python %s on %s.\n' %
                   (sys.version, sys.platform))
        self.write('Type "copyright", "credits" or "license"'
                   ' for more information on Python.\n')
        self.write(message+'\n\n')
        self.write(sys.ps1)


        ##

        self.supportedEditorCommands = {
            #QsciScintilla.SCI_LINEDELETE   : self.__clearCurrentLine,
            QsciScintilla.SCI_TAB          : self.__QScintillaTab,
            QsciScintilla.SCI_NEWLINE      : self.__QScintillaNewline,
            
            QsciScintilla.SCI_DELETEBACK   : self.__QScintillaDeleteBack,
            QsciScintilla.SCI_CLEAR        : self.__QScintillaDelete,
            QsciScintilla.SCI_DELWORDLEFT  : self.__QScintillaDeleteWordLeft,
            QsciScintilla.SCI_DELWORDRIGHT : self.__QScintillaDeleteWordRight,
            QsciScintilla.SCI_DELLINELEFT  : self.__QScintillaDeleteLineLeft,
            QsciScintilla.SCI_DELLINERIGHT : self.__QScintillaDeleteLineRight,
            
            QsciScintilla.SCI_CHARLEFT     : self.__QScintillaCharLeft,
            QsciScintilla.SCI_CHARRIGHT    : self.__QScintillaCharRight,
            QsciScintilla.SCI_WORDLEFT     : self.__QScintillaWordLeft,
            QsciScintilla.SCI_WORDRIGHT    : self.__QScintillaWordRight,
            QsciScintilla.SCI_VCHOME       : self.__QScintillaVCHome,
            QsciScintilla.SCI_LINEEND      : self.__QScintillaLineEnd,
            QsciScintilla.SCI_LINEUP       : self.__QScintillaLineUp,
            QsciScintilla.SCI_LINEDOWN     : self.__QScintillaLineDown,
            
            #QsciScintilla.SCI_PAGEUP       : self.__QScintillaAutoCompletionCommand,
            #QsciScintilla.SCI_PAGEDOWN     : self.__QScintillaAutoCompletionCommand,
            #QsciScintilla.SCI_CANCEL       : self.__QScintillaAutoCompletionCommand,
            
            #QsciScintilla.SCI_CHARLEFTEXTEND  : self.__QScintillaCharLeftExtend,
            #QsciScintilla.SCI_CHARRIGHTEXTEND : self.extendSelectionRight,
            #QsciScintilla.SCI_WORDLEFTEXTEND  : self.__QScintillaWordLeftExtend,
            #QsciScintilla.SCI_WORDRIGHTEXTEND : self.extendSelectionWordRight,
            #QsciScintilla.SCI_VCHOMEEXTEND    : self.__QScintillaVCHomeExtend,
            #QsciScintilla.SCI_LINEENDEXTEND   : self.extendSelectionToEOL,
        }
        

    def get_interpreter(self):
        """ Return the interpreter object """

        return self.interpreter
        

    def moveCursor(self, operation, mode=QTextCursor.MoveAnchor):
        """
        Convenience function to move the cursor
        This function will be present in PyQT4.2
        """
        cursor = self.textCursor()
        cursor.movePosition(operation, mode)
        self.setTextCursor(cursor)
        

    def flush(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        pass


    def isatty(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        return 1
    

    def readline(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        self.reading = 1
        self.__clearLine()
        self.moveCursor(QTextCursor.End)
        while self.reading:
            qApp.processOneEvent()
        if self.line.length() == 0:
            return '\n'
        else:
            return str(self.line) 


    def __getEndPos(self):
        """
        Private method to return the line and column of the last character.
        @return tuple of two values (int, int) giving the line and column
        """
        line = self.lines() - 1
        return (line, self.lineLength(line))


    def write(self, s):
        """
        Simulate stdin, stdout, and stderr.
        """

        line, col = self.__getEndPos()
        self.setCursorPosition(line, col)
        self.insert(s)
        self.prline, self.prcol = self.getCursorPosition()
        self.ensureCursorVisible()
        self.ensureLineVisible(line)


    def writelines(self, text):
        """
        Simulate stdin, stdout, and stderr.
        """
        map(self.write, text)


    def fakeUser(self, lines):
        """
        Simulate a user: lines is a sequence of strings, (Python statements).
        """
        for line in lines:
            self.line = QtCore.QString(line.rstrip())
            self.write(self.line)
            self.write('\n')
            self.__run()

            
    def __run(self):
        """
        Append the last line to the history list, let the interpreter execute
        the last line(s), and clean up accounting for the interpreter results:
        (1) the interpreter succeeds
        (2) the interpreter fails, finds no errors and wants more line(s)
        (3) the interpreter fails, finds errors and writes them to sys.stderr
        """
        self.pointer = 0
        self.history.append(QtCore.QString(self.line))
        try:
            self.__lines.append(str(self.line))
        except Exception,e:
            print e

        source = '\n'.join(self.__lines)
        self.more = self.interpreter.runsource(source)

        if self.more:
            self.write(sys.ps2)
        else:
            self.write(sys.ps1)
            self.__lines = []
        self.__clearLine()

        
    def __clearLine(self):
        """
        Clear input line buffer
        """
        self.line.truncate(0)
        self.point = 0


    ###########################################
    def __executeLines(self, lines):
        """
        Private method to execute a set of lines as multiple commands.
        
        @param lines multiple lines of text to be executed as single
            commands (string)
        """
        for line in lines.splitlines(True):
            if line.endswith("\r\n"):
                fullline = True
                cmd = line[:-2]
            elif line.endswith("\r") or line.endswith("\n"):
                fullline = True
                cmd = line[:-1]
            else:
                fullline = False
            
            self.__insertTextAtEnd(line)
            if fullline:
                self.__executeCommand(cmd)
                if self.interruptCommandExecution: 
                    self.__executeCommand("")
                    break

                
    def __executeCommand(self, cmd):
        """
        Private slot to execute a command.
        
        @param cmd command to be executed by debug client (string)
        """
        if not self.inRawMode:
            self.inCommandExecution = True
            self.interruptCommandExecution = False
            if not cmd:
                cmd = ''
            else:
                if len(self.history) == self.maxHistoryEntries:
                    del self.history[0]
                self.history.append(QString(cmd))
                self.histidx = -1
            if cmd.startswith('start'):
                if not self.passive:
                    cmdList = cmd.split(None, 1)
                    if len(cmdList) < 2:
                        self.dbs.startClient(False) # same as reset
                    else:
                        language = cmdList[1]
                        if not language in self.clientLanguages:
                            language = cmdList[1].capitalize()
                            if not language in self.clientLanguages:
                                language = ""
                        if language:
                            self.dbs.startClient(False, language)
                        else:
                            # language not supported or typo
                            self.__write(\
                                self.trUtf8('Shell language "%1" not supported.\n')\
                                    .arg(cmdList[1]))
                            self.__clientStatement(False)
                        return
                    cmd = ''
            elif cmd == 'languages':
                s = '%s\n' % ', '.join(self.clientLanguages)
                self.__write(s)
                self.__clientStatement(False)
                return
            elif cmd == 'clear':
                # Display the banner.
                self.__getBanner()
                if not self.passive:
                    return
                else:
                    cmd = ''
            elif cmd == 'reset':
                self.dbs.startClient(False)
                if self.passive:
                    return
                else:
                    cmd = ''
            
            self.dbs.remoteStatement(cmd)
            while self.inCommandExecution: QApplication.processEvents()
        else:
            if not self.echoInput:
                cmd = unicode(self.buff)
            self.inRawMode = False
            self.echoInput = True
            if not cmd:
                cmd = ''
            else:
                cmd = str(cmd.replace(unicode(self.prompt), ""))
            self.dbs.remoteRawInput(cmd)

    
    def __insertText(self, text):
        """
        Insert text at the current cursor position.
        """

        line, col = self.getCursorPosition()
        self.insertAt(s, line, col)
        self.setCursorPosition(line, col + len(str(s)))


    def __insertTextAtEnd(self, s):
        """
        Private method to insert some text at the end of the command line.
        @param s text to be inserted (string or QString)
        """
        line, col = self.__getEndPos()
        self.setCursorPosition(line, col)
        self.insert(s)
        self.prline, self.prcol = self.getCursorPosition()


    def __isCursorOnLastLine(self):
        """
        Private method to check, if the cursor is on the last line.
        """
        cline, ccol = self.getCursorPosition()
        return cline == self.lines() - 1    


    def keyPressEvent(self, ev):
        """
        Re-implemented to handle the user input a key at a time.
        
        @param ev key event (QKeyEvent)
        """
        txt = ev.text()
        key = ev.key()
        
        # See it is text to insert.
        if self.__isCursorOnLastLine() and txt.length():
            QsciScintilla.keyPressEvent(self, ev)
        else:
            ev.ignore()


    def __QScintillaTab(self, cmd):
        """
        Private method to handle the Tab key.
        
        @param cmd QScintilla command
        """
        if self.isListActive():
            self.SendScintilla(cmd)
        elif self.__isCursorOnLastLine():
            line, index = self.getCursorPosition()
            buf = unicode(self.text(line)).replace(sys.ps1, "").replace(sys.ps2, "")
            if self.inContinue and not buf[:index-len(sys.ps2)].strip():
                self.SendScintilla(cmd)
            elif self.racEnabled:
                self.dbs.remoteCompletion(buf)
                
        
    def __QScintillaLeftDeleteCommand(self, method):
        """
        Private method to handle a QScintilla delete command working to the left.
        
        @param method shell method to execute
        """
        if self.__isCursorOnLastLine():
            line, col = self.getCursorPosition()
            db = 0
            ac = self.isListActive()
            oldLength = self.text(line).length()
            
            if self.text(line).startsWith(sys.ps1):
                if col > len(sys.ps1):
                    method()
                    db = 1
            elif self.text(line).startsWith(sys.ps2):
                if col > len(sys.ps2):
                    method()
                    db = 1
            elif col > 0:
                method()
                db = 1
            if db and ac and self.racEnabled and self.completionText:
                delta = self.text(line).length() - oldLength
                self.dbs.remoteCompletion(self.completionText[:delta])
        
    def __QScintillaDeleteBack(self):
        """
        Private method to handle the Backspace key.
        """
        self.__QScintillaLeftDeleteCommand(self.deleteBack)
        
    def __QScintillaDeleteWordLeft(self):
        """
        Private method to handle the Delete Word Left command.
        """
        self.__QScintillaLeftDeleteCommand(self.deleteWordLeft)
        
    def __QScintillaDelete(self):
        """
        Private method to handle the delete command.
        """
        if self.__isCursorOnLastLine():
            if self.hasSelectedText():
                lineFrom, indexFrom, lineTo, indexTo = self.getSelection()
                if self.text(lineFrom).startsWith(sys.ps1):
                    if indexFrom >= len(sys.ps1):
                        self.delete()
                elif self.text(lineFrom).startsWith(sys.ps2):
                    if indexFrom >= len(sys.ps2):
                        self.delete()
                elif indexFrom >= 0:
                    self.delete()
                self.setSelection(lineTo, indexTo, lineTo, indexTo)
            else:
                self.delete()
        
    def __QScintillaDeleteLineLeft(self):
        """
        Private method to handle the Delete Line Left command.
        """
        if self.__isCursorOnLastLine():
            if self.isListActive():
                self.cancelList()
            
            line, col = self.getCursorPosition()
            if self.text(line).startsWith(sys.ps1):
                prompt = sys.ps1
            elif self.text(line).startsWith(sys.ps2):
                prompt = sys.ps2
            else:
                prompt = ""
            
            self.deleteLineLeft()
            self.insertAt(prompt, line, 0)
            self.setCursorPosition(line, len(prompt))
        
    def __QScintillaNewline(self, cmd):
        """
        Private method to handle the Return key.
        
        @param cmd QScintilla command
        """
        if self.__isCursorOnLastLine():
            if self.isListActive():
                self.SendScintilla(cmd)
            else:
                self.incrementalSearchString = ""
                self.incrementalSearchActive = False
                line, col = self.__getEndPos()
                self.setCursorPosition(line,col)
                buf = unicode(self.text(line)).replace(sys.ps1, "").replace(sys.ps2, "")
                self.insert('\n')
                self.__executeCommand(buf)
        
    def __QScintillaLeftCommand(self, method, allLinesAllowed = False):
        """
        Private method to handle a QScintilla command working to the left.
        
        @param method shell method to execute
        """
        if self.__isCursorOnLastLine() or allLinesAllowed:
            line, col = self.getCursorPosition()
            if self.text(line).startsWith(sys.ps1):
                if col > len(sys.ps1):
                    method()
            elif self.text(line).startsWith(sys.ps2):
                if col > len(sys.ps2):
                    method()
            elif col > 0:
                method()
        
    def __QScintillaCharLeft(self):
        """
        Private method to handle the Cursor Left command.
        """
        self.__QScintillaLeftCommand(self.moveCursorLeft)
        
    def __QScintillaWordLeft(self):
        """
        Private method to handle the Cursor Word Left command.
        """
        self.__QScintillaLeftCommand(self.moveCursorWordLeft)
        
    def __QScintillaRightCommand(self, method):
        """
        Private method to handle a QScintilla command working to the right.
        
        @param method shell method to execute
        """
        if self.__isCursorOnLastLine():
            method()
        
    def __QScintillaCharRight(self):
        """
        Private method to handle the Cursor Right command.
        """
        self.__QScintillaRightCommand(self.moveCursorRight)
        
    def __QScintillaWordRight(self):
        """
        Private method to handle the Cursor Word Right command.
        """
        self.__QScintillaRightCommand(self.moveCursorWordRight)
        
    def __QScintillaDeleteWordRight(self):
        """
        Private method to handle the Delete Word Right command.
        """
        self.__QScintillaRightCommand(self.deleteWordRight)
        
    def __QScintillaDeleteLineRight(self):
        """
        Private method to handle the Delete Line Right command.
        """
        self.__QScintillaRightCommand(self.deleteLineRight)
        
    def __QScintillaVCHome(self, cmd):
        """
        Private method to handle the Home key.
        
        @param cmd QScintilla command
        """
        if self.isListActive():
            self.SendScintilla(cmd)
        elif self.__isCursorOnLastLine():
            line, col = self.getCursorPosition()
            if self.text(line).startsWith(sys.ps1):
                col = len(sys.ps1)
            elif self.text(line).startsWith(sys.ps2):
                col = len(sys.ps2)
            else:
                col = 0
            self.setCursorPosition(line, col)
        
    def __QScintillaLineEnd(self, cmd):
        """
        Private method to handle the End key.
        
        @param cmd QScintilla command
        """
        if self.isListActive():
            self.SendScintilla(cmd)
        elif self.__isCursorOnLastLine():
            self.moveCursorToEOL()
        
    def __QScintillaLineUp(self, cmd):
        """
        Private method to handle the Up key.
        
        @param cmd QScintilla command
        """
        if self.isListActive():
            self.SendScintilla(cmd)
        else:
            line, col = self.__getEndPos()
            buf = unicode(self.text(line)).replace(sys.ps1, "").replace(sys.ps2, "")
            if buf and self.incrementalSearchActive:
                if self.incrementalSearchString:
                    idx = self.__rsearchHistory(self.incrementalSearchString, 
                                                self.histidx)
                    if idx >= 0:
                        self.histidx = idx
                        self.__useHistory()
                else:
                    idx = self.__rsearchHistory(buf)
                    if idx >= 0:
                        self.histidx = idx
                        self.incrementalSearchString = buf
                        self.__useHistory()
            else:
                if self.histidx < 0:
                    self.histidx = len(self.history)
                if self.histidx > 0:
                    self.histidx = self.histidx - 1
                    self.__useHistory()
        
    def __QScintillaLineDown(self, cmd):
        """
        Private method to handle the Down key.
        
        @param cmd QScintilla command
        """
        if self.isListActive():
            self.SendScintilla(cmd)
        else:
            line, col = self.__getEndPos()
            buf = unicode(self.text(line)).replace(sys.ps1, "").replace(sys.ps2, "")
            if buf and self.incrementalSearchActive:
                if self.incrementalSearchString:
                    idx = self.__searchHistory(self.incrementalSearchString, self.histidx)
                    if idx >= 0:
                        self.histidx = idx
                        self.__useHistory()
                else:
                    idx = self.__searchHistory(buf)
                    if idx >= 0:
                        self.histidx = idx
                        self.incrementalSearchString = buf
                        self.__useHistory()
            else:
                if self.histidx >= 0 and self.histidx < len(self.history):
                    self.histidx += 1
                    self.__useHistory()
          



        
            


    




