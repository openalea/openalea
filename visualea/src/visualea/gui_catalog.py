# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2008 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
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


from PyQt4 import QtCore, QtGui
from openalea.core.interface import * #IGNORE:W0614,W0401
from openalea.core.observer import lock_notify         

def isiterable(seq):
    try:
        iter(seq)
        return True
    except TypeError:
        return False
    return False

class IFloatWidget(IInterfaceWidget, QtGui.QWidget):
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
        QtGui.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)
        
        hboxlayout = QtGui.QHBoxLayout(self)
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)

        self.label = QtGui.QLabel(self)
        self.label.setText(node.get_input_port(name=parameter_str).get_label())
        hboxlayout.addWidget(self.label)

        self.spin = QtGui.QDoubleSpinBox (self)
        self.spin.setRange(interface.min, interface.max)
        self.spin.setSingleStep(interface.step)
        
        hboxlayout.addWidget(self.spin)

        self.notify(None, None)
        
        self.connect(self.spin, QtCore.SIGNAL("valueChanged(double)"), \
                     self.valueChanged)

    @lock_notify      
    def valueChanged(self, newval):
        """ todo """
        self.node.set_input(self.param_str, newval)

    def notify(self, sender, event):
        """ Notification sent by node """
        try:
            v = float(self.node.get_input(self.param_str))
        except:
            v = 0.
            #print "FLOAT SPIN : cannot set value : ", \
            #    self.node.get_input(self.param_str)
            
        self.spin.setValue(v)
        


class IIntWidget(IInterfaceWidget, QtGui.QWidget):
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
        QtGui.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        hboxlayout = QtGui.QHBoxLayout(self)
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)


        self.label = QtGui.QLabel(self)
        self.label.setText(node.get_input_port(name=parameter_str).get_label())
        hboxlayout.addWidget(self.label)

        self.spin = QtGui.QSpinBox (self)
        self.spin.setRange(interface.min, interface.max)
        self.spin.setSingleStep(interface.step)
        
        hboxlayout.addWidget(self.spin)

        self.notify(None, None)

        self.connect(self.spin, QtCore.SIGNAL("valueChanged(int)"), self.valueChanged)


    @lock_notify      
    def valueChanged(self, newval):
        self.node.set_input(self.param_str, newval)
        
        
    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            v = int(self.node.get_input(self.param_str))
        except:
            v = 0
            #print "INT SPIN : cannot set value : ", self.node.get_input(self.param_str)

        self.spin.setValue(v)



class IBoolWidget(IInterfaceWidget, QtGui.QWidget):
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
        
        QtGui.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        hboxlayout = QtGui.QHBoxLayout(self)
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)

        self.checkbox = QtGui.QCheckBox (parameter_str, self)

        hboxlayout.addWidget(self.checkbox)

        self.notify(node, None)
        self.connect(self.checkbox, QtCore.SIGNAL("stateChanged(int)"), self.stateChanged)


    @lock_notify      
    def stateChanged(self, state):

        if(state == QtCore.Qt.Checked):
            self.node.set_input(self.param_str, True)
        else:
            self.node.set_input(self.param_str, False)
        
        
    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            ischecked = bool(self.node.get_input(self.param_str))
        except:
            ischecked = False

        if(ischecked):
            self.checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkbox.setCheckState(QtCore.Qt.Unchecked)



class IStrWidget(IInterfaceWidget, QtGui.QWidget):
    """
    Line Edit widget
    """

    __interface__ = IStr
    __metaclass__ = make_metaclass()

    MAX_LEN = 100000

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtGui.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtGui.QHBoxLayout(self)

        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)


        self.label = QtGui.QLabel(self)
        self.label.setText(node.get_input_port(name=parameter_str).get_label())
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QLineEdit (self)
        self.hboxlayout.addWidget(self.subwidget)
        
        self.too_long = False # Validity Flag
        self.notify(None, None)
        self.connect(self.subwidget, QtCore.SIGNAL("textChanged(QString)"), self.valueChanged)


    @lock_notify      
    def valueChanged(self, newval):

        if(not self.too_long):
            self.node.set_input(self.param_str, str(newval))
        
        
    def notify(self, sender, event):
        """ Notification sent by node """
        
        s = str(self.node.get_input(self.param_str))

        if(len(s) > self.MAX_LEN) : 
            s = "String too long..."
            self.too_long = True
        else:
            self.too_long = False

        self.subwidget.setText(s)
        


