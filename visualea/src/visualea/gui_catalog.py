# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2008 INRIA - CIRAD - INRA
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       File contributor(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

"""Catalog of InterfaceWidgets"""

__license__ = "CeCILL V2"
__revision__ = " $Id$"

from Qt import QtCore, QtGui, QtWidgets

from openalea.core.interface import *  # IGNORE:W0614,W0401
from openalea.core.observer import lock_notify

def isiterable(seq):
    try:
        iter(seq)
        return True
    except TypeError:
        return False
    return False


class IFloatWidget(IInterfaceWidget, QtWidgets.QWidget):

    """
    Float spin box widget
    """

    # Corresponding Interface & Metaclass
    __interface__ = IFloat
    __metaclass__ = make_metaclass()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """
        QtWidgets.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        hboxlayout = QtWidgets.QHBoxLayout(self)
        hboxlayout.setContentsMargins(3, 3, 3, 3)
        hboxlayout.setSpacing(5)

        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.get_label(node, parameter_str))
        hboxlayout.addWidget(self.label)

        self.spin = QtWidgets.QDoubleSpinBox(self)
        self.set_interface(interface)

        hboxlayout.addWidget(self.spin)

        self.notify(None, None)

        self.spin.valueChanged[float].connect(self.valueChanged)

    @lock_notify
    def valueChanged(self, newval):
        """ todo """
        self.set_value(newval)

    def notify(self, sender, event):
        """ Notification sent by node """
        print 'not', sender, event
        try:
            v = float(self.get_value())
        except:
            v = 0.
            # print "FLOAT SPIN : cannot set value : ", \
            #    self.node.get_input(self.param_str)

        self.set_widget_value(v)

    def set_interface(self, interface):
        self.spin.setRange(interface.min, interface.max)
        self.spin.setSingleStep(interface.step)

    def set_widget_value(self, newval):
        self.spin.setValue(newval)

    def get_widget_value(self):
        return self.spin.value()


class IIntWidget(IInterfaceWidget, QtWidgets.QWidget):

    """
    integer spin box widget
    """

    __interface__ = IInt
    __metaclass__ = make_metaclass()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """
        QtWidgets.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        hboxlayout = QtWidgets.QHBoxLayout(self)
        hboxlayout.setContentsMargins(3, 3, 3, 3)
        hboxlayout.setSpacing(5)

        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.get_label(node, parameter_str))
        hboxlayout.addWidget(self.label)

        self.spin = QtWidgets.QSpinBox(self)
        self.spin.setRange(interface.min, interface.max)
        self.spin.setSingleStep(interface.step)

        hboxlayout.addWidget(self.spin)

        self.notify(None, None)

        self.spin.valueChanged[int].connect(self.valueChanged)

    @lock_notify
    def valueChanged(self, newval):
        self.set_value(newval)

    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            v = int(self.get_value())
        except:
            v = 0
            # print "INT SPIN : cannot set value : ", self.node.get_input(self.param_str)

        self.spin.setValue(v)


class IBoolWidget(IInterfaceWidget, QtWidgets.QWidget):

    """
    integer spin box widget
    """

    __interface__ = IBool
    __metaclass__ = make_metaclass()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtWidgets.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        hboxlayout = QtWidgets.QHBoxLayout(self)
        hboxlayout.setContentsMargins(3, 3, 3, 3)
        hboxlayout.setSpacing(5)

        self.checkbox = QtWidgets.QCheckBox(parameter_str, self)

        hboxlayout.addWidget(self.checkbox)

        self.notify(node, None)

        self.checkbox.stateChanged[int].connect(self.stateChanged)

    @lock_notify
    def stateChanged(self, state):

        if(state == QtCore.Qt.Checked):
            self.set_value(True)
        else:
            self.set_value(False)

    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            ischecked = bool(self.get_value())
        except:
            ischecked = False

        if(ischecked):
            self.checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkbox.setCheckState(QtCore.Qt.Unchecked)


