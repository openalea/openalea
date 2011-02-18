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

class CodeEditorFactory(WidgetFactory):
    __name__ = "CodeEditor"
    __namespace__ = "CodeEditor"

    __supported_schemes__ = {"file", "http"}#, "oa"}
    __supported_extensions__ = {".txt", ".py", ".lpy"}

    def __init__(self):
        WidgetFactory.__init__(self)
        self.__ctr = 0

    def _instanciate_space(self, url):
        text = None
        if url is None:
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
        else:
            assert self.handles(url)
            f = urllib2.urlopen(url.geturl())
            text = f.read()
            name = url.path

        widget   = ScintillaCodeEditor()
        widget.setText(text)
        res = widget.document()
        document = Document(name, "CodeEditor", url.geturl(), res)
        return document, LayoutSpace(self.__name__, self.__namespace__, widget)

    def handles(self, url):
        good = False
        print "CodeEditorFactory handles scheme", url.scheme, self.__supported_schemes__
        if url.scheme in self.__supported_schemes__:
        # if url.scheme == "oa":
            # queries = urlparse.parse_qs(url.query)
            # if "ft" not in queries or "DataFactory" not in queries["ft"]:
            #     good = False
            ext = path.splitext(url.path)[1]
            print "CodeEditorFactory handles ext", ext, self.__supported_extensions__
            if ext in self.__supported_extensions__:
                good = True
        return good



# -- instantiate widget factories --
editor_f = CodeEditorFactory()