class IDateTimeWidget(IInterfaceWidget, QtGui.QWidget):
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

        QtGui.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtGui.QHBoxLayout(self)

        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)


        self.label = QtGui.QLabel(self)
        self.label.setText(node.get_input_port(name=parameter_str).get_label())
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QDateTimeEdit(self)
        self.hboxlayout.addWidget(self.subwidget)

        try:
            self.subwidget.setDateTime(self.node.get_input(self.param_str))
        except:
            pass

        self.connect(self.subwidget, QtCore.SIGNAL
                     ("dateTimeChanged( const QDateTime & datetime )"), self.valueChanged)


    @lock_notify      
    def valueChanged(self, newval):
        d = newval.toPyDateTime()
        self.node.set_input(self.param_str, d)
        
        
    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            self.subwidget.setDateTime(self.node.get_input(self.param_str))
        except:
            pass



class ITextStrWidget(IInterfaceWidget, QtGui.QWidget):
    """
    Multi-Line Edit widget
    """

    __interface__ = ITextStr
    __metaclass__ = make_metaclass()
    MAX_LEN = 1000000

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtGui.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtGui.QHBoxLayout(self)

        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)


        self.label = QtGui.QLabel(self)
        self.label.setText(node.get_input_port(name=parameter_str).get_label())
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QTextEdit (self)
        self.hboxlayout.addWidget(self.subwidget)

        self.too_long = False # Validity Flag
        self.notify(None, None)

        self.connect(self.subwidget, QtCore.SIGNAL("textChanged()"), self.valueChanged)


    def setEnabled(self, val):
        self.subwidget.setReadOnly(not bool(val))
        

    @lock_notify      
    def valueChanged(self):

        if(not self.too_long):
            self.node.set_input(self.param_str, str(self.subwidget.toPlainText()))
            
        
    def notify(self, sender, event):
        """ Notification sent by node """
        
        s = str(self.node.get_input(self.param_str))

        if(len(s) > self.MAX_LEN) : 
            s = "String too long..."
            self.too_long = True
        else:
            self.too_long = False

        self.subwidget.setText(s)
       



