################################################################################
# Widgets
import sys
from openalea.visualea.node_widget import NodeWidget       

from openalea.vpltk.qt import QtCore, QtGui

class ListSelector(NodeWidget, QtGui.QDialog):
    """
    This Widget allows to select some elements in a list
    """
    def __init__(self, node, parent):

        QtGui.QDialog.__init__(self, parent)
        NodeWidget.__init__(self, node)

        #self.browser = QtGui.QTextBrowser()
        
        layout = QtGui.QVBoxLayout()
        #layout.addWidget(self.browser)
        self.setLayout(layout)

        self.in_list = []
        self.widgets = []
        self.notify(node, ("input_modified", 0))
        


    def notify(self, sender, event):
        # Notification sent by node 

        if(event[0] != "input_modified"): return

        self.in_list = self.node.get_input(0)
        self.node.out_indices = [True for i in self.in_list]       
        self.create_buttons()


    def reactToClick(self, index):
        #self.node.out_indices[index] = button.isChecked()
        #if not buttonlist[i].isChecked():

        outs = self.node.out_indices
        outs[index] = self.widgets[index].isChecked()

        #self.browser.clear()
        #self.browser.append("<b> The List contains the following elements:</b>")
        #for i, l in enumerate(self.in_list):
        #    if outs[i]:
        #        self.browser.append(l)

        #self.node.set_output(0, self.node.out)

    def create_buttons(self):
        """ Remove old buttons and add new ones.
        """
        # Manage in the new func
  
        layout = self.layout()

        for w in self.widgets:
            layout.removeWidget(w)
        
        self.widgets = []

        for i, elt in enumerate(self.in_list):
            elt_name = str(elt)
            button = QtGui.QCheckBox(elt_name)
            button.setChecked(True)

            self.connect(button, QtCore.SIGNAL("clicked()"), lambda index=i: self.reactToClick(index))
            layout.addWidget(button)
            self.widgets.append(button)


            








