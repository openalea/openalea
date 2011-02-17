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
from openalea.core.logger import get_logger


logger = get_logger(__name__)

def init_sources():
    init_extension_sources()
    init_widgetfactory_sources()
    init_layout_sources()
    init_document_sources()
    LayoutManager().gather_items(refresh=True)
    WidgetFactoryManager().gather_items(refresh=True)
    ExtensionManager().gather_items(refresh=True)
    DocumentManager().gather_items(refresh=True)





class AbstractSourceManager(QtCore.QObject):

    __metaclass__ = make_metaclass((ProxySingleton,),
                                   (QtCore.pyqtWrapperType,))

    itemListChanged = QtCore.pyqtSignal(list)

    def __init__(self):
        QtCore.QObject.__init__(self)
        self._sources = {}
        self._items   = {}

    def __iter__(self):
        return self._items.iteritems()

    def _add_source(self, src):
        if src.name in self._sources:
            return #TODO : raise something dude
        src.itemListChanged.connect(self.update_with_source)
        self._sources[src.name] = src

    def iter_sources(self):
        return self._sources.itervalues()

    def gather_items(self, refresh=False):
        if refresh:
            self._items = {}
            for src in self.iter_sources():
                if not src.is_valid():
                    continue
                src.gather_items()
                self._items.update(src.get_items())
            self.itemListChanged.emit(list(self.iter_item_names()))
        return self._items

    def get(self, name):
        items = self.gather_items()
        return items.get(name, None)

    def iter_item_names(self):
        return self.gather_items().iterkeys()

    def update_with_source(self, src, items):
        self._items.update(items)
        self.itemListChanged.emit(list(self.iter_item_names()))





class AbstractSource(QtCore.QObject):

    __metaclass__ = make_metaclass((ProxySingleton,),
                                   (QtCore.pyqtWrapperType,))

    __concrete_manager__ = None


    itemListChanged = QtCore.pyqtSignal(object, dict)

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.__name = self.__class__.__name__

        mgrCls = self.__concrete_manager__
        if mgrCls is not None:
            mgrCls()._add_source(self)

    name = property( lambda x:x.__name )

    def is_valid(self):
        raise NotImplementedError

    def gather_items(self):
        raise NotImplementedError

    def get_items(self):
        raise NotImplementedError





class EntryPointSourceBase(AbstractSource):

    __entry_point__ = None

    def __init__(self):
        AbstractSource.__init__(self)
        try:
            import pkg_resources
        except ImportError:
            logger.error("Setuptools' pkg_resources not available. No entry point extensions.")
            self.pkg_resources = None
        else:
            self.pkg_resources = pkg_resources
        self.__items = None

    def is_valid(self):
        return self.pkg_resources is not None

    def gather_items(self):
        if not self.is_valid():
            return None #TODO : raise something dude
        if self.__entry_point__ is None:
            return None #TODO : raise something dude

        self.items = {}
        for ep in self.pkg_resources.iter_entry_points(self.__entry_point__):
            try:
                it = ep.load()
            except ImportError, e:
                logger.error(self.name + " couldn't load " + str(ep) )
            else:
                self.items[it.fullname] = it
        self.itemListChanged.emit(self, self.items.copy())

    def get_items(self):
        return self.items.copy()



class BuiltinSourceBase(AbstractSource):

    __mod_name__ = None

    def __init__(self):
        AbstractSource.__init__(self)
        name = ".".join(["builtins",self.__mod_name__])
        try:
            self.mod = __import__(name,
                                  fromlist=[self.__mod_name__])
        except ImportError, e:
            logger.error("Couldn't import " + name)
            self.mod = None
        self.__items = None

    def is_valid(self):
        return self.mod is not None

    def gather_items(self):
        if not self.is_valid():
            return None #TODO : raise something dude
        itemlist = self.mod.get_builtins()
        self.__items = dict( (v.fullname, v) for v in itemlist)
        self.itemListChanged.emit(self, self.__items.copy())

    def get_items(self):
        return self.__items.copy()





##########################
# LAYOUT MANAGER CLASSES #
##########################
class LayoutManager(AbstractSourceManager):
    pass

class LayoutSourceMixin(object):
    __concrete_manager__ = LayoutManager

class LayoutSourceEntryPoints(LayoutSourceMixin, EntryPointSourceBase):

    __entry_point__ = "openalea.app.layout"

    def __init__(self):
        LayoutSourceMixin.__init__(self)
        EntryPointSourceBase.__init__(self)

def init_layout_sources():
    LayoutSourceEntryPoints()







#################################
# WIDGETFACTORY MANAGER CLASSES #
#################################
class WidgetFactoryManager(AbstractSourceManager):
    def has_handler_for(self, input):
        if input is not None:
            factories = self.gather_items()
            for it in factories.itervalues():
                if it.handles(input):
                    return it
        return None


    def create_space(self, name=None, input=None, parent=None):
        factories = self.gather_items()
        factory   = factories.get(name)
        factory   = factory or self.has_handler_for(input)
        if factory is not None:
            return factory(input, parent)
        return None, None


