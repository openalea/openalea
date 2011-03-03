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
    init_layout_sources()
    init_applet_sources()
    LayoutManager().gather_items(refresh=True)
    AppletFactoryManager().gather_items(refresh=True)


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
    __key__ = "fullname"

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
        self.pkg_resources = None
        try:
            import pkg_resources
        except ImportError:
            logger.error("Setuptools' pkg_resources not available. No entry point extensions.")
        else:
            self.pkg_resources = pkg_resources
        self.items = None

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
            except Exception, e:
                logger.error(self.name + " couldn't load " + str(ep) + ":" + str(e) )
                continue
            else:
                key = getattr(it, self.__key__)
                self.items[key] = it
        self.itemListChanged.emit(self, self.items.copy())

    def get_items(self):
        return self.items.copy()



class BuiltinSourceBase(AbstractSource):

    __mod_name__ = None

    def __init__(self):
        AbstractSource.__init__(self)
        name = ".".join(["openalea.secondnature.builtins",self.__mod_name__])
        self.mod = None
        try:
            self.mod = __import__(name,
                                  fromlist=[self.__mod_name__])
        except Exception, e:
            logger.error("Couldn't import " + name + ":" + str(e))
        self.__items = None

    def is_valid(self):
        return self.mod is not None

    def gather_items(self):
        if not self.is_valid():
            return None #TODO : raise something dude
        itemlist = self.mod.get_builtins()
        self.__items = dict( (getattr(v, self.__key__), v) for v in itemlist)
        self.itemListChanged.emit(self, self.__items.copy())

    def get_items(self):
        return self.__items.copy()



def make_manager(name, entry_point=None, builtin=None, is_base=False, key="fullname"):

    class MetaManager(AbstractSourceManager):
        pass
    MetaManager.__name__ = name+("ManagerBase"if is_base else "Manager")

    class MetaSourceMixin(object):
        __concrete_manager__ = MetaManager
        __key__ = key
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




##########################
# LAYOUT MANAGER CLASSES #
##########################
layout_classes = make_manager("Layout",
                              entry_point="openalea.app.layout",
                              builtin="layouts",
                              key="easyname")
LayoutManager = layout_classes[0]
LayoutSourceMixin = layout_classes[1]
LayoutSourceEntryPoints, LayoutSourceBuiltin = layout_classes[2]
init_layout_sources = layout_classes[3]


##########################################
# DOCUMENT WIDGETFACTORY MANAGER CLASSES #
##########################################
applet_classes = make_manager("AppletFactory",
                               entry_point="openalea.app.applet_factory",
                               builtin="applet_factories", is_base=True)
AppletFactoryManagerBase = applet_classes[0]
AppletFactorySourceMixin = applet_classes[1]
AppletFactorySourceEntryPoints, AppletFactorySourceBuiltin = applet_classes[2]
init_applet_sources = applet_classes[3]

class AppletFactoryManager(AppletFactoryManagerBase):
    def __init__(self):
        AppletFactoryManagerBase.__init__(self)
        self.__mimeMap = {}

    def gather_items(self, refresh=True):
        items = AppletFactoryManagerBase.gather_items(self, refresh)
        if refresh:
            self.__mimeMap.clear()
            for v in items.itervalues():
                if v is None or not v.supports_document_open():
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


AppletFactorySourceMixin.__concrete_manager__ = AppletFactoryManager