class ISequenceWidget(IInterfaceWidget, QtGui.QWidget):
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

        QtGui.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.gridlayout = QtGui.QGridLayout(self)
        self.gridlayout.setMargin(3)
        self.gridlayout.setSpacing(5)

        self.button = QtGui.QPushButton("Add Item", self)
        self.gridlayout.addWidget(self.button,2,0,1,2)

        self.buttonplus = QtGui.QPushButton(" + ", self)
        self.gridlayout.addWidget(self.buttonplus,3,1,1,1)

        self.buttonmoins = QtGui.QPushButton(" - ", self)
        self.gridlayout.addWidget(self.buttonmoins,3,0,1,1)

        self.label = QtGui.QLabel(self)
        self.label.setText(node.get_input_port(name=parameter_str).get_label())
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.subwidget = QtGui.QListWidget (self)
        self.gridlayout.addWidget(self.subwidget,1,0,1,2)

        self.connect(self.subwidget, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"),
                     self.itemclick)
        self.connect(self.subwidget, QtCore.SIGNAL("itemChanged(QListWidgetItem*)"),
                     self.itemchanged)
        self.connect(self.button, QtCore.SIGNAL("clicked()"), self.button_clicked)
        self.connect(self.buttonplus, QtCore.SIGNAL("clicked()"), self.buttonplus_clicked)
        self.connect(self.buttonmoins, QtCore.SIGNAL("clicked()"), self.buttonmoins_clicked)

        self.updating = False # itemchanged protection
        self.update_list()


    def update_state(self):
        """ Enable or disable widget depending of its state """
        
        # do not call itemchanged
        self.updating = True

        state = self.node.get_input_state(self.param_str)
        
        self.connected = (state == "connected")
        self.buttonplus.setVisible(not self.connected)
        self.buttonmoins.setVisible(not self.connected)
        self.button.setVisible(not self.connected)

        for i in range(self.subwidget.count()):
            item = self.subwidget.item(i)
            if(self.connected):
                item.setFlags(QtCore.Qt.ItemIsSelectable)
            else:
                item.setFlags(QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled|
                              QtCore.Qt.ItemIsSelectable)
        self.updating = False


    def notify(self, sender, event):
        """ Notification sent by node """
        self.update_list()


    @lock_notify
    def update_list(self):
        """ Rebuild the list """
        seq = self.node.get_input(self.param_str)
        
        # do not call itemchanged
        self.updating = True

        self.subwidget.clear()

        if not isiterable(seq): return
        for elt in seq :
            item = QtGui.QListWidgetItem(str(elt))
            item.setFlags(QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled|
                          QtCore.Qt.ItemIsSelectable)
            self.subwidget.addItem(item)
        self.updating = False

            
    @lock_notify      
    def button_clicked(self):
        seq = self.node.get_input(self.param_str)
        seq.append(None)
        item = QtGui.QListWidgetItem(str(None))
        item.setFlags(QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled|
                      QtCore.Qt.ItemIsSelectable)
        self.subwidget.addItem(item)
        self.node.unvalidate_input(self.param_str)    


    @lock_notify      
    def buttonplus_clicked(self):
        seq = self.node.get_input(self.param_str)
        row = self.subwidget.currentRow()
        if(row<0): return
        val = seq[row]
        del(seq[row])
        row = (row + 1) % (len(seq) + 1)
        seq.insert(row, val)
        self.update_list()
        self.subwidget.setCurrentRow(row)
        self.node.unvalidate_input(self.param_str)
        
        
    @lock_notify      
    def buttonmoins_clicked(self):
        seq = self.node.get_input(self.param_str)
        row = self.subwidget.currentRow ()
        if(row<0): return
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
        self.node.unvalidate_input(self.param_str)
        

    def itemclick(self, item):
        self.subwidget.editItem(item)


    @lock_notify      
    def itemchanged(self, item):
        if(self.updating) : return

        text = item.text()
        i = self.subwidget.currentRow()
        seq = self.node.get_input(self.param_str)
        
        try:
            obj = eval(str(text))
            seq[i] = obj
            item.setText(str(obj))
        except :
            item.setText(text)
            seq[i] = str(text)

        self.node.unvalidate_input(self.param_str)
        
        
            
    @lock_notify      
    def keyPressEvent(self, e):
        if(self.connected): return
        key = e.key()
        seq = self.node.get_input(self.param_str)
        if( key == QtCore.Qt.Key_Delete):
            selectlist = self.subwidget.selectedItems()
            for i in selectlist:
                row = self.subwidget.row(i)
                del(seq[row])
                self.subwidget.takeItem(row)

        self.node.unvalidate_input(self.param_str)    




