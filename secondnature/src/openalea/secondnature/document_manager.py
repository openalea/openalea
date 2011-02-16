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
from openalea.core.metaclass import make_metaclass
from openalea.core.singleton import ProxySingleton


class Document(object):
    """"""
    def __init__(self, url, obj):
        self.__url    = url
        self.__obj    = obj

    def simple_name(self):
        return None

    url    = property(lambda x:x.__url)
    obj    = property(lambda x:x.__obj)


class DocumentManager(QtCore.QObject):

    __metaclass__ = make_metaclass((ProxySingleton,),
                                   (QtCore.pyqtWrapperType,))

    documentAdded = QtCore.pyqtSignal(object, object)
    documentDeleted = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.__docprops = {}

    def add_document(self, doc):
        if doc.url in self.__docprops or \
           (doc.simple_name is not None and doc.simple_name in self.__docprops) :
            return

        self.__docprops.setdefault(doc.url, {})["document"] = doc
        sname = doc.simple_name()
        if sname:
            self.__docprops.setdefault(sname, {})["document"] = doc
        self.documentAdded.emit(iden, doc)

    def set_document_property(self, iden, key, val):
        if iden not in self.__docprops:
            return None

        self.__docprops[iden][key] = val

    def get_document_property(self, iden, key):
        if iden not in self.__docprops:
            return None
        return self.__docprops[iden].get(key)

    def pop_document_property(self, iden, key):
        if iden not in self.__docprops:
            return None
        return self.__docprops[iden].pop(key)

    def get_document(self, iden):
        return self.__docprops[iden]["document"]

    def del_document(self, iden):
        if url not in self.__docprops:
            return

        del self.__docprops[iden]
        self.documentDeleted.emit(iden)

    def document_names(self):
        return set(self.__docprops.iterkeys())