class IStrWidget(IInterfaceWidget, QtWidgets.QWidget):

    """
    Line Edit widget
    """

    __interface__ = IStr
    __metaclass__ = make_metaclass()
    __widgetclass__ = QtWidgets.QTextEdit  # QtWidgets.QLineEdit#

    MAX_LEN = 100000

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtWidgets.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtWidgets.QHBoxLayout(self)

        self.hboxlayout.setContentsMargins(3, 3, 3, 3)
        self.hboxlayout.setSpacing(5)

        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.get_label(node, parameter_str))
        self.hboxlayout.addWidget(self.label)

        self.subwidget = self.__widgetclass__()
        self.hboxlayout.addWidget(self.subwidget)

        self.too_long = False  # Validity Flag

        self.subwidget.textChanged.connect(self.valueChanged)
        self.notify(None, None)

    @lock_notify
    def valueChanged(self):
        if(not self.too_long):
            self.set_value(self.get_widget_value())

    def notify(self, sender, event):
        """ Notification sent by node """

        s = str(self.get_value())

        if(len(s) > self.MAX_LEN):
            s = "String too long..."
            self.too_long = True
        else:
            self.too_long = False

        self.set_widget_value(s)

    def get_widget_value(self):
        if isinstance(self.subwidget, QtWidgets.QTextEdit):
            return self.subwidget.toPlainText()
        elif isinstance(self.subwidget, QtWidgets.QLineEdit):
            return self.subwidget.text()
        else:
            raise NotImplementedError

    def set_widget_value(self, newval):
        if isinstance(self.subwidget, (QtWidgets.QTextEdit, QtWidgets.QLineEdit)):
            self.subwidget.setText(newval)
        else:
            raise NotImplementedError


class IDateTimeWidget(IInterfaceWidget, QtWidgets.QWidget):

    """
    Date widget
    """

    __interface__ = IDateTime
    __metaclass__ = make_metaclass()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtWidgets.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtWidgets.QHBoxLayout(self)

        self.hboxlayout.setContentsMargins(3, 3, 3, 3)
        self.hboxlayout.setSpacing(5)

        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.get_label(node, parameter_str))
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtWidgets.QDateTimeEdit(self)
        self.hboxlayout.addWidget(self.subwidget)

        try:
            self.subwidget.setDateTime(self.get_value())
        except:
            pass

        self.subwidget.dateTimeChanged.connect(self.valueChanged)

    @lock_notify
    def valueChanged(self, newval):
        d = newval.toPyDateTime()
        print self.param_str, d
        self.set_value(d)

    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            self.subwidget.setDateTime(self.get_value())
        except:
            pass


class ITextStrWidget(IInterfaceWidget, QtWidgets.QWidget):

    """
    Multi-Line Edit widget
    """

    __interface__ = ITextStr
    __metaclass__ = make_metaclass()
    __widgetclass__ = QtWidgets.QTextEdit

    MAX_LEN = 1000000

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtWidgets.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtWidgets.QHBoxLayout(self)

        self.hboxlayout.setContentsMargins(3, 3, 3, 3)
        self.hboxlayout.setSpacing(5)

        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.get_label(node, parameter_str))
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.hboxlayout.addWidget(self.label)

        self.subwidget = self.__widgetclass__()
        self.hboxlayout.addWidget(self.subwidget)

        self.too_long = False  # Validity Flag

        self.subwidget.textChanged.connect(self.valueChanged)

        self.notify(None, None)

    def setEnabled(self, val):
        self.subwidget.setReadOnly(not bool(val))

    @lock_notify
    def valueChanged(self):
        if(not self.too_long):
            self.set_value(str(self.subwidget.toPlainText()))

    def notify(self, sender, event):
        """ Notification sent by node """

        s = str(self.get_value())

        if(len(s) > self.MAX_LEN):
            s = "String too long..."
            self.too_long = True
        else:
            self.too_long = False

        self.subwidget.setText(s)

try:
    from scintilla_editor import ScintillaCodeEditor
except ImportError:
    class ICodeStrWidget(ITextStrWidget):

        __interface__ = ICodeStr

        @lock_notify
        def valueChanged(self):
            self.set_value(str(self.subwidget.text()))

        def notify(self, sender, event):
            """ Notification sent by node """
            s = self.get_value()
            if s is not None:
                s = str(s)
                self.subwidget.setText(s)
else:
    class ICodeStrWidget(ITextStrWidget):

        __interface__ = ICodeStr
        from scintilla_editor import ScintillaCodeEditor
        __widgetclass__ = ScintillaCodeEditor

        @lock_notify
        def valueChanged(self):
            self.set_value(str(self.subwidget.text()))

        def notify(self, sender, event):
            """ Notification sent by node """
            s = self.get_value()
            if s is not None:
                s = str(s)
                self.subwidget.setText(s)


