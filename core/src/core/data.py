# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2008 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################


__doc__="""
Data management classes
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

from openalea.core.node import AbstractFactory, Node, NodeFactory
from openalea.core.interface import IData

import os
import string



class PackageData(object):
    """ String representing a package data """

    # if __local__ is True, then PackageData point to a local data (i.e in the currrent directory)
    __local__ = False

    def __init__(self, pkg_name, filename, package=None):
        """ 
        pkg_name : package name 
        name : data name
        package : Package object
        """
        self.pkg_name = pkg_name
        self.name = filename

        if(not package):
            from openalea.core.pkgmanager import PackageManager
            path = PackageManager()[self.pkg_name].path
        else:
            path = package.path

        if(PackageData.__local__):
            self.repr = self.name
        else:
            self.repr = os.path.join(path, self.name)
        

    def __repr__(self):
        return "PackageData(%s, %s)"%(self.pkg_name, self.name)

    def __str__(self):
        return self.repr



class DataFactory(AbstractFactory):
    """ Data representation as factory """
    
    #mimetype = "openalea/datafactory"

    def __init__(self,
                 name,
                 description = '',
                 editors = None,
                 **kargs):
        """
        name : filename
        description : file description
        editors : dictionnary listing external command to execute
        """

        AbstractFactory.__init__(self, name, description, category='data', **kargs)
        self.pkgdata_cache = None

        self.editors = editors


    def is_valid(self):
        """ 
        Return True if the factory is valid 
        else raise an exception
        """
        if(not os.path.exists(str(self.get_pkg_data()))):
            raise Exception("%s does'nt exists. Ignoring"%(str(self.get_pkg_data())))
                        

    def get_pkg_data(self):
        """ Return the associated PackageData object """

        if(not self.pkgdata_cache):
            self.pkgdata_cache = PackageData(self.package.name, self.name, self.package)
            
        return self.pkgdata_cache
    
    
    def instantiate(self, call_stack=[]):
        """ Return a node instance
        @param call_stack : the list of NodeFactory id already in call stack
        (in order to avoir infinite recursion)
        """

        node = DataNode(self.get_pkg_data(), self.editors)
        node.factory = self
        return node


    def instantiate_widget(self, node=None, parent=None, edit=False):
        """ Return the corresponding widget initialised with node """

        if(node): editors = node.get_input(1)
        else: editors = self.editors

        # single command
        if(editors and isinstance(editors, str)):
            command = self.editors%(self.get_pkg_data(),)
            os.system(command)

        # multi command
        elif(editors and isinstance(editors, dict)):
            
            from openalea.visualea.dialogs import EditorSelector
            return EditorSelector(parent, self.editors, (self.get_pkg_data(),) )

        else:
            # Code Editor
            from openalea.visualea.code_editor import get_editor
            w = get_editor()(parent)
            w.edit_file(str(self.get_pkg_data()))
            return w 
        
     
    def get_writer(self):
        """ Return the writer class """
 
        return PyDataFactoryWriter(self)


    def clean_files(self):
        """ Remove files depending of factory """
        
        os.remove(str(self.get_pkg_data()))



class DataNode(Node):
    """ Node representing a Data """

    __color__ = (200,200,200)
 
    def __init__(self, packagedata, editors=None):

         Node.__init__(self,
                      inputs=(dict(name='data', interface=IData, value=packagedata),
                              dict(name='editors', interface=None, value=editors),
                              ),
                       outputs=(dict(name='data', interface=IData),),
                       )
         self.caption = 'Data : %s'%(packagedata.name)
        

    def __call__(self, args):
        return str(args[0]),




class PyDataFactoryWriter(object):
    """ DataFactory python Writer """

    datafactory_template = """
$NAME = DataFactory(name=$PNAME, 
                    description=$DESCRIPTION, 
                    )
"""

    def __init__(self, factory):
        self.factory = factory


    def __repr__(self):
        """ Return the python string representation """
        f = self.factory
        fstr = string.Template(self.datafactory_template)
        result = fstr.safe_substitute(NAME=f.get_python_name(),
                                      PNAME=repr(f.name),
                                      DESCRIPTION=repr(f.description),
                                      )
        return result



           
