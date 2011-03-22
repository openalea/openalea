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
import traceback

logger = get_logger(__name__)


######################################################
# Base classes and function for manager declarations #
######################################################

class AbstractSourceManager(QtCore.QObject):

    __metaclass__ = make_metaclass((ProxySingleton,),
                                   (QtCore.pyqtWrapperType,))

    item_list_changed = QtCore.pyqtSignal(list)

    __managers__ = []

    def __init__(self):
        QtCore.QObject.__init__(self)
        self._sources     = {}
        self._items       = {}
        self._customItems = {}
        AbstractSourceManager.__managers__.append(self)

    def __iter__(self):
        return self._items.iteritems()

    def add_custom_item(self, name, value):
        self._customItems[name] = value

    def _add_source(self, src):
        if src.name in self._sources:
            return #TODO : raise something dude
        src.item_list_changed.connect(self.update_with_source)
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
            self._items.update(self._customItems)
            self.item_list_changed.emit(list(self._items.iterkeys()))
        return self._items.copy()

    def get(self, name):
        return self._items.get(name, None)

    def iter_item_names(self):
        return self.gather_items().iterkeys()

    def update_with_source(self, src, items):
        self._items.update(items)
        self.item_list_changed.emit(list(self._items.iterkeys()))

    @classmethod
    def init_sources(cls):
        raise NotImplementedError

    @classmethod
    def init(cls):
        from openalea.secondnature.layouts    import LayoutManager
        from openalea.secondnature.applets    import AppletFactoryManager
        from openalea.secondnature.data       import DataFactoryManager

        lm = LayoutManager()
        am = AppletFactoryManager()
        dm = DataFactoryManager()

        lm.init_sources()
        am.init_sources()
        dm.init_sources()

        lm.gather_items(refresh=True)
        am.gather_items(refresh=True)
        dm.gather_items(refresh=True)


class AbstractSource(QtCore.QObject):

    __metaclass__ = make_metaclass((ProxySingleton,),
                                   (QtCore.pyqtWrapperType,))

    # -- EXTENSION POINT SOURCES API ATTRIBUTES --
    __concrete_manager__ = None
    __key__ = "name"

    # -- SIGNALS --
    item_list_changed = QtCore.pyqtSignal(object, dict)

    # -- PROPERTIES --
    name  = property( lambda x:x.__name )
    valid = property( lambda x:x.is_valid())

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.__name = self.__class__.__name__

        mgrCls = self.__concrete_manager__
        if mgrCls is not None:
            mgrCls()._add_source(self)

    #################
    # EXTENSION API #
    #################
    def is_valid(self):
        raise NotImplementedError

    def gather_items(self):
        raise NotImplementedError

    def get_items(self):
        raise NotImplementedError




class AbstractEntryPointSource(AbstractSource):

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
                traceback.print_exc()
                continue
            else:
                key = getattr(it, self.__key__)
                self.items[key] = it
        self.item_list_changed.emit(self, self.items.copy())

    def get_items(self):
        return self.items.copy()



class AbstractBuiltinSource(AbstractSource):

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
            traceback.print_exc()
        self.__items = None

    def is_valid(self):
        return self.mod is not None

    def gather_items(self):
        if not self.is_valid():
            return None #TODO : raise something dude
        itemlist = self.mod.get_builtins()
        self.__items = dict( (getattr(v, self.__key__), v) for v in itemlist)
        self.item_list_changed.emit(self, self.__items.copy())

    def get_items(self):
        return self.__items.copy()



def make_manager(name, entry_point=None, builtin=None, to_derive=False, key="name"):

    sources = []

    class MetaManager(AbstractSourceManager):
        @classmethod
        def init_sources(cls):
            for src in sources:
                src()

    MetaManager.__name__ = name+("ManagerBase"if to_derive else "Manager")

    class MetaSourceMixin(object):
        __concrete_manager__ = MetaManager
        __key__ = key
    MetaSourceMixin.__name__ = name+"SourceMixin"

    if builtin is not None:
        class MetaSourceBuiltin(MetaSourceMixin, AbstractBuiltinSource):

            __mod_name__ = builtin

            def __init__(self):
                MetaSourceMixin.__init__(self)
                AbstractBuiltinSource.__init__(self)
        MetaSourceBuiltin.__name__ = name+"SourceBuiltin"
        sources.append(MetaSourceBuiltin)

    if entry_point is not None:
        class MetaSourceEntryPoints(MetaSourceMixin, AbstractEntryPointSource):
            __entry_point__ = entry_point

            def __init__(self):
                MetaSourceMixin.__init__(self)
                AbstractEntryPointSource.__init__(self)
        MetaSourceEntryPoints.__name__ = name+"SourceEntryPoints"
        sources.append(MetaSourceEntryPoints)


    return MetaManager, MetaSourceMixin, sources

#############################################################
# End of base classes and function for manager declarations #
#############################################################





