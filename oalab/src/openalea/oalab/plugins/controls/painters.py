# -*- coding: utf-8 -*-

from openalea.vpltk.qt import QtCore, QtGui

from openalea.oalab.service.interface import alias
from openalea.oalab.control.control import Control

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
        self.paint_data(alias(control.interface), painter, rectangle, option)

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
