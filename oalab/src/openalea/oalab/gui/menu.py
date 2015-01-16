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

"""

Full example:

.. code-block:: python

    from openalea.vpltk.qt import QtGui
    from openalea.oalab.gui.menu import PanedMenu

    # Create ribbon bar
    menu = PanedMenu()

    # Create Qt QAction
    act1 = QtGui.QAction(u'act 1', menu)
    act2 = QtGui.QAction(u'act 2', menu)

    # Add actions to ribbon bar
    menu.addBtnByAction('Panel', 'group', act1, PanedMenu.BigButton)
    menu.addBtnByAction('Panel', 'group', act2, PanedMenu.SmallButton)

"""

__revision__ = ""

from openalea.vpltk.qt import QtGui, QtCore

"""
# To generate images
from openalea.lpy.gui.compile_ui import check_rc_generation
check_rc_generation('resources.qrc')
"""

Policy = QtGui.QSizePolicy
size_policy_xsmall = Policy(Policy.Maximum, Policy.Preferred)
size_policy_ysmall = Policy(Policy.Preferred, Policy.Maximum)
size_policy_preferred = Policy(Policy.Preferred, Policy.Preferred)

big_btn_size = QtCore.QSize(25, 25)
small_btn_size = QtCore.QSize(140, 16)
big_icon_size = QtCore.QSize(24, 24)
small_icon_size = QtCore.QSize(16, 16)
paned_menu_size = QtCore.QSize(10000, 80)

style_paned_menu = """

    QWidget {
         background-color: transparent;
     }

    """

style_pane = """
    QWidget {
         background-color: red;
     }
     """

style_group = """
    QWidget {
         background-color: green;
     }
     """

style = """
    QToolButton {
         background-color: transparent;
         min-width: 80px;
     }

    QToolButton:hover {
        border: 1px solid rgb(200, 200, 200);
        border-radius: 2px;
    }

    QToolButton:pressed {
        background-color: rgba(0, 0, 0, 50);
        border: 1px solid rgb(175, 175, 175);
        border-radius: 2px;
    }

"""


def fill_panedmenu(menu, actions):
    for action in actions:
        if isinstance(action, QtGui.QAction):
            menu.addBtnByAction('Default', 'Default', action, 0)
        elif isinstance(action, (list, tuple)):
            menu.addBtnByAction(*action)
        elif isinstance(action, dict):
            args = [
                action.get('pane', 'Default'),
                action.get('group', 'Default'),
                action['action'],
                action.get('style', 0)
            ]
            menu.addBtnByAction(*args)
        elif isinstance(action, QtGui.QMenu):
            pass
        else:
            continue


class PanedMenu(QtGui.QTabWidget):

    """
    A widget that tries to mimic menu of Microsoft Office 2010.
    Cf. Ribbon Bar.

    >>> from openalea.oalab.gui.menu import PanedMenu
    >>> menu = PanedMenu()

    """
    BigButton = 0
    SmallButton = 1
    BigWidget = 'bigwidget'
    SmallWidget = 'smallwidget'

    def __init__(self, parent=None):
        super(PanedMenu, self).__init__()
        self.setObjectName('PanedMenu')
        self.setAccessibleName("Menu")
        self.tab_name = list()

        self.fine_tune()

    def fine_tune(self):
        self.setSizePolicy(size_policy_preferred)
        self.setStyleSheet(style_paned_menu)

    def addSpecialTab(self, label, widget=None):
        widget = Pane()
        self.tab_name.append(label)
        self.addTab(widget, label)
        return widget

    def addBtns(self, pane_names, group_names, btn_names, btn_icons, btn_types):
        # TODO
        pass

    def addBtn(self, pane_name, group_name, btn_name, btn_icon, btn_type=0):
        """
        :param pane_name: name of pane. type:String.
        :param group_name: name of group inside the pane. type:String.
        :param btn_name: name of button inside the group. type:String.
        :param btn_icon: icon of button. type:QtGui.QIcon.
        :param btn_type: type of button to add. 0 = Big Button. 1 = Small Button, smallwidget = Small Widget, bigwidget = Big Widget. Default=0.
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
        index = pane.group_name.index(group_name) + 1
        grp = pane.layout.itemAtPosition(0, index).widget()
        # Add Btn
        return grp.addBtn(btn_name, btn_icon, btn_type)

    def addBtnByAction(self, pane_name, group_name, action, btn_type=0):
        """
        :param pane_name: name of pane. type:String.
        :param group_name: name of group inside the pane. type:String.
        :param action: to add (with a name and an icon)
        :param btn_type: type of button to add. 0 = Big Button. 1 = Small Button, smallwidget = Small Widget, bigwidget = Big Widget. Default=0.
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
        index = pane.group_name.index(group_name) + 1
        grp = pane.layout.itemAtPosition(0, index).widget()
        # Add Btn
        return grp.addBtnByAction(action, btn_type)

    def showPane(self, pane_name):
        # Find tab named 'name'
        try:
            index = self.tab_name.index(pane_name)
        except ValueError:
            pass
        else:
            self.setCurrentIndex(index)


