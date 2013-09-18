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

class DictionaryCompleter(QtGui.QCompleter):
    def __init__(self, parent=None):
        words = []
        try:
            f = open("/usr/share/dict/words","r")
            for word in f:
                words.append(word.strip())
            f.close()
        except IOError:
            print "dictionary not in anticipated location"
        QtGui.QCompleter.__init__(self, words, parent)
