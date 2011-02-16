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
    LayoutManager().gather_items(refresh=True)
    WidgetFactoryManager().gather_items(refresh=True)
    ExtensionManager().gather_items(refresh=True)


class AbstractSourceManager(QtCore.QObject):

    __metaclass__ = make_metaclass((ProxySingleton,),
                                   (QtCore.pyqtWrapperType,))

    itemListChanged = QtCore.pyqtSignal(list)

    def __init__(self):
        QtCore.QObject.__init__(self)
        self._sources = {}
        self._items   = {}

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
                logger.error(self.name + " couldn't load " + ep)
            else:
                self.items[it.fullname] = it
        self.itemListChanged.emit(self, self.items.copy())

    def get_items(self):
        if self.__items is None:
            self.gather_items()
        return self.items.copy()



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
        factories = self.gather_items()
        for it in factories.itervalues():
            if it.handles(input):
                return it
        return None

    def no_data_factory_names(self):
        factories = self.gather_items()
        return [f for f, v in factories.iteritems() if v.creates_without_data()]

    def create_space_for(self, input, parent):
        factory = self.has_handler_for(input)
        if not factory:
            return None, None
        else:
            return factory(input, parent)

    def create_space(self, name, parent):
        factories = self.gather_items()
        if name not in factories:
            return #TODO : raise something dude
        else:
            return factories[name](None, parent)

class WidgetFactorySourceMixin(object):
    __concrete_manager__ = WidgetFactoryManager

class WidgetFactorySourceEntryPoints(WidgetFactorySourceMixin, EntryPointSourceBase):

    __entry_point__ = "openalea.app.widget_factory"

    def __init__(self):
        WidgetFactorySourceMixin.__init__(self)
        EntryPointSourceBase.__init__(self)

def init_widgetfactory_sources():
    WidgetFactorySourceEntryPoints()



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