class Pane(QtGui.QWidget):

    def __init__(self, parent=None):
        # TODO : scroll doesn't work yet
        super(Pane, self).__init__()
        self.setObjectName('Pane')
        self.group_name = list()
        self._layout = QtGui.QGridLayout(self)
        self.fine_tune()

    def fine_tune(self):
        # self.setWidgetResizable(False)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # ScrollBarAsNeeded
        # ScrollBarAlwaysOn
        # ScrollBarAlwaysOff
        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setSizePolicy(size_policy_preferred)
        self.setStyleSheet(style_pane)

    def addGroup(self, name):
        grp = Group(name)
        column = self._layout.columnCount()
        self._layout.addWidget(grp, 0, column)
        self.group_name.append(name)


class Group(QtGui.QWidget):

    def __init__(self, name, orientation=QtCore.Qt.Horizontal):
        super(Group, self).__init__()

        self.setToolTip(name)
        self.setObjectName('Group')
        self.name = name

        self.row_number = 2
        self.orientation = orientation

        if orientation == QtCore.Qt.Horizontal:
            self.layout = QtGui.QHBoxLayout()
            self.layout.setAlignment(QtCore.Qt.AlignLeft)
        else:
            self.layout = QtGui.QVBoxLayout()
            self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)

        if orientation == QtCore.Qt.Horizontal:
            self._group_big = SubGroupH()
            self._group_small = SubGroupGrid()
        else:
            self._group_big = SubGroupV()
            self._group_small = SubGroupV()

        self.layout.addWidget(self._group_big)
        self.layout.addWidget(self._group_small)
        self.fine_tune()

    def fine_tune(self):
        self.setSizePolicy(size_policy_preferred)
        self.setStyleSheet(style_group)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def addBtnByAction(self, action, style=PanedMenu.BigButton):
        if style == PanedMenu.BigButton:
            return self.addBigToolButton(action)
        elif style == PanedMenu.SmallButton:
            return self.addSmallToolButton(action)
        elif style == PanedMenu.SmallWidget:
            return self.addWidget(action, "small")
        elif style == PanedMenu.BigWidget:
            return self.addWidget(action, "big")

    def addWidget(self, widget, style="bigwidget"):
        """
        Permit to add small widget like if it was a small button
        """
        if style == 'big':
            self._group_big.addWidget(widget)
        else:
            self._group_small.addWidget(widget)

    def addBigBtn(self, name, icon):
        btn = BigToolButton(name, icon)
        self._group_big.addWidget(btn)
        return btn

    def addSmallBtn(self, name, icon):
        btn = SmallToolButton(name, icon)
        self._group_small.addWidget(btn)
        return btn

    def addBigToolButton(self, action):
        btn = BigToolButton(action)
        self._group_big.addWidget(btn)
        return btn

    def addSmallToolButton(self, action):
        btn = SmallToolButton(action)
        self._group_small.addWidget(btn)
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
                    widget = layout.itemAtPosition(x, y).widget()
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
        super(SubGroupH, self).__init__()
        self.setObjectName('SubGroupH')
        self.layout = QtGui.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(self.layout)
        self.setSizePolicy(size_policy_preferred)
        self.setStyleSheet(style)

    def addWidget(self, widget):
        widget.setSizePolicy(Policy(Policy.Preferred, Policy.Minimum))
        self.layout.addWidget(widget)


