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
from openalea.secondnature.data import DataFactory
from openalea.secondnature.layouts import SpaceContent
from PyQt4 import QtCore


class AbstractApplet(HasName):

    __name__ = ""
    __icon_rc__ = None

    def __init__(self):
        HasName.__init__(self, self.__name__)
        self.__dataFacs       = []
        self.__mimemap         = {}
        self.__defaultDataFac = None
        self.__bgpixmap        = None

        # -- icon--
        self.__icon = None
        if QtCore.QCoreApplication.instance():
            if self.__icon_rc__:
                self.__icon = QtGui.QIcon(self.__icon_rc__)
            else:
                self.__icon = QtGui.QIcon()

    def set_default_data_type(self, dt):
        assert dt in self.__dataFacs
        self.__defaultDataFac = dt

    def get_default_data_type(self):
        if self.__defaultDataFac:
            return self.__defaultDataFac
        elif len(self.__dataFacs):
            return self.__dataFacs[0]
        return None

    def get_mimetypes(self):
        return list(self.__mimemap.iterkeys())

    mimetypes = property(lambda x:x.get_mimetypes())

    def create_space_content(self, data):
        raise NotImplementedError

    def _create_space_content_0(self, data):
        space = self.create_space_content(data)
        if data.registerable:
            ProjectManager().set_property_to_active_project(data, "spaceContent", space)
        return space

    def __call__(self):
        return AppletSpace(self)

    #####################
    # Graphical Goodies #
    #####################
    icon = property(lambda x:x.__icon)

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

    #############
    # DataFacs #
    #############
    def add_data_type(self, dt):
        assert isinstance(dt, DataFactory)
        self.__dataFacs.append(dt)
        mimetypes = dt.opened_mimetypes
        for mt in mimetypes:
            self.__mimemap[mt] = dt
        self.__mimemap[dt.created_mimetype] = dt

    if __debug__:
        def add_data_types(self, dts):
            assert isinstance(dts, list)
            for dt in dts:
                self.add_data_type(dt)
    else:
        def add_data_types(self, dts):
            self.__dataFacs.extend(dts)
            d = dict( (dt.mimetype, dt) for dt in dts )
            self.__mimemap.update(d)

    def get_data_types(self):
        return self.__dataFacs[:]

    data_types = property(lambda x:x.__dataFacs[:])











from PyQt4 import QtGui, QtCore
import traceback
from openalea.secondnature.data      import DataSourceManager
from openalea.secondnature.data      import GlobalDataManager
from openalea.secondnature.data      import GlobalData
from openalea.secondnature.project   import ProjectManager
from openalea.secondnature.qtutils   import ComboBox


