# -*- python -*-
#
#       OpenAlea.Secondnature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "CeCILL v2"
__revision__ = " $Id$ "

from openalea.secondnature.extendable_objects import *
from openalea.visualea.scintilla_editor import ScintillaCodeEditor
import urllib2
import urlparse
import os.path as path

class CodeEditorFactory(DocumentWidgetFactory):
    __name__ = "CodeEditor"
    __namespace__ = "CodeEditor"
    __mimeformats__ = ["text/plain"]

    def __init__(self):
        WidgetFactory.__init__(self)
        self.__ctr = 0

    def new_document(self):
        text = ""
        name = "New code " + str(self.__ctr)
        self.__ctr += 1
        url = urlparse.ParseResult(scheme="file",
                                   netloc="",
                                   path="unknown/"+name,
                                   params="",
                                   query="",
                                   fragment=""
                                   )
        document = Document(name, "CodeEditor", url.geturl(), "")
        return document

    def open_document(self, parsedUrl):
        url = parsedUrl.geturl()
        f = urllib2.urlopen(url)
        text = f.read()
        name = parsedUrl.path
        f.close()
        document = Document(name, "CodeEditor", url, text)
        return document

    def get_document_space(self, document):
        widget = ScintillaCodeEditor()
        widget.setText(document.obj)
        return LayoutSpace(self.__name__, self.__namespace__, widget)


# -- instantiate widget factories --
editor_f = CodeEditorFactory()
