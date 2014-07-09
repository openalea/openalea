# -*- coding: utf-8 -*-
__all__ = ["PreferenceWidget"]

from openalea.vpltk.qt import QtGui, QtCore
from openalea.core import settings
from openalea.oalab.service.qt_control import qt_widget_plugins

def Widget(label, value):
    """
    :return: create a widget which permit to edit the value with a label
    """
    try:
        eval_value = eval(value)
    except NameError:
        eval_value = value
    is_str = False
    
    wid = QtGui.QWidget()
    layout = QtGui.QHBoxLayout(wid)
    layout.addWidget(QtGui.QLabel(label))

    if value == "False" or value == "True":
        editorclass = qt_widget_plugins("IBool")[0]
        editor = editorclass.load()()
    elif isinstance(eval_value, int):
        editorclass = qt_widget_plugins("IInt")[0]
        editor = editorclass.load()
        editor = editor.edit(eval_value)
    elif isinstance(eval_value, list):
        editorclass = qt_widget_plugins("ISequence")[0]
        editor = editorclass.load()()
        # API is not good. (value != get_value)
        # TODO: fix it inside core.interface.py or inside controls
        editor.get_value = editor.value 
    else:
        editorclass = qt_widget_plugins("IStr")[0]
        is_str = True
        editor = editorclass.load()()

    if is_str:
        editor.setValue(value)
    else:
        editor.setValue(eval_value)
        
    layout.addWidget(editor)
    return wid

       
def get_label_and_value(widget):
    """
    :return: the current label and value from a widget constructed by "Widget" function
    """
    labelwidget = widget.layout().itemAt(0).widget()
    valuewidget = widget.layout().itemAt(1).widget()

    return labelwidget.text(), valuewidget.value()

        
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
            if section != "AutoAddedConfItems" and section != "MainWindow" and section != "TreeView":
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