class AppletSpace(QtGui.QWidget):

    __hh__ = 22  # header content height

    def __init__(self, applet, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setContentsMargins(0,0,0,0)

        assert isinstance(applet, AbstractApplet)
        self.__applet  = applet

        self.__lay     = QtGui.QVBoxLayout(self)
        self.__lay.setContentsMargins(0,0,0,0)
        self.__lay.setSpacing(0)
        self.__toolbar = QtGui.QToolBar()
        self.__stack   = QtGui.QStackedWidget()

        self.__newDataBut    = QtGui.QPushButton("+")
        self.__browseDataBut = ComboBox()
        self.__browseDataBut.setIconSize(QtCore.QSize(16,16))

        # -- configure the layout --
        self.__lay.addWidget(self.__stack)
        self.__lay.addWidget(self.__toolbar)
        self.__newDataBut.setFixedSize(QtCore.QSize(self.__hh__, self.__hh__))
        self.__browseDataBut.setFixedSize(QtCore.QSize(200, self.__hh__))

        # -- an empty widget for the bkgd --
        self.__bkgd = EmptyAppletBackground(applet, self)
        self.__stack.addWidget(self.__bkgd)
        self.__bkgd.show()

        # -- configure the toolbar --
        self.__toolbar.setFloatable(False)
        self.__toolbar.setMovable(False)
        self.__toolbar.addWidget(self.__newDataBut)
        self.__toolbar.addWidget(self.__browseDataBut)

        # -- connect relevant stuff --
        self.__newDataBut.pressed.connect(self.update_dataFac_menu)
        self.__browseDataBut.activated[int].connect(self.show_data_at_index)

        self.update_dataFac_menu()

        proj = ProjectManager().get_active_project()
        data = self.update_combo_list(proj)

        if self.__browseDataBut.count() == 1:
            self.__browseDataBut.setCurrentIndex(0)

        # -- if there is only one data that is global data
        # and no space toolbar or menu hide the header --
        if len(data)==1 and isinstance(data[0][0], GlobalData) and \
           len(self.__toolbar.actions()) == 2:
            self.__toolbar.hide()

        AppletFactoryManager().applet_created.emit(self)


    name = property(lambda x:x.__applet.name)

    def supports(self, data):
        return data.mimetype in self.__applet.mimetypes

    def add_content(self, data, content):
        print "add_content", content.widget
        content = content.widget
        self.__stack.addWidget(content)
        index = self.__browseDataBut.findText(data.name)
        self.__browseDataBut.setCurrentIndex(index)
        self.__stack.setCurrentWidget(content)

    def update_dataFac_menu(self):
        menu = QtGui.QMenu(self.__newDataBut)
        dataFacs = self.__applet.get_data_types()
        dataFacs.sort(cmp = lambda x,y:cmp(x.name, y.name))
        for dt in dataFacs:
            action = menu.addAction(dt.icon, dt.name)
            action.setIconVisibleInMenu(True)
            func = self.__make_dataFac_handler(dt)
            action.triggered.connect(func)
        self.__newDataBut.setMenu(menu)

    def update_combo_list(self, proj, addedData=None, block=True):
        self.__browseDataBut.blockSignals(block)
        currentText = self.__browseDataBut.currentText()
        self.__browseDataBut.clear()

        mimetypes = self.__applet.get_mimetypes()
        data = [(datum,proj) for k, datum in proj if datum.mimetype in mimetypes]
        globalProj = GlobalDataManager()
        data.extend([(datum, globalProj) for k, datum in globalProj \
                     if datum.mimetype in mimetypes])

        for dp in data:
            self.__browseDataBut.addItem(dp[0].icon, dp[0].name,
                                         QtCore.QVariant(dp))

        index = self.__browseDataBut.findText(currentText)
        self.__browseDataBut.setCurrentIndex(index)
        self.__browseDataBut.blockSignals(False)
        return data

    def __make_dataFac_handler(self, dataFac):
        def on_dataFac_chosen(checked):
            data    = dataFac._new_0()
            content = self.__applet._create_space_content_0(data)
            widget  = content.widget
            self.__stack.addWidget(widget)
            index = self.__browseDataBut.findText(data.name)
            self.__browseDataBut.setCurrentIndex(index)
        return on_dataFac_chosen

    def show_data(self, data):
        index = self.__browseDataBut.findText(data.name)
        self.__browseDataBut.setCurrentIndex(index)

    def show_data_at_index(self, index):
        itemData = self.__browseDataBut.itemData(index).toPyObject()
        if not itemData:
            return
        data, proj =  itemData
        content = proj.get_data_property(data, "spaceContent")
        if not content:
            content = self.__applet._create_space_content_0(data)
        widget = content.widget
        if not self.__stack.indexOf(widget)>-1:
            self.__stack.addWidget(widget)
        self.__stack.setCurrentWidget(widget)

    def _set_combo_index(self, index):
        self.__browseDataBut.setCurrentIndex(index)




class EmptyAppletBackground(QtGui.QWidget):
    def __init__(self, applet, appletspace, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__pm = applet.get_background_pixmap()
        self.__lay = QtGui.QVBoxLayout()
        self.__lay.setAlignment(QtCore.Qt.AlignHCenter)
        self.setLayout(self.__lay)

        self.__lay.addStretch()
        for dt in applet.get_data_types():
            but  = QtGui.QPushButton(dt.icon, dt.name)
            policy = QtGui.QSizePolicy.Fixed
            policy = QtGui.QSizePolicy(policy, policy)
            but.setSizePolicy(policy)
            self.__lay.addWidget(but)
            self.__lay.setAlignment(but, QtCore.Qt.AlignHCenter)
            func = self.__make_button_click_handler(but, applet, dt, appletspace)
            but.clicked.connect(func)
        self.__lay.addStretch()

    def __make_button_click_handler(self, but, applet, dataFac, appletspace):
        def on_type_selected(checked):
            data = dataFac._new_0()
            content = applet._create_space_content_0(data)
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

applet_classes = make_manager("AppletFactory",
                               entry_point="openalea.app.applet_factory",
                               builtin="applet_factories", to_derive=True)
AbstractAppletFactoryManager = applet_classes[0]
AppletFactorySourceMixin = applet_classes[1]
AppletFactorySourceEntryPoints, AppletFactorySourceBuiltin = applet_classes[2]

class AppletFactoryManager(AbstractAppletFactoryManager):

    applet_created = QtCore.pyqtSignal(object)

    def __init__(self):
        AbstractAppletFactoryManager.__init__(self)
        self.__mimeMap = {}

    def gather_items(self, refresh=True):
        items = AbstractAppletFactoryManager.gather_items(self, refresh)
        if refresh:
            self.__mimeMap.clear()
            for appFac in items.itervalues():
                if appFac is None:
                    continue
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



AppletFactorySourceMixin.__concrete_manager__ = AppletFactoryManager

AppletFactoryManager()
