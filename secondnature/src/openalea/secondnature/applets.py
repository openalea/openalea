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
from openalea.secondnature.data        import DataFactory
from openalea.secondnature.layouts     import SpaceContent
from openalea.core.singleton           import Singleton

from openalea.core.logger import get_logger

from PyQt4 import QtCore

mod_logger = get_logger(__name__)

class AbstractApplet(HasName, CanBeStarted):

    __metaclass__ = Singleton

    # -- API ATTRIBUTES --
    __name__          = ""
    __icon_rc__       = None
    __datafactories__ = []

    # -- PROPERTIES --
    mimetypes  = property(lambda x:x.get_mimetypes())
    logger     = property(lambda x:x.__logger)
    icon       = property(lambda x:x.__icon)
    data_types = property(lambda x:x.__dataFacs[:])


    def __init__(self):
        HasName.__init__(self, self.__name__)
        CanBeStarted.__init__(self)

        self.__dataFacs       = []
        self.__mimemap        = {}
        self.__defaultDataFac = None
        self.__bgpixmap       = None
        self.__logger         = get_logger("Applet:"+self.__name__)

        # -- icon--
        self.__icon = None
        if QtCore.QCoreApplication.instance():
            if self.__icon_rc__:
                self.__icon = QtGui.QIcon(self.__icon_rc__)
            else:
                self.__icon = QtGui.QIcon()

        self.add_data_types([df() for df in self.__datafactories__])

    #################
    # EXTENSION API #
    #################
    def create_space_content(self, data):
        raise NotImplementedError

    #####################
    # Graphical Goodies #
    #####################
    def get_background_pixmap(self, refresh=False):
        if self.__bgpixmap is None or refresh:
            # -- all icons are 32*32
            iconPixmaps = [dt.icon.pixmap(32,32) for dt in self.__dataFacs \
                           if dt.icon]
            bgw, bgh    = len(iconPixmaps)*32, 32
            bgPixmap    = QtGui.QPixmap(bgw, bgh)
            painter     = QtGui.QPainter(bgPixmap)
            painter.eraseRect(0,0,bgw,bgh)
            for i, icPm in enumerate(iconPixmaps):
                target = QtCore.QRect(i*32, 0, 32, 32)
                source = QtCore.QRect(0, 0, 32, 32)
                painter.drawPixmap(target, icPm, source)
            painter.end()
            self.__bgpixmap = bgPixmap
        return self.__bgpixmap

    #################
    # DataFactories #
    #################
    def add_data_type(self, dt):
        assert isinstance(dt, DataFactory)
        self.__dataFacs.append(dt)
        mimetypes = dt.opened_mimetypes
        for mt in mimetypes:
            self.__mimemap[mt] = dt
        self.__mimemap[dt.created_mimetype] = dt

    def add_data_types(self, dts):
        assert isinstance(dts, list)
        for dt in dts:
            self.add_data_type(dt)

    def get_data_types(self):
        return self.__dataFacs[:]

    def get_mimetypes(self):
        return list(self.__mimemap.iterkeys())

    #################
    # Private Stuff #
    #################
    def _create_space_content_0(self, data):
        space = self.create_space_content(data)
        # NO_SPACE_CONTENT_TRACKING
        # if data.registerable:
        #     ProjectManager().set_property_to_active_project(data, "spaceContent", space)
        return space

    def __call__(self, proj):
        return AppletSpace(proj)






from PyQt4 import QtGui, QtCore
import weakref
import types
import traceback
from openalea.secondnature.data      import DataFactoryManager
from openalea.secondnature.data      import GlobalDataManager
from openalea.secondnature.data      import GlobalData
from openalea.secondnature.project   import Project
from openalea.secondnature.project   import ProjectManager
from openalea.secondnature.qtutils   import ComboBox
from openalea.secondnature.qtutils   import try_to_disconnect
from openalea.secondnature.mimetools import DataEditorSelector

