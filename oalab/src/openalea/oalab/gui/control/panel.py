
from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.observer import AbstractListener
from openalea.oalab.service.qt_control import qt_editor

from openalea.oalab.gui.control.ui_widget_container import Ui_WidgetContainer

MODE_VIEW = 0
# MODE_EDIT = 1
MODE_DESIGN = 1

class WidgetContainer2(QtGui.QWidget, Ui_WidgetContainer):
    def __init__(self, title):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.l_title.setText(title)
        self._decorations = [self.line, self.line_2, self.l_title,
                             self.bottom_left, self.bottom_right,
                             self.top_left, self.top_right]

    def show_decoration(self, state=True):
        for deco in self._decorations:
            deco.setVisible(state)

class WidgetContainer(QtGui.QWidget):
    def __init__(self, widget, title):
        QtGui.QWidget.__init__(self)
        self.widget = widget
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(widget)

    def set_mode(self, mode):
        if mode == MODE_DESIGN:
            self.widget.setStyleSheet("background-color:rgba(200,200,255,100);")
            self.setStyleSheet("background-color:rgba(200,200,255,100);")
        else:
            color = QtGui.QApplication.palette().color(QtGui.QPalette.Window)
            r = color.red()
            g = color.green()
            b = color.blue()
            a = 0
            self.widget.setStyleSheet("background-color:rgba(%d, %d, %d, %d);" % (r, g, b, a))
            self.setStyleSheet("background-color:rgba(%d, %d, %d, %d);" % (r, g, b, a))

cls = QtGui.QGraphicsProxyWidget
class WidgetItem(cls):
    def __init__(self, widget, pos, title=''):
        cls.__init__(self)


        self.container = WidgetContainer(widget, title=title)
#         self.resize(100, 100)
#         self.container.resize(100, 100)

        self.acceptHoverEvents()

        self.setWidget(self.container)
        self.setFlag(self.ItemIsMovable, True)
#         self.setFlag(self.ItemIsFocusable, True)
        self.setFlag(self.ItemIsSelectable, True)

        self._mode = MODE_VIEW

    def set_mode(self, mode):
        self._mode = mode
        self.container.set_mode(mode)

#     def hoverEnterEvent(self, event):
#         inframe = self._in_frame(event)
#         if inframe:
#             self.show_decoration(True)
#         else:
#             self.show_decoration(False)
#
#     def hoverLeaveEvent(self, event):
#         inframe = self._in_frame(event)
#         if inframe:
#             self.show_decoration(True)
#         else:
#             self.show_decoration(False)

    def _in_frame(self, event):
        margin = 10
        tl = self.rect().topLeft()
        br = self.rect().bottomRight()
        xmin = tl.x()
        xmax = br.x()
        ymin = tl.y()
        ymax = br.y()

        x = event.pos().x()
        y = event.pos().y()

        inframe = False

        # top left
        if (x - xmin) < margin and (y - ymin) < margin:
            inframe = True
        return True

    def mousePressEvent(self, event):
        if self._mode == MODE_DESIGN:
            return QtGui.QGraphicsItem.mousePressEvent(self, event)
        else:
            return QtGui.QGraphicsProxyWidget.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self._mode == MODE_DESIGN:
            return QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
        else:
            return QtGui.QGraphicsProxyWidget.mouseReleaseEvent(self, event)

    def mouseMoveEvent(self, event):
        if self._mode == MODE_DESIGN:
            return QtGui.QGraphicsItem.mouseMoveEvent(self, event)
        else:
            return QtGui.QGraphicsProxyWidget.mouseMoveEvent(self, event)


class ControlPanelScene(QtGui.QGraphicsScene):
    def __init__(self):
        QtGui.QGraphicsScene.__init__(self, parent=None)
        self._pos = None
        self._item = None
        self._mode = MODE_VIEW
        self.witems = []

    def add_control(self, control, pos=None):

        widget = qt_editor(control, 'large')
        if widget:

            if pos is None:
                pos = QtCore.QPointF(0, 0)

            item = WidgetItem(widget, pos, control.name)
            item.set_mode(self._mode)
            self.witems.append(item)
            self.addItem(item)


    def set_mode(self, mode):
        self._mode = mode
        for witem in self.witems:
            witem.set_mode(mode)


    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('openalealab/control'):
            event.acceptProposedAction()
        else:
            return QtGui.QWidget.dragEnterEvent(self, event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('openalealab/control'):
            event.acceptProposedAction()
        else:
            for fmt in event.mimeData().formats():
                print fmt, event.mimeData().data(fmt)
            event.ignore()
            return False

    def dropEvent(self, event):
        source = event.mimeData()
        fmt = 'openalealab/control'
        if source.hasFormat(fmt):
            from openalea.oalab.service.mimetype import decode
            control = decode(fmt, source.data(fmt))
            pos = event.scenePos()
            self.add_control(control, pos)
            event.acceptProposedAction()
        else:
            return QtGui.QWidget.dropEvent(self, event)


class ControlGraphicsView(QtGui.QGraphicsView):

    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
#         self.setDragMode(self.ScrollHandDrag)
        self.scene = ControlPanelScene()
        self.setScene(self.scene)

    def sizeHint(self):
        return QtCore.QSize(300, 300)

    def set_mode(self, mode=MODE_VIEW):
        self.scene.set_mode(mode)


class ControlPanel(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.view = ControlGraphicsView()
        self.cb_edit_mode = QtGui.QComboBox()
        for mode in ['User mode (change values)', 'Designer mode (place widgets)']:
            self.cb_edit_mode.addItem(mode)
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.cb_edit_mode)
        self.cb_edit_mode.currentIndexChanged.connect(self._mode_changed)

    def _mode_changed(self, idx):
        self.view.set_mode(idx)

    def add_control(self, control):
        self.view.scene.add_control(control)