class IDictWidget(IInterfaceWidget, QtGui.QWidget):
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
        
        QtGui.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtGui.QVBoxLayout(self)

        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)

        self.label = QtGui.QLabel(self)
        self.label.setText(node.get_input_port(name=parameter_str).get_label())
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QListWidget (self)
        self.hboxlayout.addWidget(self.subwidget)

        self.button = QtGui.QPushButton("Add Item", self)
        self.hboxlayout.addWidget(self.button)

        self.update_list()
        self.connect(self.subwidget, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"),
                     self.itemclick)
        self.connect(self.button, QtCore.SIGNAL("clicked()"), self.button_clicked)


    def update_state(self):
        """ Enable or disable widget depending of its state """
        
        state = self.node.get_input_state(self.param_str)
        
        self.connected = (state == "connected")
        self.button.setVisible(not self.connected)

        for i in range(self.subwidget.count()):
            item = self.subwidget.item(i)
            if(self.connected):
                item.setFlags(QtCore.Qt.ItemIsSelectable)
            else:
                item.setFlags(QtCore.Qt.ItemIsEnabled|
                              QtCore.Qt.ItemIsSelectable)


    def notify(self, sender, event):
        """ Notification sent by node """
        self.update_list()


    def update_list(self):
        """ Rebuild the list """
        dic = self.node.get_input(self.param_str)
        self.subwidget.clear()
        self.rowkey = []
    
        try:
            keys = dic.keys()
            keys.sort()
            for key in keys:
                elt = dic[key]
                item = QtGui.QListWidgetItem("%s : %s"%(str(key), str(elt)))
                item.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
                self.subwidget.addItem(item)
                self.rowkey.append(key)
        except Exception, e:
            print e


    @lock_notify      
    def button_clicked(self):
        """ Add add an element in the dictionary """
        dic = self.node.get_input(self.param_str)
        (text, ok) = QtGui.QInputDialog.getText(self, "Key", "Key", )
        if (not ok or text.isEmpty()):
            return

        try:
            key = eval(str(text))
        except:
            key = str(text)

        dic[key] = None
        self.node.unvalidate_input(self.param_str)
        self.update_list()

        
    @lock_notify      
    def itemclick(self, item):
        if(self.connected): return
        text = item.text()
        i = self.subwidget.currentRow()
        dic = self.node.get_input(self.param_str)
        key = self.rowkey[i]

        (text, ok) = QtGui.QInputDialog.getText(self, "Value", "Value")
        if (not ok or text.isEmpty()):
            return

        try:
            obj = eval(str(text))
            dic[key] = obj
            item.setText("%s : %s"%(str(key), str(obj)))
        except :
            item.setText(text)
            dic[key] = str(text)
            item.setText("%s : %s"%(str(key), str(text)))

        self.node.unvalidate_input(self.param_str)

        
    @lock_notify      
    def keyPressEvent(self, e):
        if(self.connected): return
        key   = e.key()
        seq = self.node.get_input(self.param_str)

        # Delete Row
        if( key == QtCore.Qt.Key_Delete):
            selectlist = self.subwidget.selectedItems()
            for i in selectlist:
                row = self.subwidget.row(i)
                key = self.rowkey[row]
                del(seq[key])
                del(self.rowkey[row])
                self.subwidget.takeItem(row)

            self.node.unvalidate_input(self.param_str)


        
class IFileStrWidget(IStrWidget):
    """
    File name Line Edit Widget
    """

    __interface__ = IFileStr
    __metaclass__ = make_metaclass()
    
    last_result = QtCore.QDir.homePath()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IStrWidget.__init__(self, node, parent, parameter_str, interface)

        
        self.button = QtGui.QPushButton("...", self)
        self.checkbox = QtGui.QCheckBox("Save", self)
        self.hboxlayout.addWidget(self.button)
        self.hboxlayout.addWidget(self.checkbox)
        self.filter = interface.filter
        self.open = not interface.save
        #self.open = False

        self.connect(self.button, QtCore.SIGNAL("clicked()"), self.button_clicked)


    def button_clicked(self):

        
        if(not self.open or self.checkbox.checkState()== QtCore.Qt.Checked):
            result = QtGui.QFileDialog.getSaveFileName(self, "Select File",
                                                       self.last_result, self.filter)

        else:
            result = QtGui.QFileDialog.getOpenFileName(self, "Select File",
                                                       self.last_result, self.filter)
    
        if(result):
            self.node.set_input(self.param_str, str(result))
            IFileStrWidget.last_result = result