class AppletSpace(QtGui.QWidget):

    # -- PROPERTIES --
    name    = property(lambda x:x.__applet.name if x.__applet else "uknown")
    project = property(lambda x:x.__project)

    # -- NONE API ATTRIBUTES --
    __hh__ = 22  # header content height

    def __init__(self, proj, applet=None, parent=None):
        QtGui.QWidget.__init__(self, parent)

        assert isinstance(applet, (types.NoneType, AbstractApplet))
        self.__applet  = applet
        if applet is None:
            restToApp = False
        self.__restrictedToApplet = restToApp

        self.__project   = proj
        self.__widgetMap = {} #weakref.WeakKeyDictionary()
        self.__projToWidgets = weakref.WeakKeyDictionary()
        self.setContentsMargins(0,0,0,0)
        self.__lay     = QtGui.QVBoxLayout(self)
        self.__lay.setContentsMargins(0,0,0,0)
        self.__lay.setSpacing(0)
        self.__toolbar = QtGui.QToolBar()
        self.__stack   = QtGui.QStackedWidget()


        self.__newDataBut    = QtGui.QPushButton("+")
        self.__browseDataBut = ComboBox()
        self.__browseDataBut.setIconSize(QtCore.QSize(16,16))
        self.__menubar = QtGui.QMenuBar()
        self.__menubar.setDefaultUp(True)

        # -- configure the layout --
        self.__lay.addWidget(self.__stack)
        self.__lay.addWidget(self.__toolbar)
        self.__newDataBut.setFixedSize(QtCore.QSize(40, self.__hh__))
        self.__browseDataBut.setFixedSize(QtCore.QSize(150, self.__hh__))
        self.__menubar.setFixedHeight(self.__hh__)

        # -- an empty widget for the bkgd --
        self.__bkgd = EmptyAppletBackground(applet, self, restToApp=restToApp)
        self.__stack.addWidget(self.__bkgd)
        self.__bkgd.show()

        # -- configure the toolbar --
        self.__toolbar.setStyleSheet("QToolBar{background-color: " +\
                                     "qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, "+\
                                     "stop:0 rgba(135,135,135,255), " +\
                                     "stop:0.1 rgba(175,175,175,255), " +\
                                     "stop:1 rgba(200, 200, 200, 255));}")
        self.__toolbar.setFloatable(False)
        self.__toolbar.setMovable(False)
        self.__toolbar.addWidget(self.__newDataBut)
        self.__toolbar.addWidget(self.__browseDataBut)
        self.__toolbar.addWidget(self.__menubar)

        # -- connect relevant stuff --
        self.__newDataBut.pressed.connect(self.update_dataFac_menu)
        self.__browseDataBut.activated[int].connect(self.show_data_at_index)

        self.update_dataFac_menu()

        data = self.update_combo_list()

        if not restToApp:
            self.__stack.setCurrentWidget(self.__bkgd)
        else:
            if self.__browseDataBut.count() >= 1:
                self.__browseDataBut.setCurrentIndex(0)

        # -- if there is only one data that is global data
        # and no space toolbar or menu hide the header --
        if len(data)==1 and isinstance(data[0][0], GlobalData) and \
           len(self.__toolbar.actions()) == 2 and self.__restrictedToApplet:
            self.__toolbar.hide()

        AppletFactoryManager().applet_created.emit(self)

    @project.setter
    def project(self, proj):
        assert isinstance(proj, Project)

        projWidgets = self.__projToWidgets.get(self.__project, [])
        for w in projWidgets:
            self.__stack.removeWidget(w)

        self.__project = proj
        self.__menubar.clear()
        self.__widgetMap.clear()
        self.__projToWidgets.clear()
        self.update_combo_list()


    def supports(self, data):
        if not self.__restrictedToApplet:
            return True
        else:
            return data.mimetype in self.__applet.mimetypes

    def add_content(self, data, content):
        content = content.widget
        self.__stack.addWidget(content)
        index = self.__browseDataBut.findText(data.name)
        self.__browseDataBut.setCurrentIndex(index)
        self.__stack.setCurrentWidget(content)

    def update_dataFac_menu(self):
        menu = QtGui.QMenu(self.__newDataBut)
        if not self.__restrictedToApplet:
            dataFacs = [f for f in DataFactoryManager().gather_items().itervalues() \
                        if not f.singleton]
        else:
            dataFacs = self.__applet.get_data_types()
        dataFacs.sort(cmp = lambda x,y:cmp(x.name, y.name))
        for dt in dataFacs:
            action = menu.addAction(dt.icon, dt.name)
            action.setIconVisibleInMenu(True)
            func = self.__make_dataFac_handler(dt)
            action.triggered.connect(func)
        self.__newDataBut.setMenu(menu)

    def update_combo_list(self):
        proj = self.__project
        self.__browseDataBut.blockSignals(True)
        currentText = self.__browseDataBut.currentText()
        self.__browseDataBut.clear()

        if not self.__restrictedToApplet:
            mimetypes = [f.created_mimetype for f in \
                         DataFactoryManager().gather_items().itervalues()]
        else:
            mimetypes = self.__applet.get_mimetypes()

        data = [(datum,proj) for k, datum in proj if datum.mimetype in mimetypes]

        for dp in data:
            if dp[0].hidden:
                continue
            self.__browseDataBut.addItem(dp[0].icon, dp[0].name,
                                         QtCore.QVariant(dp))

        self.__browseDataBut.insertSeparator(self.__browseDataBut.count())

        globalProj = GlobalDataManager()
        globalData = [(datum, globalProj) for k, datum in globalProj \
                     if datum.mimetype in mimetypes]

        for dp in globalData:
            if dp[0].hidden:
                continue
            self.__browseDataBut.addItem(dp[0].icon, dp[0].name,
                                         QtCore.QVariant(dp))

        index = self.__browseDataBut.findText(currentText)
        self.__browseDataBut.setCurrentIndex(index)
        self.__browseDataBut.blockSignals(False)
        return data

    def __make_dataFac_handler(self, dataFac):
        def on_dataFac_chosen(checked):
            data    = dataFac._new_0()
            self.show_data(data)
        return on_dataFac_chosen

    def show_data(self, data):
        self.update_combo_list()
        index = self.__browseDataBut.findText(data.name)
        if index > -1: #-1 is not found
            # : calls show_data_at_index by the signals
            self.__browseDataBut.setCurrentIndex(index)

    def show_data_at_index(self, index):
        itemData = self.__browseDataBut.itemData(index).toPyObject()
        if not itemData:
            return
        data, proj =  itemData
        # NO_SPACE_CONTENT_TRACKING
        # content = proj.get_data_property(data, "spaceContent")
        content = self.__widgetMap.get(data)
        if not content:
            if not self.__restrictedToApplet:
                appFac  = DataEditorSelector.mime_type_handler([data.mimetype])
                content = appFac._create_space_content_0(data)
            else:
                content = self.__applet._create_space_content_0(data)
            self.__widgetMap[data]=content
        if content is None:
            print "Applet", self.name, "returned None content"

        widget = content.widget
        self.__projToWidgets.setdefault( proj, set() ).add(widget)
        self.__menubar.clear()
        for menu in content.menus:
            self.__menubar.addMenu(menu)
        if not self.__stack.indexOf(widget)>-1:
            self.__stack.addWidget(widget)
        self.__stack.setCurrentWidget(widget)





