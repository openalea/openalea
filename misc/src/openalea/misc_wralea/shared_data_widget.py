"""

:author: Thomas Cokelaer
"""
import sys
from openalea.visualea.node_widget import NodeWidget

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class SharedDataBrowser(NodeWidget, QDialog):
    """
    This Widget allows to select some elements in a list
    """
    def __init__(self, node, parent):


        print 'a'
        QDialog.__init__(self, parent)
        print 'b'
        NodeWidget.__init__(self, node)
        print 'c'

        self.packages = ['sequence_analysis', 'stat_tool']
        self.package = None
        self.glob = '*'
        self.path = None
        self.data = None
        self.output_filename = None

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
        #self.connect(self.widget_glob, SIGNAL("activated(QString)"), self.update_glob)
        self.connect(self.widget_glob, SIGNAL("textChanged(QString)"), self.update_glob)
        #todo
        #self.widget_glob.textChanged.connect(self.update_glob)
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

        #self.widgets = []
        self.notify(node, ("input_modified", 0))

    def notify(self, sender, event):
        # Notification sent by node 

        if(event[0] != "input_modified"): return

        print 'from user inputs'
        print self.node.get_input(0)
        print self.node.get_input(1)
        if len(self.node.get_input(0))!=0:
            self.packages = self.node.get_input(0)
            self.widget_combo_packages.clear()
            for i, elt in enumerate(self.packages):
                elt_name = str(elt)
                self.widget_combo_packages.addItem(elt_name)
        if self.node.get_input(1)!=None:
            self.glob = self.node.get_input(1)
            self.widget_glob.setText(self.glob)

        #self.node.out_indices = [True for i in self.in_list]
        self.update_packages(self.package)
        self.update_glob(self.glob) #does also update_data
        self.node.output_filename = str(self.output_filename)


    def update_packages(self, package):
        valid_keys = ['name', 'package', 'pkg_name', 'url', 'project', 'authors', 
            'authors_email', 'version', 'release' , 'license', 'url']
        self.package = package
        if self.package:
            try:
                cmd = 'import openalea.%s.data as data' % self.package
                exec(cmd)
                self.path = data.path


                cmd = 'import openalea.%s as tmp' % self.package
                exec(cmd)
                txt = "<p style=\"color:red\"><b>Package %s metadata</b></p>" % self.package
                for key in valid_keys:
                    if key=='url':
                        try:
                            txt += '<b>%s</b>: <a href="%s">web documentation</a><br/>' % (key.title(), tmp.metadata[key])
                        except:
                            txt += '<b>%s</b>: <a href="%s">web documentation</a><br/>' % (key.title(), 'not filled!!')
                    else:
                        try:
                            txt += '<b>%s</b>: %s<br/>' % (key.title(), tmp.metadata[key])
                        except:
                            txt += '<b>%s</b>: %s<br/>' % (key.title(), 'not filled')

                self.widget_browser_packages.setText(txt)
                print 'Succeeded'
            except:
                self.widget_browser_packages.setText("Could not import this package (%s) or retrieve metainfo" % self.package)

        self.update_data(self.data)

    def update_data(self, data):
        self.data = data
        import glob
        import os
        filenames = []
        try:
            filenames = glob.glob(str(self.path) +  str(self.glob))
        except:
            pass
        self.widget_combo_data.clear()
        for i, elt in enumerate(filenames):
            elt_name = str(elt)
            self.widget_combo_data.addItem(os.path.basename(elt_name))

    def selection_data(self, data):
        self.data = data
        import os
        self.output_filename = os.path.join(str(self.path), str(self.data))
        print 'bbbb'
        print self.output_filename
        self.node.output_filename = str(self.output_filename)

    def update_glob(self, glob):
        self.glob = glob
        self.widget_glob.setText(glob)
        self.update_data(self.data)














