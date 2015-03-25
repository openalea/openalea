# -*- coding: utf-8 -*-

from openalea.vpltk.qt import QtCore, QtGui

from openalea.core.service.interface import interface_alias
from openalea.core.control import Control


class AbstractPainter(object):

    def __call__(self, data, painter, rectangle, option=None):
        if isinstance(data, Control):
            self.paint_control(data, painter, rectangle, option)
        else:
            self.paint_data(data, painter, rectangle, option)

    def paint_control(self, control, painter, rectangle, option=None):
        self.paint_data(control.value, painter, rectangle, option)

    def paint_data(self, data, painter, rectangle, option=None):
        raise NotImplementedError


class PainterInterfaceObject(AbstractPainter):

    def paint_control(self, control, painter, rectangle, option=None):
        self.paint_data(interface_alias(control.interface), painter, rectangle, option)

    def paint_data(self, data, painter, rectangle, option=None):
        painter.save()

        pen = QtGui.QPen()
        if option and option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
            pen.setColor(option.palette.highlightedText().color())
        else:
            pen.setColor(QtCore.Qt.blue)
        painter.setPen(pen)

        painter.setRenderHint(painter.Antialiasing, True)

        text_option = QtGui.QTextOption()
        text_option.setAlignment(QtCore.Qt.AlignHCenter)
        painter.drawText(QtCore.QRectF(rectangle), data, text_option)
        painter.restore()


class PainterColormap(AbstractPainter):

    def paint_data(self, data, painter, rectangle, option=None):
        painter.save()
        r = rectangle
        x = r.bottomLeft().x()
        y = r.topRight().y()
        lx = r.width() / 101.

        points = data.keys()

        if len(points) > 1:
            points.sort()
            prev_point = points[0]
            prev_color = tuple([255 * data[prev_point][c] for c in [0, 1, 2]])

            for point in points[1:]:
                gradient = QtGui.QLinearGradient(x + prev_point * 100 * lx, y, x + point * 100 * lx, y)
                gradient.setColorAt(0, QtGui.QColor(*prev_color))
                color = tuple([255 * data[point][c] for c in [0, 1, 2]])
                gradient.setColorAt(1, QtGui.QColor(*color))
                painter.fillRect(x + prev_point * 100 * lx, y, (point - prev_point) * 100 * lx, r.height(), gradient)
                prev_point = point
                prev_color = color

        painter.restore()
