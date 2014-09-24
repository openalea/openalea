# -*- coding: utf-8 -*-
__all__ = ["PreferenceWidget"]

import ast
from openalea.vpltk.qt import QtGui, QtCore
from openalea.core import settings
from openalea.oalab.service.qt_control import qt_editor
from openalea.core.service import guess_interface, new_interface
from openalea.core.control import Control

def Widget(option_name, value):
    """
    :return: create a widget which permit to edit the value with a label
    """
    # TODO: Currently an evaluation is used to guess value type.
    # This approach may fails for complex data
    # We need to improve option type management, for example by providing an associated map "option_name -> type".
    # We should also add constraints on values
    try:
        eval_value = ast.literal_eval(value)
    except (ValueError, SyntaxError):
        eval_value = value
    
    inames = guess_interface(eval_value)
    if len(inames):
        iname = inames[0]
    else:
        iname = 'IStr'
        
    # Dirty hack to handle int constraints on font size.
    if 'font' in option_name and iname == 'IInt':
        iname = new_interface(iname, min=5, max=200)

    control = Control(option_name, iname, eval_value)
    editor = qt_editor(control)
    return control, editor

        
class PreferenceWidget(QtGui.QWidget):
    hidden_sections = ["AutoAddedConfItems", "MainWindow", "TreeView"]

    def __init__(self, parent=None):
        """
        Widget to change settings.

        """
        super(PreferenceWidget, self).__init__(parent)
        self.setWindowTitle("OpenAleaLab Preferences")
        self.resize(600, 300)
        
        mainlayout = QtGui.QVBoxLayout(self)
        
        self.tabwidget = QtGui.QTabWidget(self)
        mainlayout.addWidget(self.tabwidget)
        config = settings.Settings()
        
        self._config = None
        self._option_values = {}
        self._set_config(config)

    def _set_config(self, config):
        #TODO
        # Manage memory (are children widgets destroyed when tabwidget.clear ?)
        # Once it is sure all widget are totally cleaned and destroyed, 
        # we can move it to public method to allow to change config dynamically
        self._config = config
        sections = config.sections()    

        self.tabwidget.clear()
        
        for section in sections:
            if section not in self.hidden_sections:
                self._option_values[section] = []
                tab = QtGui.QWidget(self.tabwidget)
                self.tabwidget.addTab(tab, section)
                layout = QtGui.QFormLayout(tab)
                options = config.options(section)
                for option_name in options:
                    value = config.get(section, option_name)
                    control, widget = Widget(option_name, value)
                    self._option_values[section].append(control)
                    layout.addRow(option_name, widget)
                # layout.addStretch()
               
    def update_config(self, config=None, save=False):
        if not config:
            config = self._config
        if config:
            for section, options in self._option_values.items():
                for option in options:
                    config.set(section, option.name, str(option.value))
            if save:
                config.write()
        
        
def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    win = PreferenceWidget()
    win.show()

    # PreferenceWidget.hidden_sections = []
    # win2 = PreferenceWidget()
    # win2.show()

    win.raise_()
    app.exec_()
    
if(__name__ == "__main__"):
    main()
