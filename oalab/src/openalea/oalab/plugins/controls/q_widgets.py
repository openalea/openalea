from openalea.vpltk.qt import QtCore, QtGui

class QFloatSlider(QtGui.QSlider):

    floatValueChanged = QtCore.Signal(float)

    def __init__(self, orientation=QtCore.Qt.Horizontal):
        QtGui.QSlider.__init__(self, orientation)
        self.connect(self, QtCore.SIGNAL('valueChanged(int)'), self.notifyValueChanged)
        self.slider_step = 0.1
        self.floatValue = 0.0

    def notifyValueChanged(self, value):
        self.floatValue = value*self.slider_step
        self.floatValueChanged.emit(self.floatValue)

    def setFloatValue(self, value):
        self.floatValue = value
        self.setValue(round(value/self.slider_step))
        # self.floatValueChanged.emit(self.floatValue)
        # self.setValue(int(float(value)/self.slider_step))

    def value(self):
        return self.floatValue

    def setStep(self, step):
        self.slider_step = step


class QSpanSlider(QtGui.QSlider):
    # Based on QxtSpanSlider.py

    # The MIT License (MIT)

    # Copyright (c) 2011-2014 Marvin Killing

    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions:

    # The above copyright notice and this permission notice shall be included in
    # all copies or substantial portions of the Software.

    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    # THE SOFTWARE.

    spanChanged = QtCore.Signal(int,int)
    upperPositionChanged = QtCore.Signal(int)
    lowerPositionChanged = QtCore.Signal(int)
    sliderPressed = QtCore.Signal(int)

    NoHandle = None
    LowerHandle = 1
    UpperHandle = 2

    def __init__(self, orientation = QtCore.Qt.Horizontal,  parent = None):
        QtGui.QSlider.__init__(self, orientation, parent)

        # self.connect(self, SIGNAL("rangeChanged(int, int)"), self.updateRange)
        self.connect(self, QtCore.SIGNAL("sliderReleased()"), self.movePressedHandle)
        # self.setStyle(QStyleFactory.create('Plastique'))

        self.lower = 0
        self.upper = 0
        self.lowerPos = 0
        self.upperPos = 0
        self.offset = 0
        self.position = 0
        self.lastPressed = QSpanSlider.NoHandle
        self.upperPressed = QtGui.QStyle.SC_None
        self.lowerPressed = QtGui.QStyle.SC_None
        # self.movement = QSpanSlider.FreeMovement
        self.mainControl = QSpanSlider.LowerHandle
        self.firstMovement = False
        self.blockTracking = False
        self.gradientLeft = self.palette().color(QtGui.QPalette.Dark).light(110)
        self.gradientRight = self.palette().color(QtGui.QPalette.Dark).light(110)

    def lowerValue(self):
        return min(self.lower, self.upper)
        
    def setLowerValue(self, lower):
        self.setSpan(lower, self.upper)
        
    def upperValue(self):
        return max(self.lower, self.upper)
        
    def setUpperValue(self, upper):
        self.setSpan(self.lower, upper)

    def setSpan(self, lower, upper):
        low = min(self.maximum(), max(self.minimum(), min(lower, upper)))
        upp = min(self.maximum(), max(self.minimum(), max(lower, upper)))
        changed = False
        if low != self.lower:
            self.lower = low
            self.lowerPos = low
            changed = True
        if upp != self.upper:
            self.upper = upp
            self.upperPos = upp
            changed = True
        if changed:
            self.spanChanged.emit(self.lower, self.upper)
            self.update()

    def lowerPosition(self):
        return self.lowerPos

    def setLowerPosition(self, lower):
        if self.lowerPos != lower:
            self.lowerPos = lower
            if not self.hasTracking():
                self.update()
            if self.isSliderDown():
                self.lowerPositionChanged.emit(lower)
            if self.hasTracking() and not self.blockTracking:
                main = (self.mainControl == QSpanSlider.LowerHandle)
                self.triggerAction(QSpanSlider.SliderMove, main)

    def upperPosition(self):
        return self.upperPos

    def setUpperPosition(self, upper):
        if self.upperPos != upper:
            self.upperPos = upper
            if not self.hasTracking():
                self.update()
            if self.isSliderDown():
                self.upperPositionChanged.emit(upper)
            if self.hasTracking() and not self.blockTracking:
                main = (self.mainControl == QSpanSlider.UpperHandle)
                self.triggerAction(QSpanSlider.SliderMove, main)

    def gradientLeftColor(self):
        return self.gradientLeft
    
    def setGradientLeftColor(self, color):
        self.gradientLeft = color
        self.update()
    
    def gradientRightColor(self):
        return self.gradientRight
    
    def setGradientRightColor(self, color):
        self.gradientRight = color
        self.update()

    def movePressedHandle(self):
        if self.lastPressed == QSpanSlider.LowerHandle:
            if self.lowerPos != self.lower:
                main = (self.mainControl == QSpanSlider.LowerHandle)
                self.triggerAction(QtGui.QAbstractSlider.SliderMove, main)
        elif self.lastPressed == QSpanSlider.UpperHandle:
            if self.upperPos != self.upper:
                main = (self.mainControl == QSpanSlider.UpperHandle)
                self.triggerAction(QtGui.QAbstractSlider.SliderMove, main)

    def pick(self, p):
        if self.orientation() == QtCore.Qt.Horizontal:
            return p.x()
        else:
            return p.y()
    
    def triggerAction(self, action, main):
        value = 0
        no = False
        up = False
        my_min = self.minimum()
        my_max = self.maximum()
        altControl = QSpanSlider.LowerHandle
        if self.mainControl == QSpanSlider.LowerHandle:
            altControl = QSpanSlider.UpperHandle

        self.blockTracking = True
        
        isUpperHandle = (main and self.mainControl == QSpanSlider.UpperHandle) or (not main and altControl == QSpanSlider.UpperHandle)
        
        if action == QtGui.QAbstractSlider.SliderSingleStepAdd:
            if isUpperHandle:
                value = min(my_max, max(my_min, self.upper + self.singleStep()))
                up = True
            else:
                value = min(my_max, max(my_min, self.lower + self.singleStep()))
        elif action == QtGui.QAbstractSlider.SliderSingleStepSub:
            if isUpperHandle:
                value = min(my_max, max(my_min, self.upper - self.singleStep()))
                up = True
            else:
                value = min(my_max, max(my_min, self.lower - self.singleStep()))
        elif action == QtGui.QAbstractSlider.SliderToMinimum:
            value = my_min
            if isUpperHandle:
                up = True
        elif action == QtGui.QAbstractSlider.SliderToMaximum:
            value = my_max
            if isUpperHandle:
                up = True
        elif action == QtGui.QAbstractSlider.SliderMove:
            if isUpperHandle:
                up = True
            no = True
        elif action == QtGui.QAbstractSlider.SliderNoAction:
            no = True

        if not no and not up:
            # if self.movement == QSpanSlider.NoCrossing:
            #     value = min(value, self.upper)
            # elif self.movement == QSpanSlider.NoOverlapping:
            value = min(value, self.upper)

            # if self.movement == QSpanSlider.FreeMovement and value > self.upper:
            #     self.swapControls()
            #     self.setUpperPosition(value)
            # else:

            self.setLowerPosition(value)

        elif not no:
            # if self.movement == QSpanSlider.NoCrossing:
            # value = max(value, self.lower)
            # elif self.movement == QSpanSlider.NoOverlapping:
            value = max(value, self.lower)

            # if self.movement == QSpanSlider.FreeMovement and value < self.lower:
            #     self.swapControls()
            #     self.setLowerPosition(value)
            # else:
            self.setUpperPosition(value)

        self.blockTracking = False
        self.setLowerValue(self.lowerPos)
        self.setUpperValue(self.upperPos)

    def paintEvent(self, event):
        painter = QtGui.QStylePainter(self)
        
        # ticks
        opt = QtGui.QStyleOptionSlider()
        self.initStyleOption(opt)
        # opt.subControls = QtGui.QStyle.SC_SliderTickmarks
        painter.drawComplexControl(QtGui.QStyle.CC_Slider, opt)

        # groove
        opt.sliderPosition = 20
        opt.sliderValue = 0
        opt.subControls = QtGui.QStyle.SC_SliderGroove
        painter.drawComplexControl(QtGui.QStyle.CC_Slider, opt)

        # handle rects
        opt.sliderPosition = self.lowerPos
        lr = self.style().subControlRect(QtGui.QStyle.CC_Slider, opt, QtGui.QStyle.SC_SliderHandle, self)
        lrv  = self.pick(lr.center())
        opt.sliderPosition = self.upperPos
        ur = self.style().subControlRect(QtGui.QStyle.CC_Slider, opt, QtGui.QStyle.SC_SliderHandle, self)
        urv  = self.pick(ur.center())

        # span
        minv = min(lrv, urv)
        maxv = max(lrv, urv)
        c = self.style().subControlRect(QtGui.QStyle.CC_Slider, opt, QtGui.QStyle.SC_SliderGroove, self).center()
        spanRect = QtCore.QRect(QtCore.QPoint(c.x() - 2, minv), QtCore.QPoint(c.x() + 1, maxv))
        if self.orientation() == QtCore.Qt.Horizontal:
            spanRect = QtCore.QRect(QtCore.QPoint(minv, c.y() - 2), QtCore.QPoint(maxv, c.y() + 1))
        self.drawSpan(painter, spanRect)

        # handles
        if self.lastPressed == QSpanSlider.LowerHandle:
            self.drawHandle(painter, QSpanSlider.UpperHandle)
            self.drawHandle(painter, QSpanSlider.LowerHandle)
        else:
            self.drawHandle(painter, QSpanSlider.LowerHandle)
            self.drawHandle(painter, QSpanSlider.UpperHandle)
    
    def setupPainter(self, painter, orientation, x1, y1, x2, y2):
        highlight = self.palette().color(QtGui.QPalette.Highlight)
        gradient = QtGui.QLinearGradient(x1, y1, x2, y2)
        gradient.setColorAt(0, highlight.light(108))
        gradient.setColorAt(1, highlight.light(108))
        painter.setBrush(gradient)

        if orientation == QtCore.Qt.Horizontal:
            painter.setPen(QtGui.QPen(highlight.dark(130), 0))
        else:
            painter.setPen(QtGui.QPen(highlight.dark(150), 0))

    def drawSpan(self, painter, rect):
        opt = QtGui.QStyleOptionSlider()
        QtGui.QSlider.initStyleOption(self, opt)

        # area
        groove = self.style().subControlRect(QtGui.QStyle.CC_Slider, opt, QtGui.QStyle.SC_SliderGroove, self)
        if opt.orientation == QtCore.Qt.Horizontal:
            groove.adjust(0, 0, -1, 0);
        else:
            groove.adjust(0, 0, 0, -1);

        # pen & brush
        painter.setPen(QtGui.QPen(self.gradientLeft, 0))
        if opt.orientation == QtCore.Qt.Horizontal:
            self.setupPainter(painter, opt.orientation, groove.center().x(), groove.top(), groove.center().x(), groove.bottom())
        else:
            self.setupPainter(painter, opt.orientation, groove.left(), groove.center().y(), groove.right(), groove.center().y())

        # draw groove
        intersected = QtCore.QRectF(rect.intersected(groove))
        gradient = QtGui.QLinearGradient(intersected.topLeft(), intersected.topRight())
        gradient.setColorAt(0, self.gradientLeft)
        gradient.setColorAt(1, self.gradientRight)
        painter.fillRect(intersected, gradient)
    
    def drawHandle(self, painter, handle):
        opt = QtGui.QStyleOptionSlider()
        self._initStyleOption(opt, handle)
        opt.subControls = QtGui.QStyle.SC_SliderHandle

        # if handle == QSpanSlider.LowerHandle:
        #     print "LowerHandle (",self.lowerPressed,")"
        # elif handle == QSpanSlider.UpperHandle:
        #     print "UpperHandle (",self.upperPressed,")"
        # else:
        #     print "NoHandle"

        pressed = self.upperPressed
        if handle == QSpanSlider.LowerHandle:
            pressed = self.lowerPressed
        
        if pressed == QtGui.QStyle.SC_SliderHandle:
            opt.activeSubControls = pressed
            opt.state |= QtGui.QStyle.State_Sunken
        painter.drawComplexControl(QtGui.QStyle.CC_Slider, opt)
    
    def _initStyleOption(self, option, handle):
        self.initStyleOption(option)

        option.sliderPosition = self.lowerPos
        if handle == QSpanSlider.UpperHandle:
            option.sliderPosition = self.upperPos

        option.sliderValue = self.lower
        if handle == QSpanSlider.UpperHandle:
            option.sliderValue = self.upper
    
    def handleMousePress(self, pos, control, value, handle):
        opt = QtGui.QStyleOptionSlider()

        self._initStyleOption(opt, handle)
        oldControl = control
        control = self.style().hitTestComplexControl(QtGui.QStyle.CC_Slider, opt, pos, self)
        sr = self.style().subControlRect(QtGui.QStyle.CC_Slider, opt, QtGui.QStyle.SC_SliderHandle, self)
        if control == QtGui.QStyle.SC_SliderHandle:
            self.position = value
            self.offset = self.pick(pos - sr.topLeft())
            self.lastPressed = handle
            self.setSliderDown(True)
            # self.sliderPressed.emit(handle)
            self.emit(QtCore.SIGNAL("sliderPressed(PyQt_PyObject)"), handle)
        if control != oldControl:
            self.update(sr)
        return control
    
    def mousePressEvent(self, event):
        if self.minimum() == self.maximum() or event.buttons() ^ event.button():
            event.ignore()
            return

        self.lowerPressed = self.handleMousePress(event.pos(), self.lowerPressed, self.lower, QSpanSlider.LowerHandle)
        self.upperPressed = self.handleMousePress(event.pos(), self.upperPressed, self.upper, QSpanSlider.UpperHandle)

        self.firstMovement = True
        event.accept()
    
    def mouseMoveEvent(self, event):
        if self.lowerPressed != QtGui.QStyle.SC_SliderHandle and self.upperPressed != QtGui.QStyle.SC_SliderHandle:
            event.ignore()
            return

        opt = QtGui.QStyleOptionSlider()
        self.initStyleOption(opt)
        m = self.style().pixelMetric(QtGui.QStyle.PM_MaximumDragDistance, opt, self)
        newPosition = self.pixelPosToRangeValue(self.pick(event.pos()) - self.offset)
        if m >= 0:
            r = self.rect().adjusted(-m, -m, m, m)
            if not r.contains(event.pos()):
                newPosition = self.position

        # pick the preferred handle on the first movement
        if self.firstMovement:
            # if self.lower == self.upper:
            #     if newPosition < self.lowerValue():
            #         self.swapControls()
            #         self.firstMovement = False
            # else:
            self.firstMovement = False

        if self.lowerPressed == QtGui.QStyle.SC_SliderHandle:
            newPosition = min(newPosition, self.upper)
            self.setLowerPosition(newPosition)
        elif self.upperPressed == QtGui.QStyle.SC_SliderHandle:
            newPosition = max(newPosition, self.lower);
            self.setUpperPosition(newPosition)
        event.accept()
    
    def mouseReleaseEvent(self, event):
        QtGui.QSlider.mouseReleaseEvent(self, event)
        self.setSliderDown(False)
        self.lowerPressed = QtGui.QStyle.SC_None
        self.upperPressed = QtGui.QStyle.SC_None
        self.update()
    
    def pixelPosToRangeValue(self, pos):
        opt = QtGui.QStyleOptionSlider()
        self.initStyleOption(opt)

        sliderMin = 0
        sliderMax = 0
        sliderLength = 0
        gr = self.style().subControlRect(QtGui.QStyle.CC_Slider, opt, QtGui.QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QtGui.QStyle.CC_Slider, opt, QtGui.QStyle.SC_SliderHandle, self)
        if self.orientation() == QtCore.Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1
        
        return QtGui.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), pos - sliderMin, sliderMax - sliderMin, opt.upsideDown)

    # lowerValue = QtCore.pyqtProperty("int", lowerValue, setLowerValue)
    # upperValue = QtCore.pyqtProperty("int", upperValue, setUpperValue)
    upperPosition = QtCore.pyqtProperty("int", upperPosition, setUpperPosition)
    lowerPosition = QtCore.pyqtProperty("int", lowerPosition, setLowerPosition)
