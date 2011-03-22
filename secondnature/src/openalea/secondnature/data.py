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

from openalea.secondnature.base_mixins import HasName
from openalea.secondnature.base_mixins import CanBeStarted
from openalea.secondnature.project     import ProjectManager
from PyQt4 import QtGui, QtCore





class DataFactory(HasName, CanBeStarted):

    # -- API ATTRIBUTES --
    __name__             = ""
    __created_mimetype__ = ""
    __opened_mimetypes__ = []
    __icon_rc__          = None
    __supports_open__    = False

    # -- PROPERTIES --
    icon             = property(lambda x:x.__icon)
    opened_mimetypes = property(lambda x:x.__opened_mimetypes__[:])
    created_mimetype = property(lambda x:x.__created_mimetype__)


    def __init__(self, parent=None):
        HasName.__init__(self, self.__name__)
        CanBeStarted.__init__(self)

        # -- icon--
        self.__icon = None
        if QtCore.QCoreApplication.instance():
            if self.__icon_rc__:
                self.__icon = QtGui.QIcon(self.__icon_rc__)
            else:
                self.__icon = QtGui.QIcon()

    #################
    # EXTENSION API #
    #################
    def data_from_stream(self, name, stream, type="b"):
        import cPickle
        obj = cPickle.load(stream)
        return self.wrap_data(name, obj, cls=type)

    def data_to_stream(self, data, stream):
        import cPickle
        cPickle.dump(data.obj, stream, cPickle.HIGHEST_PROTOCOL)

    def new(self):
        raise NotImplementedError

    def supports_open(self):
        return self.__supports_open__

    ###########
    # UTILITY #
    ###########
    def wrap_data(self, name, obj, cls="b", **kwargs):
        if cls=="b":
            cls = Data
        elif cls=="u":
            cls = UnregisterableData
        elif cls=="g":
            cls = GlobalData
        return self.__patch_data(cls(name, obj, **kwargs))

    ###################
    # Protected Stuff #
    ###################
    def _new_0(self):
        data = self.new()
        if data.registerable:
            ProjectManager().add_data_to_active_project(data)
        return data

    def __patch_data(self, data):
        data._Data__set_data_type(self, self.__created_mimetype__)
        return data






class DataReader(DataFactory):
    __supports_open__ = True

    def _open_url_0(self, parsedUrl):
        data = self.open_url(parsedUrl)
        if data.registerable:
            ProjectManager().add_data_to_active_project(data)
        return data

    def open_url(self, parsedUrl):
        raise NotImplementedError




class Data(HasName):
    """"""

    # -- PROPERTIES --
    obj          = property(lambda x:x.__obj)
    registerable = property(lambda x:True)
    mimetype     = property(lambda x:x.__mimetype)
    icon         = property(lambda x:x.__dt.icon if x.__dt else QtGui.QIcon())
    factory_name = property(lambda x:x.__dt.name)
    type         = property(lambda x:"b")

    def __init__(self, name, obj, **kwargs):
        HasName.__init__(self, name)
        self.__obj     = obj
        self.__mimetype = None
        self.__props    = kwargs.copy()
        self.__dt = None

    def get_inner_property(self, key):
        return self.__props.get(key)

    def __set_data_type(self, dt, mimetype):
        assert isinstance(dt, DataFactory)
        self.__dt = dt
        self.__mimetype = mimetype

    def to_stream(self, stream):
        self.__dt.data_to_stream(self, stream)




class UnregisterableData(Data):
    # -- API ATTRIBUTES --
    registerable = property(lambda x:False)

    # -- PROPERTIES --
    type         = property(lambda x:"u")

class GlobalData(UnregisterableData):
    # -- PROPERTIES --
    type         = property(lambda x:"g")

    def __init__(self, name, obj, **kwargs):
        UnregisterableData.__init__(self, name, obj, **kwargs)
        GlobalDataManager().add_data(self)




__global_data_manager = None
def GlobalDataManager():
    global __global_data_manager
    if __global_data_manager is None:
        from openalea.secondnature.project import Project
        __global_data_manager = Project("Global")
    return __global_data_manager





#############################
# DATATYPE  MANAGER CLASSES #
#############################
from openalea.secondnature.managers import make_manager, AbstractSource

datatype_classes = make_manager("DataFactory", to_derive=True)

AbstractDataFactoryManager = datatype_classes[0]
DataFactorySourceMixin = datatype_classes[1]
DataFactorySources = datatype_classes[2]

class DataFactoryManager(AbstractDataFactoryManager):

    data_created              = QtCore.pyqtSignal(object)
    data_property_set_request = QtCore.pyqtSignal(object, str, object)

    def __init__(self):
        AbstractDataFactoryManager.__init__(self)
        self.__mimeMap = {}

    def gather_items(self, refresh=False):
        items = AbstractDataFactoryManager.gather_items(self, refresh)
        if refresh:
            self.__mimeMap.clear()
            for datatype in items.itervalues():
                if not datatype.started:
                    datatype._start_0()
                if datatype is None or not datatype.supports_open():
                    continue
                fmts = datatype.opened_mimetypes
                for fmt in fmts:
                    self.__mimeMap.setdefault(fmt, set()).add(datatype)
        return items

    def get_handlers_for_mimedata(self, formats):
        datatypes = self.gather_items()
        handlers = set() # for unicity
        for fm in formats:
            fmt_datatypes = self.__mimeMap.get(fm)
            if fmt_datatypes is not None:
                handlers.update(fmt_datatypes)
        return list(handlers)



class DataFactoryAppletSource(DataFactorySourceMixin, AbstractSource):
    """A DataFactory source that gathers DataFactories from applets.
    It must therefor be loaded after the AppletManager."""
    def __init__(self):
        DataFactorySourceMixin.__init__(self)
        AbstractSource.__init__(self)
        self.items = {}
    def is_valid(self):
        return True

    def gather_items(self):
        from openalea.secondnature.applets import AppletFactoryManager
        APM = AppletFactoryManager()
        appletFactories = APM.gather_items()

        self.items.clear()
        for appFac in appletFactories.itervalues():
            dataTypes = appFac.get_data_types()
            self.items.update( (dt.name, dt) for dt in dataTypes )
        self.item_list_changed.emit(self, self.items.copy())

    def get_items(self):
        return self.items.copy()


DataFactorySourceMixin.__concrete_manager__ = DataFactoryManager
DataFactorySources.append(DataFactoryAppletSource)
dtmgr = DataFactoryManager()
add_custom_data_factory = dtmgr.add_custom_item