class SubGroupV(QtGui.QWidget):

    def __init__(self):
        super(SubGroupV, self).__init__()
        self.setObjectName('SubGroupV')
        self._layout = QtGui.QVBoxLayout(self)

        self.fine_tune()

    def fine_tune(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self.setSizePolicy(size_policy_ysmall)
        self.setStyleSheet(style)

    def addWidget(self, widget):
        self._layout.addWidget(widget)


class SubGroupGrid(QtGui.QWidget):

    def __init__(self, row_number=2):
        super(SubGroupGrid, self).__init__()
        self._count = 0
        self.row_number = row_number
        self.setObjectName('SubGroupGrid')
        self.layout = QtGui.QGridLayout(self)

        self.fine_tune()

    def fine_tune(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setSizePolicy(size_policy_preferred)
        self.setStyleSheet(style)

    def addWidget(self, widget):
        row = self._count % self.row_number
        col = self._count / self.row_number
        self.layout.addWidget(widget, row, col)
        self._count += 1


class ToolButton(QtGui.QToolButton):

    def __init__(self, action, icon=None):
        super(ToolButton, self).__init__()
        self.setObjectName('ToolButton')
        self.setAutoRaise(True)

        if isinstance(action, QtGui.QAction):
            self.setDefaultAction(action)
        else:
            self.setText(str(action))
            if isinstance(icon, QtGui.QIcon):
                self.setIcon(icon)

        self.setStyleSheet(style)
        self.setSizePolicy(size_policy_preferred)


class BigToolButton(ToolButton):

    def __init__(self, action, icon=None):
        super(BigToolButton, self).__init__(action, icon)

        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setIconSize(big_icon_size)
        self.setMinimumSize(big_btn_size)


class SmallToolButton(ToolButton):

    def __init__(self, action, icon=None):
        super(SmallToolButton, self).__init__(action, icon)

        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.setIconSize(small_icon_size)
        self.setMinimumSize(big_btn_size)

import weakref


class ContextualMenu(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        self._layout = QtGui.QHBoxLayout(self)
        self._current_group = None
        self._group = {}
        self.clear()

        self.fine_tune()

    def fine_tune(self):
        self.setContentsMargins(0, 0, 0, 0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(size_policy_preferred)
        self.setStyleSheet(style_paned_menu)

    def _new_group(self, name):
        width = self.size().width()
        height = self.size().height()
        if height > width:
            orientation = QtCore.Qt.Vertical
        else:
            orientation = QtCore.Qt.Horizontal
        identifier = '%s:%s' % (name, orientation)
        if identifier in self._group:
            group = self._group[identifier]
        else:
            group = Group(name, orientation=orientation)
        self._current_group = weakref.ref(group)
        self._layout.addWidget(group)
        group.show()

    def clear(self):
        if self._current_group:
            group = self._current_group()
            if group:
                self._layout.removeWidget(group)
                group.hide()

    def set_actions(self, name, actions):
        self.clear()
        self._new_group(name)
        fill_panedmenu(self, actions)

    def addBtnByAction(self, pane_name, group_name, action, btn_type=0):
        if self._current_group is None or self._current_group() is None:
            return

        self._current_group().addBtnByAction(action, btn_type)

    def properties(self):
        return dict(style=0)

    def set_properties(self, properties):
        get = properties.get
        style = get('style', 0)

if __name__ == '__main__':

    import sys
    from openalea.vpltk.qt import QtGui

    instance = QtGui.QApplication.instance()
    if instance is None:
        qapp = QtGui.QApplication(sys.argv)
    else:
        qapp = instance

    # Example: create a panel with one group containing 1 big and 3 small buttons
    menu = PanedMenu()

    act0 = QtGui.QAction(u'Action', menu)
    act1 = QtGui.QAction(u'act 1', menu)
    act2 = QtGui.QAction(u'act 2', menu)
    act3 = QtGui.QAction(u'act 3', menu)

    menu.addBtnByAction('Panel', 'group', act0, PanedMenu.BigButton)
    menu.addBtnByAction('Panel', 'group', act1, PanedMenu.SmallButton)
    menu.addBtnByAction('Panel', 'group', act2, PanedMenu.SmallButton)
    menu.addBtnByAction('Panel', 'group', act3, PanedMenu.SmallButton)
    menu.show()

    if instance is None:
        qapp.exec_()
