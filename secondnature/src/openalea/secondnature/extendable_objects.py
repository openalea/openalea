# -*- python -*-
#
#       OpenAlea.SecondNature
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



from PyQt4 import QtCore
from openalea.secondnature.managers import DocumentManager

class Base(object):
    def __init__(self, name, ns):
        self._name = name
        self.__ns = ns

    name      = property(lambda x: x._name)
    namespace = property(lambda x: x.__ns)
    fullname  = property(lambda x: ".".join([x.__ns, x._name]))



class Layout(Base):
    def __init__(self, name, ns, skeleton, appletmap, easy_name=None):
        Base.__init__(self, name, ns)
        self.__skeleton  = skeleton
        self.__appletmap = appletmap
        self.__ezname    = easy_name

    skeleton  = property(lambda x: x.__skeleton)
    appletmap = property(lambda x: x.__appletmap)
    easyname  = property(lambda x: x.__ezname or x.fullname)



class LayoutSpace(Base):
    """returned by widget factories"""
    def __init__(self, name, ns, content, menuList=None, toolbar=None):
        Base.__init__(self, name, ns)
        self.__content = content
        self.__menuList    = menuList
        self.__toolbar = toolbar

    content = property(lambda x:x.__content)
    menus   = property(lambda x:x.__menuList)
    toolbar = property(lambda x:x.__toolbar)


class AppletFactory(Base):
    __name__ = ""
    __namespace__ = ""
    __mimeformats__ = []
    __supports_open__ = True
    __dm = None

    def __init__(self):
        Base.__init__(self, self.__name__, self.__namespace__)
        if AppletFactory.__dm is None:
            AppletFactory.__dm = DocumentManager()

    def get_mime_formats(self):
        return self.__mimeformats__[:]

    def supports_document_open(self):
        return self.__supports_open__

    def get_icon(self):
        return NotImplementedError

    def new_document(self):
        raise NotImplementedError

    def open_document(self, parsedUrl):
        raise NotImplementedError(self.__class__.__name__+" doesn't support document opening")

    def get_applet_space(self, document):
        raise NotImplementedError

    def new_document_and_register_it(self):
        document = self.new_document()
        if document and document.registerable:
            self.__dm.add_document(document)
        return document

    def open_document_and_register_it(self, parsedUrl):
        document = self.open_document(parsedUrl)
        if document and document.registerable:
            self.__dm.add_document(document)
        return document

    def get_applet_space_and_register_it(self, document=None):
        document = document or self.new_document_and_register_it()
        space = self.get_applet_space(document)
        if self.__dm.has_document(document) and space:
            self.__dm.set_document_property(document, "space", space)
        return space

    __call__ = get_applet_space_and_register_it



class Document(Base):
    """"""
    def __init__(self, name, ns, source, obj, **kwargs):
        Base.__init__(self, name, ns)
        self.__source = source
        self.__obj    = obj
        self._reg    = True
        self._props  = kwargs.copy()

    source       = property(lambda x:x.__source)
    obj          = property(lambda x:x.__obj)
    registerable = property(lambda x:x._reg)

    def _set_name(self, name):
        self._name = name

    def save(self):
        raise NotImplementedError

    def get_inner_property(self, key):
        return self._props.get(key)

class UnregisterableDocument(Document):
    def __init__(self, name, ns, source, obj):
        Document.__init__(self, name, ns, source, obj)
        self._reg = False

