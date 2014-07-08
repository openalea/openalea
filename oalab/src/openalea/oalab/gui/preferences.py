# -*- coding: utf-8 -*-
__all__ = ["PreferenceWidget"]

from openalea.vpltk.qt import QtGui, QtCore
from openalea.core import settings

def Widget(label, value):
    """
    :return: create a widget which permit to edit the value with a label
    """
    try:
        eval_value = eval(value)
    except NameError:
        eval_value = value
    
    # Check Box if bool
    if value == "False" or value == "True":
        wid = QtGui.QCheckBox(label)
        wid.setChecked(eval(value))
        return wid
        
    # Spin Box if int
    elif isinstance(eval_value, int):
        wid = QtGui.QWidget()
        layout = QtGui.QHBoxLayout(wid)
        layout.addWidget(QtGui.QLabel(label))
        sp = QtGui.QSpinBox()
        sp.setValue(eval_value)
        layout.addWidget(sp)
        return wid
        
    # else Line Edit
    else:
        wid = QtGui.QWidget()
        layout = QtGui.QHBoxLayout(wid)
        layout.addWidget(QtGui.QLabel(label))
        layout.addWidget(QtGui.QLineEdit(value))
        return wid

def get_label_and_value(widget):
    """
    :return: the current label and value from a widget constructed by "Widget" function
    """
    if hasattr(widget, "isChecked"):
        return widget.text(), widget.isChecked()
    else:
        labelwidget = widget.layout().itemAt(0).widget()
        valuewidget = widget.layout().itemAt(1).widget()
        if hasattr(valuewidget,"value"):
            return labelwidget.text(), valuewidget.value()
        elif hasattr(valuewidget, "text"):
            return labelwidget.text(), valuewidget.text()
    
        
class PreferenceWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        """
        Widget to change settings.
        
        TODO!
        """
        super(PreferenceWidget, self).__init__(parent)
        self.setWindowTitle("OpenAleaLab Preferences")
        self.resize(600, 300)
        
        mainlayout = QtGui.QVBoxLayout(self)
        
        self.tabwidget = QtGui.QTabWidget(self)
        mainlayout.addWidget(self.tabwidget)
        config = settings.Settings()
        self.sections = config.sections()
        
        for section in self.sections:
            if section != "AutoAddedConfItems":
                tab = QtGui.QWidget(self.tabwidget)
                self.tabwidget.addTab(tab, section)
                layout = QtGui.QVBoxLayout(tab)
                options = config.options(section)
                for option in options:
                    value = config.get(section, option)
                    wid = Widget(option, value)
                  
                    layout.addWidget(wid)
                layout.addStretch()

    def write_settings(self):
        config = settings.Settings()
        tabwidget = self.tabwidget
        
        n1 = tabwidget.count()
        for i1 in range(n1):
            widget = tabwidget.widget(i1)
            section = tabwidget.tabText(i1)
            layout = widget.layout()
            n2 = layout.count()
            for i2 in range(n2):
                wi = layout.itemAt(i2).widget()
                if wi:
                    option, value = get_label_and_value(wi)                                      
                    config.set(str(section), str(option), str(value))
        config.write()
        self.close()
        
        
def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    win = PreferenceWidget()
    win.show()
    win.raise_()
    app.exec_()
    
if(__name__ == "__main__"):
    main()