class EmptyAppletBackground(QtGui.QWidget):

    __button_width__ = 200

    def __init__(self, applet, appletspace, parent=None, restToApp=False):
        QtGui.QWidget.__init__(self, parent)
        if restToApp:
            self.__pm = applet.get_background_pixmap()
        else:
            self.__pm = None
        self.__lay = QtGui.QVBoxLayout()
        self.__lay.setAlignment(QtCore.Qt.AlignHCenter)
        self.setLayout(self.__lay)

        self.__lay.addStretch()
        if restToApp:
            dataFacs = applet.get_data_types()
        else:
            dataFacs = [f for f in DataFactoryManager().gather_items().itervalues() \
                        if not f.singleton]

        label = QtGui.QLabel("Create a new...")
        label.setFixedWidth(self.__button_width__)
        self.__lay.addWidget(label)
        for dt in dataFacs:
            but  = QtGui.QPushButton(dt.icon, dt.name)
            policy = QtGui.QSizePolicy.Fixed
            #policy = QtGui.QSizePolicy(policy, policy)
            but.setSizePolicy(policy, policy)
            but.setFixedWidth(self.__button_width__)
            self.__lay.addWidget(but)
            self.__lay.setAlignment(but, QtCore.Qt.AlignHCenter)
            func = self.__make_button_click_handler(but, applet, dt, appletspace, restToApp)
            but.clicked.connect(func)
        self.__lay.addStretch()

    def __make_button_click_handler(self, but, applet, dataFac, appletspace, restToApp):
        def on_type_selected(checked):
            data = dataFac._new_0()
            if restToApp:
                content = applet._create_space_content_0(data)
            else:
                appFac  = DataEditorSelector.mime_type_handler([data.mimetype])
                content = appFac._create_space_content_0(data)

            appletspace.show_data(data)
        return on_type_selected

    def paintEvent(self, event):
        rect = self.rect()
        painter = QtGui.QPainter(self)
        painter.eraseRect(rect)
        if self.__pm:
            painter.drawTiledPixmap(rect, self.__pm)
        painter.end()









