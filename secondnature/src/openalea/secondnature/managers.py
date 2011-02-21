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
    init_layout_sources()
    init_docwidgetfactory_sources()
    init_reswidgetfactory_sources()
    init_document_sources()
    ExtensionManager().gather_items(refresh=True)
    LayoutManager().gather_items(refresh=True)
    DocumentWidgetFactoryManager().gather_items(refresh=True)
    ResourceWidgetFactoryManager().gather_items(refresh=True)
    DocumentManager().gather_items(refresh=True)




######################################################
# Base classes and function for manager declarations #
######################################################

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
            self.itemListChanged.emit(list(self._items.iterkeys()))
        return self._items.copy()

    def get(self, name):
        items = self.gather_items()
        return items.get(name, None)

    def iter_item_names(self):
        return self.gather_items().iterkeys()

    def update_with_source(self, src, items):
        self._items.update(items)
        self.itemListChanged.emit(list(self._items.iterkeys()))



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
                logger.error(self.name + " couldn't load " + str(ep) + ":" + str(e) )
            except SyntaxError, e:
                logger.error(self.name + " couldn't load " + str(ep) + ":" + str(e) )
            else:
                self.items[it.fullname] = it
        self.itemListChanged.emit(self, self.items.copy())

    def get_items(self):
        return self.items.copy()



class BuiltinSourceBase(AbstractSource):

    __mod_name__ = None

    def __init__(self):
        AbstractSource.__init__(self)
        name = ".".join(["openalea.secondnature.builtins",self.__mod_name__])
        try:
            self.mod = __import__(name,
                                  fromlist=[self.__mod_name__])
        except ImportError, e:
            logger.error("Couldn't import " + name + ":" + str(e))
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



def make_manager(name, entry_point=None, builtin=None, is_base=False):

    class MetaManager(AbstractSourceManager):
        pass
    MetaManager.__name__ = name+("ManagerBase"if is_base else "Manager")

    class MetaSourceMixin(object):
        __concrete_manager__ = MetaManager
    MetaSourceMixin.__name__ = name+"SourceMixin"

    sources = []

    if entry_point is not None:
        class MetaSourceEntryPoints(MetaSourceMixin, EntryPointSourceBase):
            __entry_point__ = entry_point

            def __init__(self):
                MetaSourceMixin.__init__(self)
                EntryPointSourceBase.__init__(self)
        MetaSourceEntryPoints.__name__ = name+"SourceEntryPoints"
        sources.append(MetaSourceEntryPoints)

    if builtin is not None:
        class MetaSourceBuiltin(MetaSourceMixin, BuiltinSourceBase):

            __mod_name__ = builtin

            def __init__(self):
                MetaSourceMixin.__init__(self)
                BuiltinSourceBase.__init__(self)
        MetaSourceBuiltin.__name__ = name+"SourceBuiltin"
        sources.append(MetaSourceBuiltin)

    def meta_init_sources():
        for src in sources:
            src()

    return MetaManager, MetaSourceMixin, sources, meta_init_sources

#############################################################
# End of base classes and function for manager declarations #
#############################################################







#################################
# EXTENSION MANAGER CLASSES #
#################################
ExtensionManager, ExtensionSourceMixin, (ExtensionSourceEntryPoints,), init_extension_sources = make_manager("Extension",
                                                                                                             entry_point="openalea.app.extension")




##########################
# LAYOUT MANAGER CLASSES #
##########################
LayoutManager, LayoutSourceMixin, (LayoutSourceEntryPoints, LayoutSourceBuiltin), init_layout_sources = make_manager("Layout",
                                                                                                                     entry_point="openalea.app.layout",
                                                                                                                     builtin="layouts")




##########################################
# DOCUMENT WIDGETFACTORY MANAGER CLASSES #
##########################################
doc_wid_classes = make_manager("DocumentWidgetFactory",
                               entry_point="openalea.app.document_widget_factory",
                               builtin="document_widget_factories", is_base=True)
DocumentWidgetFactoryManagerBase, DocumentWidgetFactorySourceMixin, (DocumentWidgetFactorySourceEntryPoints, DocumentWidgetFactorySourceBuiltin), init_docwidgetfactory_sources = doc_wid_classes

class DocumentWidgetFactoryManager(DocumentWidgetFactoryManagerBase):
    def __init__(self):
        DocumentWidgetFactoryManagerBase.__init__(self)
        self.__mimeMap = {}

    def gather_items(self, refresh=True):
        items = DocumentWidgetFactoryManagerBase.gather_items(self, refresh)
        if refresh:
            self.__mimeMap.clear()
            for v in items.itervalues():
                if v is None:
                    continue
                fmts = v.get_mime_formats()
                for fmt in fmts:
                    self.__mimeMap.setdefault(fmt, set()).add(v)
        return items

    def get_handlers_for_mimedata(self, mimedata):
        fmts = mimedata.formats()
        factories = self.gather_items()
        handlers = set()
        for fm in fmts:
            fm = str(fm)
            fmt_factories = self.__mimeMap.get(fm)
            if fmt_factories is not None:
                handlers.update(fmt_factories)
        return list(handlers)


DocumentWidgetFactorySourceMixin.__concrete_manager__ = DocumentWidgetFactoryManager

###########################################
# RESOURCES WIDGETFACTORY MANAGER CLASSES #
###########################################
res_wid_classes = make_manager("DocumentWidgetFactory", entry_point="openalea.app.resource_widget_factory",
                           builtin="resource_widget_factories")
ResourceWidgetFactoryManager, ResourceWidgetFactorySourceMixin, (ResourceWidgetFactorySourceEntryPoints, ResourceWidgetFactorySourceBuiltin), init_reswidgetfactory_sources = res_wid_classes



############################
# DOCUMENT MANAGER CLASSES #
############################
DocumentManagerBase, DocumentSourceMixin, doc_sources, init_document_sources = make_manager("Document",
                                                                                            entry_point="openalea.app.document",
                                                                                            builtin="documents",
                                                                                            is_base=True)
DocumentSourceEntryPoints, DocumentSourceBuiltin = doc_sources

class DocumentManager(DocumentManagerBase):
    def __init__(self):
        DocumentManagerBase.__init__(self)
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


DocumentSourceMixin.__concrete_manager__ = DocumentManager


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


doc_sources.append(DocumentSourceUserDocuments)