class ISequenceWidget(IInterfaceWidget, QtWidgets.QWidget):

    """
    List edit widget
    """

    __interface__ = ISequence
    __metaclass__ = make_metaclass()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtWidgets.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)
        self.connected = False

        self.gridlayout = QtWidgets.QGridLayout(self)
        self.gridlayout.setContentsMargins(3, 3, 3, 3)
        self.gridlayout.setSpacing(5)

        self.button = QtWidgets.QPushButton("Add Item", self)
        self.gridlayout.addWidget(self.button, 2, 0, 1, 2)

        self.buttonplus = QtWidgets.QPushButton(" + ", self)
        self.gridlayout.addWidget(self.buttonplus, 3, 1, 1, 1)

        self.buttonmoins = QtWidgets.QPushButton(" - ", self)
        self.gridlayout.addWidget(self.buttonmoins, 3, 0, 1, 1)

        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.get_label(node, parameter_str))
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)

        self.subwidget = QtWidgets.QListWidget(self)
        self.gridlayout.addWidget(self.subwidget, 1, 0, 1, 2)

        self.subwidget.itemDoubleClicked.connect(self.itemclick)
        self.subwidget.itemChanged.connect(self.itemchanged)

        self.button.clicked.connect(self.button_clicked)
        self.buttonplus.clicked.connect(self.buttonplus_clicked)
        self.buttonmoins.clicked.connect(self.buttonmoins_clicked)

        p = QtWidgets.QSizePolicy
        self.setSizePolicy(p(p.MinimumExpanding, p.Preferred))
        self.subwidget.setSizePolicy(p(p.MinimumExpanding, p.Preferred))

        self.updating = False  # itemchanged protection
        self.update_list()

    def update_state(self):
        """ Enable or disable widget depending of its state """

        # do not call itemchanged
        self.updating = True

        state = self.get_state()

        self.connected = (state == "connected")
        self.buttonplus.setVisible(not self.connected)
        self.buttonmoins.setVisible(not self.connected)
        self.button.setVisible(not self.connected)

        for i in range(self.subwidget.count()):
            item = self.subwidget.item(i)
            if(self.connected):
                item.setFlags(QtCore.Qt.ItemIsSelectable)
            else:
                item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled |
                              QtCore.Qt.ItemIsSelectable)
        self.updating = False

    def notify(self, sender, event):
        """ Notification sent by node """
        self.update_list()

    @lock_notify
    def update_list(self):
        """ Rebuild the list """
        seq = self.get_value()
        self.set_widget_value(seq)

    def set_widget_value(self, seq):
        # do not call itemchanged
        self.updating = True

        self.subwidget.clear()

        if not isiterable(seq):
            self.updating = False
            self.unvalidate()
            return

        for elt in seq:
            item = QtWidgets.QListWidgetItem(str(elt))
            item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled |
                          QtCore.Qt.ItemIsSelectable)
            self.subwidget.addItem(item)
        self.updating = False
        self.unvalidate()

    def get_widget_value(self):
        return [self.subwidget.item(i).text() for i in range(self.subwidget.count())]

    @lock_notify
    def button_clicked(self):
        seq = self.get_value()
        if seq is None:
            seq = []
        seq.append(None)
        item = QtWidgets.QListWidgetItem(str(None))
        item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled |
                      QtCore.Qt.ItemIsSelectable)
        self.subwidget.addItem(item)
        self.set_value(seq)
        self.unvalidate()

    @lock_notify
    def buttonplus_clicked(self):
        seq = self.get_value()
        row = self.subwidget.currentRow()
        if(row < 0):
            return
        val = seq[row]
        del(seq[row])
        row = (row + 1) % (len(seq) + 1)
        seq.insert(row, val)
        self.update_list()
        self.subwidget.setCurrentRow(row)
        self.unvalidate()

    @lock_notify
    def buttonmoins_clicked(self):
        seq = self.get_value()
        row = self.subwidget.currentRow()
        if(row < 0):
            return
        val = seq[row]
        del(seq[row])
        row -= 1
        if(row < 0):
            row = len(seq)
            seq.append(val)
        else:
            seq.insert(row, val)

        self.update_list()
        self.subwidget.setCurrentRow(row)
        self.unvalidate()

    def itemclick(self, item):
        self.subwidget.editItem(item)

    @lock_notify
    def itemchanged(self, item):
        if(self.updating):
            return

        text = item.text()
        i = self.subwidget.currentRow()
        seq = self.get_value()

        try:
            obj = eval(str(text))
            seq[i] = obj
            item.setText(str(obj))
        except:
            item.setText(text)
            seq[i] = str(text)

        self.unvalidate()

    @lock_notify
    def keyPressEvent(self, e):
        if(self.connected):
            return
        key = e.key()
        seq = self.get_value()
        if(key == QtCore.Qt.Key_Delete):
            selectlist = self.subwidget.selectedItems()
            for i in selectlist:
                row = self.subwidget.row(i)
                del(seq[row])
                self.subwidget.takeItem(row)

        self.unvalidate()


