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

from openalea.vpltk.qt import QtGui
import keyword
import __builtin__

class DictionaryCompleter(QtGui.QCompleter):
    def __init__(self, parent=None):
        super(DictionaryCompleter, self).__init__(parent)
        self.basic_words = keyword.kwlist + __builtin__.__dict__.keys()
        
        self.update_dict()
        
    def update_dict(self):
        """
        Use it to add new words from locals() and globals()
        """
        words = self.basic_words + locals().keys() + globals().keys()
        QtGui.QCompleter.__init__(self, words, self.parent())
        
    def add_words(self, words):
        """
        Add a list of words into dict
        """
        words = list(words)
        self.words = self.words + words
        self.update_dict()
