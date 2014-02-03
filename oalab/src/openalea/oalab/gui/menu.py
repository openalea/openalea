# -*- python -*-
#
#       Main Menu class
# 
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = ""

from openalea.vpltk.qt import QtGui, QtCore

"""
# To generate images
from openalea.lpy.gui.compile_ui import check_rc_generation
check_rc_generation('resources.qrc')
"""

big_btn_size = QtCore.QSize(80,55)
small_btn_size = QtCore.QSize(130,20)
big_icon_size = QtCore.QSize(30,30)
small_icon_size = QtCore.QSize(20,20)


class PanedMenu(QtGui.QTabWidget):
    """
    A widget that tries to mimic menu of Microsoft Office 2010.
    Cf. Ribbon Bar.
    """
    def __init__(self, parent=None):
        super(QtGui.QTabWidget, self).__init__() 
        self.setAccessibleName("Menu")
        self.setMinimumSize(1,120)
        self.setMaximumSize(10000,120)
        self.tab_name = list()
        
    def addSpecialTab(self, label, widget=None):
        widget = Pane()
        self.tab_name.append(label)
        self.addTab(widget, label)

    def addBtns(self, pane_names, group_names, btn_names, btn_icons, btn_types):
        #TODO
        pass
           
    def addBtn(self, pane_name, group_name, btn_name, btn_icon, btn_type=0):
        """
        :param pane_name: name of pane. type:String.
        :param group_name: name of group inside the pane. type:String.
        :param btn_name: name of button inside the group. type:String.
        :param btn_icon: icon of button. type:QtGui.QIcon.
        :param btn_type: type of button to add. 0 = Big Button. 1 = Small Button. type: Int. Default=0.
        :return: created button. type:QToolButton
        """
        # Check if pane exist, else create it
        if pane_name not in self.tab_name:
            self.addSpecialTab(pane_name)  
        # Get Pane
        index = self.tab_name.index(pane_name)
        pane = self.widget(index)
        # Check if group exist, else create it
        if group_name not in pane.group_name:
            pane.addGroup(group_name)  
        # Get group
        index = pane.group_name.index(group_name)+1
        grp = pane.layout.itemAtPosition(0,index).widget()
        # Add Btn
        return grp.addBtn(btn_name, btn_icon, btn_type)
    
    
    def addBtnByAction(self, pane_name, group_name, action, btn_type=0):
        """
        :param pane_name: name of pane. type:String.
        :param group_name: name of group inside the pane. type:String.
        :param action: to add (with a name and an icon)
        :param btn_type: type of button to add. 0 = Big Button. 1 = Small Button. type: Int. Default=0.
        :return: created button. type:QToolButton
        """
        # Check if pane exist, else create it
        if pane_name not in self.tab_name:
            self.addSpecialTab(pane_name)  
        # Get Pane
        index = self.tab_name.index(pane_name)
        pane = self.widget(index)
        # Check if group exist, else create it
        if group_name not in pane.group_name:
            pane.addGroup(group_name)  
        # Get group
        index = pane.group_name.index(group_name)+1
        grp = pane.layout.itemAtPosition(0,index).widget()
        # Add Btn
        return grp.addBtnByAction(action, btn_type)
        
class Pane(QtGui.QScrollArea):
    def __init__(self, parent=None):
        # TODO : scroll doesn't work yet
        super(QtGui.QScrollArea, self).__init__()
        self.setWidgetResizable(False)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #ScrollBarAsNeeded
        #ScrollBarAlwaysOn
        #ScrollBarAlwaysOff
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.group_name = list()
        self.layout = QtGui.QGridLayout()
        self.layout.setMargin(0)
        self.layout.setSpacing(0)
        
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(self.layout)

    def addGroup(self, name):
        grp = Group(name)
        column = self.layout.columnCount()
        self.layout.addWidget(grp,0,column, QtCore.Qt.AlignHCenter)
        self.group_name.append( name )