class IDictWidget(IInterfaceWidget, QtWidgets.QWidget):

    """
    List edit widget
    """

    __interface__ = IDict
    __metaclass__ = make_metaclass()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtWidgets.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtWidgets.QVBoxLayout(self)

        self.hboxlayout.setContentsMargins(3, 3, 3, 3)
        self.hboxlayout.setSpacing(5)

        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.get_label(node, parameter_str))
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtWidgets.QListWidget(self)
        self.hboxlayout.addWidget(self.subwidget)

        self.button = QtWidgets.QPushButton("Add Item", self)
        self.hboxlayout.addWidget(self.button)

        self.update_list()
        self.subwidget.itemDoubleClicked.connect(self.itemclick)
        self.button.clicked.connect(self.button_clicked)

    def update_state(self):
        """ Enable or disable widget depending of its state """

        state = self.get_value()

        self.connected = (state == "connected")
        self.button.setVisible(not self.connected)

        for i in range(self.subwidget.count()):
            item = self.subwidget.item(i)
            if(self.connected):
                item.setFlags(QtCore.Qt.ItemIsSelectable)
            else:
                item.setFlags(QtCore.Qt.ItemIsEnabled |
                              QtCore.Qt.ItemIsSelectable)

    def notify(self, sender, event):
        """ Notification sent by node """
        self.update_list()

    def update_list(self):
        """ Rebuild the list """
        dic = self.get_value()
        self.subwidget.clear()
        self.rowkey = []

        try:
            keys = dic.keys()
            keys.sort()
            for key in keys:
                elt = dic[key]
                item = QtWidgets.QListWidgetItem("%s : %s" % (str(key), str(elt)))
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                self.subwidget.addItem(item)
                self.rowkey.append(key)
        except Exception, e:
            print e

    @lock_notify
    def button_clicked(self):
        """ Add add an element in the dictionary """
        dic = self.get_value()
        (text, ok) = QtWidgets.QInputDialog.getText(self, "Key", "Key",)
        if (not ok or len(text) == 0):
            return

        try:
            key = eval(str(text))
        except:
            key = str(text)

        dic[key] = None
        self.unvalidate()
        self.update_list()

    @lock_notify
    def itemclick(self, item):
        if(self.connected):
            return
        text = item.text()
        i = self.subwidget.currentRow()
        dic = self.get_value()
        key = self.rowkey[i]

        (text, ok) = QtWidgets.QInputDialog.getText(self, "Value", "Value")
        if (not ok or len(text) == 0):
            return

        try:
            obj = eval(str(text))
            dic[key] = obj
            item.setText("%s : %s" % (str(key), str(obj)))
        except:
            item.setText(text)
            dic[key] = str(text)
            item.setText("%s : %s" % (str(key), str(text)))

        self.unvalidate()

    @lock_notify
    def keyPressEvent(self, e):
        if(self.connected):
            return
        key = e.key()
        seq = self.get_value()

        # Delete Row
        if(key == QtCore.Qt.Key_Delete):
            selectlist = self.subwidget.selectedItems()
            for i in selectlist:
                row = self.subwidget.row(i)
                key = self.rowkey[row]
                del(seq[key])
                del(self.rowkey[row])
                self.subwidget.takeItem(row)

            self.unvalidate()


class IFileStrWidget(IStrWidget):

    """
    File name Line Edit Widget
    """

    __interface__ = IFileStr
    __metaclass__ = make_metaclass()
    __widgetclass__ = QtWidgets.QLineEdit

    last_result = QtCore.QDir.homePath()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IStrWidget.__init__(self, node, parent, parameter_str, interface)

        self.button = QtWidgets.QPushButton("...", self)
        self.checkbox = QtWidgets.QCheckBox("Save", self)
        self.hboxlayout.addWidget(self.button)
        self.hboxlayout.addWidget(self.checkbox)
        self.filter = interface.filter
        self.open = not interface.save
        # self.open = False

        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):

        if(not self.open or self.checkbox.checkState() == QtCore.Qt.Checked):
            result = QtWidgets.QFileDialog.getSaveFileName(self, "Select File",
                                                          self.last_result, self.filter)

        else:
            result = QtWidgets.QFileDialog.getOpenFileName(self, "Select File",
                                                          self.last_result, self.filter)

        if(result):
            self.set_value(str(result))
            IFileStrWidget.last_result = result


