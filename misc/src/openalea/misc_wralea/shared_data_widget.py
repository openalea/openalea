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
    This widget permits to select a shared data file located in a given Python package.
    """
    def __init__(self, node, parent):

        QDialog.__init__(self, parent)
        NodeWidget.__init__(self, node)
                
        self.package = ''
        self.glob = '*'
        self.shared_data_dirpath = None
        self.data_filename = None
        self.output_data_filepath = None

        self.widget_layout()

        self.notify(node, ("input_modified", 0))
        self.notify(node, ("caption_modified",node.get_caption() ) )

    def widget_layout(self):
        layout = QGridLayout()
        self.setLayout(layout)

        # add label for package
        self.widget_label_package = QLabel('1. Set the package')
        layout.addWidget(self.widget_label_package, 0, 0 )
        
        # add QEdit for the package
        self.widget_package = QLineEdit(self)
        layout.addWidget(self.widget_package, 0, 1,1,3)
        self.widget_package.setText(self.package)
        self.connect(self.widget_package, SIGNAL("textChanged(QString)"), self.update_package)

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
        layout.addWidget(self.widget_glob, 2, 1,1,2)
        self.widget_glob.setText(self.glob)
        self.connect(self.widget_glob, SIGNAL("textChanged(QString)"), self.update_glob)

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

        # if inputs are modified and run is pressed, then we are here
        if self.node.get_input(0)!=None:
            self.package = self.node.get_input(0)
            self.widget_package.setText(self.package)
            
        if self.node.get_input(1)!=None:
            self.glob = self.node.get_input(1)
            self.widget_glob.setText(self.glob)
        
        if self.node.get_input(2)!=None:
            self.data_filename = self.node.get_input(2)
#            self.widget_data.setText(self.data_filename)

        self.update_package(self.package)
        self.update_glob(self.glob) #does also update_data
        self.node._output = self.output_data_filepath


    def update_package(self, package):
        self.package = str(package)
        from openalea.deploy.util import get_metadata
        try:
            m = __import__(self.package, fromlist=[''])
            from openalea.deploy.shared_data import get_shared_data_path
        except:
            self.widget_browser_packages.setText("Can not import %s." % self.package)
        else:
            try:
                self.shared_data_dirpath = get_shared_data_path(m.__path__)
                metadata = get_metadata(self.package)
            except:
                self.widget_browser_packages.setText("Can not retrieve metainfo from %s." % self.package)
            else:
                txt = "<p style=\"color:red\"><b>Package %s metadata</b></p>" % self.package
                for line in metadata:
                    try:
                        val1, val2 = line.split(':')
                    except:
                        val1 = line
                        val2 = 'not filled'
                    if val1=='Home-page':
                        txt += '<b>%s</b>: <a href="%s">web documentation</a><br/>' % (val1.title(),val2)
                    else:
                        txt += '<b>%s</b>: %s<br/>' % (val1 , val2)
        
                self.widget_browser_packages.setText(txt)
    
            self.update_data(self.data_filename)


    def update_data(self, data):
        self.output_data_filepath = None
        self.data_filename = data
        import glob
        import os
        filenames = []
        try:
            filenames = glob.glob(self.shared_data_dirpath +  os.sep + self.glob)
        except:
            pass
        self.widget_combo_data.clear()
        for i, elt in enumerate(filenames):
            elt_name = str(elt)
            self.widget_combo_data.addItem(os.path.basename(elt_name))
        
        if len(filenames) == 1:
            self.output_data_filepath = os.path.join(self.shared_data_dirpath, os.sep, str(filenames[0]))
            self.node._output = self.output_data_filepath
            self.node.set_input(2, self.node._output)


    def selection_data(self, data):
        self.data_filename = str(data)
        import os
        self.output_data_filepath = os.path.join(self.shared_data_dirpath,  self.data_filename)
        self.node._output = self.output_data_filepath


    def update_glob(self, glob):
        self.glob = str(glob)
        self.widget_glob.setText(self.glob)
        self.update_data(self.data_filename)













