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
from openalea.secondnature.data import AbstractDataType
from openalea.secondnature.layouts import SpaceContent
from PyQt4 import QtCore

class AbstractApplet(HasName):

    __name__ = ""
    __icon_rc__ = None

    def __init__(self):
        HasName.__init__(self, self.__name__)
        self.__datatypes       = []
        self.__mimemap         = {}
        self.__defaultDataType = None
        self.__bgpixmap        = None

        # -- icon--
        self.__icon = None
        if QtCore.QCoreApplication.instance():
            if self.__icon_rc__:
                self.__icon = QtGui.QIcon(self.__icon_rc__)
            else:
                self.__icon = QtGui.QIcon()

    def set_default_data_type(self, dt):
        assert dt in self.__datatypes
        self.__defaultDataType = dt

    def get_default_data_type(self):
        if self.__defaultDataType:
            return self.__defaultDataType
        elif len(self.__datatypes):
            return self.__datatypes[0]
        return None

    def get_mimetypes(self):
        return list(self.__mimemap.iterkeys())

    def create_space_content(self, data):
        raise NotImplementedError

    def _create_space_content_0(self, data):
        space = self.create_space_content(data)
        if data.registerable:
            ProjectManager().set_property_to_active_project(data, "space", space)
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
            iconPixmaps = [dt.icon.pixmap(32,32) for dt in self.__datatypes \
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
    # DataTypes #
    #############
    def add_data_type(self, dt):
        assert isinstance(dt, AbstractDataType)
        self.__datatypes.append(dt)
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
            self.__datatypes.extend(dts)
            d = dict( (dt.mimetype, dt) for dt in dts )
            self.__mimemap.update(d)

    def get_data_types(self):
        return self.__datatypes[:]

    data_types = property(lambda x:x.__datatypes[:])











from PyQt4 import QtGui, QtCore
import traceback
from openalea.secondnature.data      import DataTypeManager
from openalea.secondnature.data      import GlobalDataManager
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
        self.__newDataBut.pressed.connect(self.update_datatype_menu)
        self.__browseDataBut.currentIndexChanged[int].connect(self.show_data)

        self.update_datatype_menu()
        proj = ProjectManager().get_active_project()
        self.update_combo_list(proj)
        if self.__browseDataBut.count() == 1:
            self.__browseDataBut.setCurrentIndex(0)

        AppletFactoryManager().applet_created.emit(self)



    name = property(lambda x:x.__applet.name)

    def update_datatype_menu(self):
        menu = QtGui.QMenu(self.__newDataBut)
        datatypes = self.__applet.get_data_types()
        datatypes.sort(cmp = lambda x,y:cmp(x.name, y.name))
        for dt in datatypes:
            action = menu.addAction(dt.icon, dt.name)
            action.setIconVisibleInMenu(True)
            func = self.__make_datatype_handler(dt)
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

    def __make_datatype_handler(self, datatype):
        def on_datatype_chosen(checked):
            data    = datatype._new_0()
            space   = self.__applet._create_space_content_0(data)
            content = space.content
            self.__stack.addWidget(content)
#            self.__stack.setCurrentWidget(content)
            index = self.__browseDataBut.findText(data.name)
            self.__browseDataBut.setCurrentIndex(index)
        return on_datatype_chosen

    def show_data(self, index):
        data, proj =  self.__browseDataBut.itemData(index).toPyObject()
        space = proj.get_data_property(data, "space")
        if not space:
            space = self.__applet._create_space_content_0(data)
        content = space.content
        content.show()
        if not self.__stack.indexOf(content)>-1:
            self.__stack.addWidget(content)
        self.__stack.setCurrentWidget(content)

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

    def __make_button_click_handler(self, but, applet, datatype, appletspace):
        def on_type_selected(checked):
            data = datatype._new_0()
            space = applet._create_space_content_0(data)
            appletspace._set_combo_index(0)
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
