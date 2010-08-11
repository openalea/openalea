"""

:author: Thomas Cokelaer
"""
import sys
from openalea.visualea.node_widget import NodeWidget

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os

class SharedDataBrowser(NodeWidget, QDialog):
    """
    This Widget allows to select some elements in a list
    """
    def __init__(self, node, parent):

        QDialog.__init__(self, parent)
        NodeWidget.__init__(self, node)

        self.packages = ['sequence_analysis', 'stat_tool']
        self.package = 'sequence_analysis'
        self.glob = '*'
        self.path = None
        self.data = None
        self.output_filename = None

        self.widget_layout()

        self.notify(node, ("input_modified", 0))
        self.notify(node, ("caption_modified",node.get_caption() ) )

    def widget_layout(self):
        layout = QGridLayout()
        self.setLayout(layout)

        # add label for packages
        self.widget_label_packages = QLabel('1. select a package')
        layout.addWidget(self.widget_label_packages, 0, 0 )
        #self.widgets.append(self.widget_label_packages)

        # add combo box for packages
        self.widget_combo_packages = QComboBox(self)
        for i, elt in enumerate(self.packages):
            elt_name = str(elt)
            self.widget_combo_packages.addItem(elt_name)
        self.connect(self.widget_combo_packages, SIGNAL("activated(QString)"), self.update_packages)
        layout.addWidget(self.widget_combo_packages, 0, 1, 1, 3)
        #self.widgets.append(self.widget_combo_packages)

        # add textedit for package summary
        self.widget_browser_packages = QTextEdit(self)
        self.widget_browser_packages.setReadOnly(True)
        self.widget_browser_packages.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.widget_browser_packages.clear()
        self.widget_browser_packages.append("")
        layout.addWidget(self.widget_browser_packages, 1, 1 , 1, 3)

        # add label to filter the filenames
        self.widget_label_glob = QLabel('2.Filter the data: (e.g., *.dat)')
        layout.addWidget(self.widget_label_glob, 2, 0 )

        # add QEdit for the glob
        self.widget_glob = QLineEdit(self)
        self.connect(self.widget_glob, SIGNAL("textChanged(QString)"), self.update_glob)
        layout.addWidget(self.widget_glob, 2, 1,1,2)
        self.widget_glob.setText(self.glob)

        # label for the data 
        self.widget_label_data = QLabel('3. Select the data file:')
        layout.addWidget(self.widget_label_data, 3, 0 )

        # combobox for the data selection
        self.widget_combo_data = QComboBox(self)
        self.connect(self.widget_combo_data, SIGNAL("activated(QString)"), self.selection_data)
        layout.addWidget(self.widget_combo_data,3,1, 1,3)

        self.setWindowTitle("SharedData browser")
        self.setGeometry(250, 200, 350, 550)


    def notify(self, sender, event):
        # Notification sent by node 
        if event[0] == 'caption_modified' :
            self.window().setWindowTitle(event[1])

        if(event[0] != "input_modified"): return

        # if inputs are modified and run is presse, then we are here
        if len(self.node.get_input(0))!=0:
            # if packages is a string, there is only one package and cast to a list must be done
            if type(self.packages)==list:
                self.packages = self.node.get_input(0)
            else:
                self.packages = [self.node.get_input(0)]
            self.widget_combo_packages.clear()
            for i, elt in enumerate(self.packages):
                elt_name = str(elt)
                self.widget_combo_packages.addItem(elt_name)
            
        if self.node.get_input(1)!=None:
            self.glob = self.node.get_input(1)
            self.widget_glob.setText(self.glob)
        
        if self.node.get_input(2)!=None:
            self.data = self.node.get_input(2)
            self.widget_data.setText(self.data)

        #self.node.out_indices = [True for i in self.in_list]
        self.update_packages(self.package)
        self.update_glob(self.glob) #does also update_data
        self.node._output = str(self.output_filename)


    def update_packages(self, package):
        self.package = package
        valid_keys = {'name':'name', 'package':'name', 'pkg_name':'name', 'url':'home_page',  'authors':'author', 
            'author_email':'authors_email', 'version':'version'}
            

        try:
            cmd = 'import openalea.%s as mypackage' % self.package
            exec(cmd)
            from openalea.deploy.shared_data import get_shared_data_path
            self.path = get_shared_data_path(mypackage.__path__)

            from openalea.deploy.metainfo import get_metadata
            cmd = 'import openalea;metadata = get_metadata(openalea.%s)' % self.package
            exec(cmd)
        except:
            self.widget_browser_packages.setText("Could not import this package (%s) or retrieve metainfo" % self.package)
        txt = "<p style=\"color:red\"><b>Package %s metadata</b></p>" % self.package
        for key, value in valid_keys.iteritems():
            if key=='url':
                try:
                    txt += '<b>%s</b>: <a href="%s">web documentation</a><br/>' % (key.title(), getattr(metadata,value))
                except:
                    txt += '<b>%s</b>: <a href="%s">web documentation</a><br/>' % (key.title(), 'not filled!!')
            else:
                try:
                    txt += '<b>%s</b>: %s<br/>' % (key.title(), getattr(metadata,value))
                except:
                    txt += '<b>%s</b>: %s<br/>' % (key.title(), 'not filled')

        self.widget_browser_packages.setText(txt)

        self.update_data(self.data)

    def update_data(self, data):
        self.output_filename = None
        self.data = data
        import glob
        import os
        filenames = []
        try:
            filenames = glob.glob(str(self.path) +  os.sep + str(self.glob))
        except:
            pass
        self.widget_combo_data.clear()
        for i, elt in enumerate(filenames):
            elt_name = str(elt)
            self.widget_combo_data.addItem(os.path.basename(elt_name))
        
        if len(filenames) == 1:
            #self.output_filename = str(filenames[0])
            self.output_filename = os.path.join(str(self.path), os.sep, str(filenames[0]))
            self.node._output = str(self.output_filename)

    def selection_data(self, data):
        self.data = data
        import os
        self.output_filename = os.path.join(self.path,  str(self.data))
        self.node._output = str(self.output_filename)

    def update_glob(self, glob):
        self.glob = glob
        self.widget_glob.setText(glob)
        self.update_data(self.data)