class Group(QtGui.QGroupBox):
    def __init__(self, name):
        super(QtGui.QGroupBox, self).__init__(name)
        self.name = name
        self.setFlat(False)
        
        self.layout = QtGui.QHBoxLayout()
        self.layout.setMargin(6)
        self.layout.setSpacing(0)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(self.layout)
        
        self.layout.addWidget(SubGroupH())
        self.layout.addWidget(SubGroupGrid())

    def addBtn(self, name, icon, type=0):
        if type==0:
            return self.addBigBtn(name, icon)
        elif type ==1:
            return self.addSmallBtn(name, icon)
        
    def addBtnByAction(self, action, type=0):
        if type==0:
            return self.addBigBtnByAction(action)
        elif type ==1:
            return self.addSmallBtnByAction(action)

    def addBigBtn(self, name, icon):
        btn = BigBtn(name, icon)
        layout = self.layout.itemAt(0).widget().layout
        self.check_unicity_box(layout, name)

        layout.addWidget(btn)
        return btn
        
    def addSmallBtn(self, name, icon):
        btn = SmallBtn(name, icon)
        layout = self.layout.itemAt(1).widget().layout
        self.check_unicity_group(layout, name)
        column = layout.columnCount()
        row = layout.rowCount()
        nb = layout.count()
        
        new_row = nb-nb/3*3
        
        # If not a new column
        if new_row>0:
            layout.addWidget(btn, new_row+1, column-1)
        # If new column    
        else:
            layout.addWidget(btn, 1, column)
        return btn    
    
    def addBigBtnByAction(self, action):
        btn = BigBtnByAction(action)
        layout = self.layout.itemAt(0).widget().layout
        self.check_unicity_box(layout, btn.defaultAction().iconText())
        layout.addWidget(btn)
        return btn
    
    def addSmallBtnByAction(self, action):
        btn = SmallBtnByAction(action)
        layout = self.layout.itemAt(1).widget().layout
        self.check_unicity_group(layout, btn.defaultAction().iconText())
        column = layout.columnCount()
        row = layout.rowCount()
        nb = layout.count()
        
        new_row = nb-nb/3*3
        
        # If not a new column
        if new_row>0:
            layout.addWidget(btn, new_row+1, column-1)
        # If new column    
        else:
            layout.addWidget(btn, 1, column)
        return btn   
    
    def check_unicity_group(self, layout, name):
        """
        Hide old button if a new is added with the same name.
        Works with groupLayout
        """
        column = layout.columnCount()
        row = layout.rowCount()
        for y in range(column):
            for x in range(row):
                try:
                    widget = layout.itemAtPosition(x,y).widget()
                    if str(widget.text()) == str(name):
                        widget.hide()
                except:
                    pass
    
    def check_unicity_box(self, layout, name):
        """
        Hide old button if a new is added with the same name
        Works with hbox and vbox layout
        """
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if str(widget.text()) == str(name):
                widget.hide()
        
class SubGroupH(QtGui.QWidget):
    def __init__(self):
        super(QtGui.QWidget, self).__init__()       
        self.layout = QtGui.QHBoxLayout()
        self.layout.setMargin(0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(self.layout)

class SubGroupV(QtGui.QWidget):
    def __init__(self):
        super(QtGui.QWidget, self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.layout.setMargin(2)
        self.layout.setSpacing(0)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)
        
class SubGroupGrid(QtGui.QWidget):
    def __init__(self):
        super(QtGui.QWidget, self).__init__()
        self.layout = QtGui.QGridLayout()
        self.layout.setMargin(0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(self.layout)

class BigBtn(QtGui.QToolButton):
    def __init__(self, label, icon):
        super(QtGui.QToolButton, self).__init__()
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setAutoRaise(True)
        self.setIcon(icon)
        self.setText(str(label))
        self.setIconSize(big_icon_size)
        self.setMinimumSize(big_btn_size)
        self.setMaximumSize(big_btn_size)

class SmallBtn(QtGui.QToolButton):
    def __init__(self, label, icon):
        super(QtGui.QToolButton, self).__init__()
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.setAutoRaise(True)
        self.setIcon(icon)
        self.setText(str(label))
        self.setIconSize(small_icon_size)
        self.setMinimumSize(small_btn_size)
        self.setMaximumSize(small_btn_size)

class BigBtnByAction(QtGui.QToolButton):
    def __init__(self, action):
        super(QtGui.QToolButton, self).__init__()
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setAutoRaise(True)
        self.setDefaultAction(action)
        self.setIconSize(big_icon_size)
        self.setMinimumSize(big_btn_size)
        self.setMaximumSize(big_btn_size)

class SmallBtnByAction(QtGui.QToolButton):
    def __init__(self, action):
        super(QtGui.QToolButton, self).__init__()
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.setAutoRaise(True)
        self.setDefaultAction(action)
        self.setIconSize(small_icon_size)
        self.setMinimumSize(small_btn_size)
        self.setMaximumSize(small_btn_size)
