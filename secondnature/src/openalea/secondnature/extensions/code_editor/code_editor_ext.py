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

from openalea.core.node import NodeFactory
from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.pkgmanager import PackageManager
from openalea.secondnature.extendable_objects import *
from openalea.visualea.scintilla_editor import ScintillaCodeEditor
import urllib2
import urlparse
import os.path as path
import inspect

class CodeEditorFactory(DocumentWidgetFactory):
    __name__        = "CodeEditor"
    __namespace__   = "CodeEditor"
    __mimeformats__ = ["text/plain", 
                       "application/x-qt-windows-mime;value=\"FileName\"",
                       NodeFactory.mimetype, 
                       CompositeNodeFactory.mimetype]

    def __init__(self):
        WidgetFactory.__init__(self)
        self.__ctr = 0
        self.pm = PackageManager()

    def new_document(self):
        text = ""
        name = "New code " + str(self.__ctr)
        self.__ctr += 1
        parsedUrl = urlparse.ParseResult(scheme="file",
                                         netloc="",
                                         path="unknown/"+name,
                                         params="",
                                         query="",
                                         fragment=""
                                         )
        document = Document(name, "CodeEditor", parsedUrl.geturl(), "")
        return document

    def open_document(self, parsedUrl):
        url = parsedUrl.geturl()
        if parsedUrl.scheme == "oa":
            fac = self.pm.get_factory_from_url(parsedUrl)
            if isinstance(fac, CompositeNodeFactory):
                pkg  = self.pm.get_package_from_url(parsedUrl)[0]
                name = pkg.get_wralea_path()
            else:
                mod_name = fac.get_node_module()
                name =  inspect.getsourcefile(mod_name)
            f = open(name)
        elif parsedUrl.scheme == "file":
            name = parsedUrl.path.strip("/")
            f = open(name)
        else:
            f = urllib2.urlopen(url)
            name = parsedUrl.path
        text = f.read()
        f.close()
        document = Document(name, "CodeEditor", url, text)
        return document

    def get_document_space(self, document):
        widget = ScintillaCodeEditor()
        widget.setText(document.obj)
        return LayoutSpace(self.__name__, self.__namespace__, widget)


# -- instantiate widget factories --
editor_f = CodeEditorFactory()