class IDirStrWidget(IStrWidget):
    """
    File name Line Edit Widget
    """

    __interface__ = IDirStr
    __metaclass__ = make_metaclass()

    last_result = QtCore.QDir.homePath()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IStrWidget.__init__(self, node, parent, parameter_str, interface)

        
        self.button = QtGui.QPushButton("...", self)
        self.hboxlayout.addWidget(self.button)

        self.connect(self.button, QtCore.SIGNAL("clicked()"), self.button_clicked)


    def button_clicked(self):
        
        result = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", self.last_result)
    
        if(result):
            self.node.set_input(self.param_str, str(result))
            IDirStrWidget.last_result = result



        
class IEnumStrWidget(IInterfaceWidget, QtGui.QWidget):
    """ String Enumeration widget """

    __interface__ = IEnumStr
    __metaclass__ = make_metaclass()

    
    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtGui.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)
                
        self.hboxlayout = QtGui.QHBoxLayout(self)
        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)

        self.label = QtGui.QLabel(self)
        self.label.setText(node.get_input_port(name=parameter_str).get_label())
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QComboBox(self)

        # map between string and combobox index
        self.map_index = {}
        for s in  interface.enum:
            self.subwidget.addItem(s)
            self.map_index[s] = self.subwidget.count() - 1

        self.hboxlayout.addWidget(self.subwidget)
        self.notify(None, None)

        self.connect(self.subwidget,
                     QtCore.SIGNAL("currentIndexChanged(QString)"),
                     self.valueChanged)


        

    @lock_notify      
    def valueChanged(self, newval):
        self.node.set_input(self.param_str, str(newval))
        
        
    def notify(self, sender, event):
        """ Notification sent by node """

        strvalue = str(self.node.get_input(self.param_str))
        try:
            index = self.map_index[strvalue]
        except :
            index = -1

        self.subwidget.setCurrentIndex(index)



class IRGBColorWidget(IInterfaceWidget, QtGui.QWidget):
    """ RGB Color Widget """

    __interface__ = IRGBColor
    __metaclass__ = make_metaclass()

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        QtGui.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtGui.QHBoxLayout(self)
        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)

        self.label = QtGui.QLabel(self)
        self.label.setText(node.get_input_port(name=parameter_str).get_label())
        self.hboxlayout.addWidget(self.label)

        self.colorwidget = QtGui.QWidget(self)
        self.colorwidget.setAutoFillBackground(True)

        self.colorwidget.setMinimumSize(QtCore.QSize(50,50))
        self.colorwidget.setBackgroundRole(QtGui.QPalette.Window)
        self.colorwidget.mouseDoubleClickEvent = self.widget_clicked
        self.notify(node, None)
    
        self.hboxlayout.addWidget(self.colorwidget)


    def widget_clicked(self,event):
        
        try:
            (r,g,b) = self.node.get_input(self.param_str)
            oldcolor = QtGui.QColor(r,g,b)
        except:
            oldcolor = QtGui.QColor(0,0,0)                                    
        
        color = QtGui.QColorDialog.getColor(oldcolor, self)
    
        if(color):
            self.node.set_input(self.param_str, (color.red(), color.green(), color.blue()))


    @lock_notify
    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            (r,g,b) = self.node.get_input(self.param_str)
        except:
            (r,g,b) = (0,0,0)
            self.node.set_input(self.param_str, (r,g,b))
        
        palette = self.colorwidget.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(r,g,b))
        self.colorwidget.setPalette(palette)
        self.colorwidget.update()
        

class ITupleWidget(IInterfaceWidget, QtGui.QWidget):
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

        QtGui.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtGui.QHBoxLayout(self)

        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)


        self.label = QtGui.QLabel(self)
        self.label.setText(node.get_input_port(name=parameter_str).get_label())
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QLineEdit (self)
        self.hboxlayout.addWidget(self.subwidget)
        
        self.notify(None, None)
        self.connect(self.subwidget, QtCore.SIGNAL("textChanged(QString)"), self.valueChanged)


    @lock_notify      
    def valueChanged(self, newval):
        try:
            self.node.set_input(self.param_str, eval(str(newval)))
        except:
            pass
        
    def notify(self, sender, event):
        """ Notification sent by node """
        
        s = str(self.node.get_input(self.param_str))
        self.subwidget.setText(s)