class IDirStrWidget(IStrWidget):

    """
    File name Line Edit Widget
    """

    __interface__ = IDirStr
    __metaclass__ = make_metaclass()
    __widgetclass__ = QtWidgets.QLineEdit

    last_result = QtCore.QDir.homePath()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IStrWidget.__init__(self, node, parent, parameter_str, interface)

        self.button = QtWidgets.QPushButton("...", self)
        self.hboxlayout.addWidget(self.button)

        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):

        result = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", self.last_result)

        if(result):
            self.set_value(str(result))
            IDirStrWidget.last_result = result


class IEnumStrWidget(IInterfaceWidget, QtWidgets.QWidget):

    """ String Enumeration widget """

    __interface__ = IEnumStr
    __metaclass__ = make_metaclass()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtWidgets.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtWidgets.QHBoxLayout(self)
        self.hboxlayout.setContentsMargins(3, 3, 3, 3)
        self.hboxlayout.setSpacing(5)

        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.get_label(node, parameter_str))
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtWidgets.QComboBox(self)

        # map between string and combobox index
        self.set_interface(interface)

        self.hboxlayout.addWidget(self.subwidget)
        self.notify(None, None)

        self.subwidget.currentIndexChanged[str].connect(self.valueChanged)

    @lock_notify
    def valueChanged(self, newval):
        self.set_value(str(newval))

    def notify(self, sender, event):
        """ Notification sent by node """

        strvalue = str(self.get_value())
        try:
            index = self.map_index[strvalue]
        except:
            index = -1

        self.subwidget.setCurrentIndex(index)

    def set_interface(self, interface):
        self.map_index = {}
        self.subwidget.clear()
        for s in interface.enum:
            self.subwidget.addItem(s)
            self.map_index[s] = self.subwidget.count() - 1

    def set_widget_value(self, newval):
        if newval in self.map_index:
            self.subwidget.setCurrentIndex(self.map_index[newval])
        else:
            self.subwidget.setCurrentIndex(0)

    def get_widget_value(self):
        return self.subwidget.currentText()


class IRGBColorWidget(IInterfaceWidget, QtWidgets.QWidget):

    """ RGB Color Widget """

    __interface__ = IRGBColor
    __metaclass__ = make_metaclass()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtWidgets.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtWidgets.QHBoxLayout(self)
        self.hboxlayout.setContentsMargins(3, 3, 3, 3)
        self.hboxlayout.setSpacing(5)

        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.get_label(node, parameter_str))
        self.hboxlayout.addWidget(self.label)

        self.colorwidget = QtWidgets.QWidget(self)
        self.colorwidget.setAutoFillBackground(True)

        self.colorwidget.setMinimumSize(QtCore.QSize(50, 50))
        self.colorwidget.setBackgroundRole(QtWidgets.QPalette.Window)
        self.colorwidget.mouseDoubleClickEvent = self.widget_clicked
        self.notify(node, None)

        self.hboxlayout.addWidget(self.colorwidget)

    def widget_clicked(self, event):

        try:
            (r, g, b) = self.get_value()
            oldcolor = QtGui.QColor(r, g, b)
        except:
            oldcolor = QtGui.QColor(0, 0, 0)

        color = QtGui.QColorDialog.getColor(oldcolor, self)

        if(color):
            self.set_value((color.red(), color.green(), color.blue()))

    @lock_notify
    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            (r, g, b) = self.get_value()
        except:
            (r, g, b) = (0, 0, 0)
            self.set_value((r, g, b))

        palette = self.colorwidget.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(r, g, b))
        self.colorwidget.setPalette(palette)
        self.colorwidget.update()

class ITupleWidget(IInterfaceWidget, QtWidgets.QWidget):

    """
    Tuple widget
    """
    # Corresponding Interface & Metaclass
    __interface__ = ITuple
    __metaclass__ = make_metaclass()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtWidgets.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtWidgets.QHBoxLayout(self)

        self.hboxlayout.setContentsMargins(3, 3, 3, 3)
        self.hboxlayout.setSpacing(5)

        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.get_label(node, parameter_str))
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtWidgets.QLineEdit(self)
        self.hboxlayout.addWidget(self.subwidget)

        self.notify(None, None)
        self.subwidget.textChanged.connect(self.valueChanged)

    @lock_notify
    def valueChanged(self, newval):
        try:
            self.set_value(eval(str(newval)))
        except:
            pass

    def notify(self, sender, event):
        """ Notification sent by node """

        s = str(self.get_value())
        self.subwidget.setText(s)
