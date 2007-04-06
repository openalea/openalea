# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
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

__doc__="""
QT4 Main window 
"""

__license__= "CeCILL v2"
__revision__=" $Id: mainwindow.py 453 2007-04-05 16:53:45Z dufourko $ "


from PyQt4 import QtCore, QtGui
import ui_newgraph


class NewGraph(QtGui.QDialog, ui_newgraph.Ui_NewGraphDialog) :
    """ New network dialog """
    
    def __init__(self, title, packages, categories, parent=None):
        """
        Constructor
        @param pacakges : the list of packages the graph can be added to
        """
        
        QtGui.QDialog.__init__(self, parent)
        ui_newgraph.Ui_NewGraphDialog.__init__(self)
        self.setWindowTitle(title)

        self.setupUi(self)

        pkgstr = []
        self.pkgmap = {}
        
        for p in packages:
            pkgstr.append(p.name)
            self.pkgmap[p.name] = p

        self.packageBox.addItems(pkgstr)
        self.categoryEdit.addItems(categories)


    def accept(self):

        # Test if name is correct
        name = str(self.nameEdit.text())
        if(self.get_package().has_key(name)):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                            "The Name is already use")
            return
        
        QtGui.QDialog.accept(self)


    def get_package(self):
        """ Return the selected package """

        pkgstr = str(self.packageBox.currentText().toAscii())
        return self.pkgmap[pkgstr]


    def get_data(self):
        """
        Return the dialog data in a tuple
        (name, nin, nout, category, description)
        """

        name = str(self.nameEdit.text())
        category = str(self.categoryEdit.currentText().toAscii())
        description = str(self.descriptionEdit.text().toAscii())
        
        return (name, self.inBox.value(), self.outBox.value(), self.get_package(),
                category, description)
    
        

import ui_newpackage

class NewPackage(QtGui.QDialog, ui_newpackage.Ui_NewPackageDialog) :
    """ New package dialog """

    
    def __init__(self, parent=None):
        
        QtGui.QDialog.__init__(self, parent)
        ui_newpackage.Ui_NewPackageDialog.__init__(self)


    def accept(self):

        # Test if name is correct
        QtGui.QDialog.accept(self)


    def get_data(self):
        """
        Return the dialog data in a dictionnary
        """

#         name = str(self.nameEdit.text())
#         category = str(self.categoryEdit.currentText().toAscii())
#         description = str(self.descriptionEdit.text().toAscii())
        
#         return (name, self.inBox.value(), self.outBox.value(), self.get_package(),
#                 category, description)
   