##################################
# APPLET FACTORY MANAGER CLASSES #
##################################
from openalea.secondnature.managers import make_manager
from openalea.secondnature.managers import AbstractBuiltinSource
from openalea.secondnature.managers import AbstractSourceManager
from openalea.secondnature.managers import AbstractEntryPointSource

applet_sources = []

class AppletFactoryManager(AbstractSourceManager):

    applet_created = QtCore.pyqtSignal(object)

    def __init__(self):
        AbstractSourceManager.__init__(self)
        self.__mimeMap = {}

    def gather_items(self, refresh=False):
        items = AbstractSourceManager.gather_items(self, refresh)
        if refresh:
            self.__mimeMap.clear()
            for appFac in items.itervalues():
                if appFac is None:
                    continue
                if not appFac.started:
                    appFac._start_0()
                fmts = appFac.get_mimetypes()
                for fmt in fmts:
                    self.__mimeMap.setdefault(fmt, set()).add(appFac)
        return items

    def get_handlers_for_mimedata(self, formats):
        factories = self.gather_items()
        handlers = set() # for unicity
        for fm in formats:
            fmt_factories = self.__mimeMap.get(fm)
            if fmt_factories is not None:
                handlers.update(fmt_factories)
        return list(handlers)

    @classmethod
    def init_sources(cls):
        for src in applet_sources:
            src()

class AppletFactorySourceMixin(object):
    __concrete_manager__ = AppletFactoryManager

class AppletFactorySourceBuiltin(AppletFactorySourceMixin, AbstractBuiltinSource):

    __mod_name__ = "applet_factories"

    def __init__(self):
        AppletFactorySourceMixin.__init__(self)
        AbstractBuiltinSource.__init__(self)

applet_sources.append(AppletFactorySourceBuiltin)

class AppletFactorySourceEntryPoints(AppletFactorySourceMixin, AbstractEntryPointSource):
    __entry_point__ = "openalea.app.applet_factory"
    def __init__(self):
        AppletFactorySourceMixin.__init__(self)
        AbstractEntryPointSource.__init__(self)

    def gather_items(self):
        if not self.is_valid():
            return None #TODO : raise something dude
        if self.__entry_point__ is None:
            return None #TODO : raise something dude

        self.items = {}
        for ep in self.pkg_resources.iter_entry_points(self.__entry_point__):
            try:
                AbstractSourceManager.post_status_message(self.__class__.__name__ + \
                                                          " loading  " + ep.name)
                it = ep.load()
                it = it()
            except Exception, e:
                mod_logger.error(self.name + " couldn't load " + str(ep) + ":" + str(e) )
                traceback.print_exc()
                continue
            else:
                key = getattr(it, self.__key__)
                self.items[key] = it
        self.item_list_changed.emit(self, self.items.copy())

applet_sources.append(AppletFactorySourceEntryPoints)
AppletFactoryManager()