class WidgetFactorySourceMixin(object):
    __concrete_manager__ = WidgetFactoryManager

class WidgetFactorySourceBuiltin(WidgetFactorySourceMixin, BuiltinSourceBase):

    __mod_name__ = "widget_factories"

    def __init__(self):
        WidgetFactorySourceMixin.__init__(self)
        BuiltinSourceBase.__init__(self)

class WidgetFactorySourceEntryPoints(WidgetFactorySourceMixin, EntryPointSourceBase):

    __entry_point__ = "openalea.app.widget_factory"

    def __init__(self):
        WidgetFactorySourceMixin.__init__(self)
        EntryPointSourceBase.__init__(self)

def init_widgetfactory_sources():
    WidgetFactorySourceEntryPoints()
    WidgetFactorySourceBuiltin()





#################################
# EXTENSION MANAGER CLASSES #
#################################
class ExtensionManager(AbstractSourceManager):
    pass

class ExtensionSourceMixin(object):
    __concrete_manager__ = ExtensionManager

class ExtensionSourceEntryPoints(ExtensionSourceMixin, EntryPointSourceBase):

    __entry_point__ = "openalea.app.extension"

    def __init__(self):
        ExtensionSourceMixin.__init__(self)
        EntryPointSourceBase.__init__(self)


def init_extension_sources():
    ExtensionSourceEntryPoints()







#################################
# DOCUMENT MANAGER CLASSES #
#################################
class DocumentManager(AbstractSourceManager):
    def __init__(self):
        AbstractSourceManager.__init__(self)
        self.__usersrc = None
        self.__docprops = {}

    def __set_user_source(self, src):
        assert isinstance(src, DocumentSourceUserDocuments)
        self.__usersrc = src

    def add_document(self, doc):
        if self.__usersrc is not None:
            return self.__usersrc.add_document(doc)

    def get_document(self, source=None, name=None):
        if self.__usersrc is not None:
            return self.__usersrc.get_document(source, name)

    def del_document(self, source=None, name=None):
        if self.__usersrc is not None:
            return self.__usersrc.deg_document(source, name)

    def set_document_property(self, doc, key, val):
        self.__docprops.setdefault(doc, {})[key] = val

    def get_document_property(self, doc, key):
        if not self.has_document_property(doc, key):
            return None
        props = self.__docprops.get(doc)
        if props is not None:
            return props.get(key)

    def pop_document_property(self, doc, key):
        if not self.has_document_property(doc, key):
            return None
        props = self.__docprops.get(doc)
        if props is not None:
            return props.pop(key)

    def has_document_property(self, doc, key):
        props = self.__docprops.get(doc)
        if not props:
            return False #TODO : raise something dude
        return key in props


class DocumentSourceMixin(object):
    __concrete_manager__ = DocumentManager

class DocumentSourceEntryPoints(DocumentSourceMixin, EntryPointSourceBase):

    __entry_point__ = "openalea.app.document"

    def __init__(self):
        DocumentSourceMixin.__init__(self)
        EntryPointSourceBase.__init__(self)

class DocumentSourceBuiltin(DocumentSourceMixin, BuiltinSourceBase):

    __mod_name__ = "documents"

    def __init__(self):
        DocumentSourceMixin.__init__(self)
        BuiltinSourceBase.__init__(self)


class DocumentSourceUserDocuments(DocumentSourceMixin, AbstractSource):

    def __init__(self):
        DocumentSourceMixin.__init__(self)
        AbstractSource.__init__(self)
        self.__items    = {}
        DocumentManager()._DocumentManager__set_user_source(self)

    def is_valid(self):
        return True

    def gather_items(self):
        pass

    def get_items(self):
        return self.__items.copy()

    def add_document(self, doc):
        if doc is None:
            return #TODO : raise something dude
        if doc.source in self.__items:
            return #TODO : raise something dude

        #TODO: watch the doc.name! maybe duplicates!

        self.__items[doc.source] = doc
        self.itemListChanged.emit(self, self.__items.copy())

    def get_document(self, source=None, name=None):
        if source is not None:
            return self.__items.get(source)
        elif name is not None:
            for doc in self.__items.itervalues():
                if doc.name == name:
                    return doc

    def del_document(self, source=None, name=None):
        doc = self.get_document(source, name)
        if doc:
            del self.__items[doc.source]
            if doc in self.__docprops:
                del self.__docprops[doc]
        self.itemListChanged.emit(self, self.__items.copy())



def init_document_sources():
    DocumentSourceEntryPoints()
    DocumentSourceUserDocuments()
    DocumentSourceBuiltin()

