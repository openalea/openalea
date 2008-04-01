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
from openalea.core.pkgmanager import PackageManager
from openalea.core.interface import IData

import os


class PackageData(object):
    """ String representing a package data """

    def __init__(self, pkg, name):
        """ 
        pkg : package name 
        name : data name
        """
        self.pkg = pkg
        self.name = name

        path = PackageManager()[self.pkg].path
        self.repr = os.path.join(path, self.name)
        

    def __repr__(self):
        return "PackageData(%s, %s)"%(self.pkg, self.name)

    def __str__(self):
        return self.repr


class DataFactory(AbstractFactory):
    """ Data representation as factory """
    
    #mimetype = "openalea/datafactory"

    def __init__(self,
                 name,
                 description = '',
                 category = '',
                 **kargs):

        AbstractFactory.__init__(self, name, description, category, **kargs)

    
    def instantiate(self, call_stack=[]):
        """ Return a node instance
        @param call_stack : the list of NodeFactory id already in call stack
        (in order to avoir infinite recursion)
        """

        p = PackageData(self.package.name, self.name)
        return DataNode(p)
    

    instantiate_widget = NodeFactory.instantiate_widget

    
    def get_writer(self):
        """ Return the writer class """
        raise NotImplementedError()




class DataNode(Node):
    """ Node representing a Data """
 
    def __init__(self, packagedata):

        # compute path
        v = packagedata

        Node.__init__(self,
                      inputs=(dict(name='data', interface=IData, value=v),),
                      outputs=(dict(name='data', interface=IData),),
                      )
        
        
    def __call__(self, args):
        return args[0],




class DataFactoryWriter(object):
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
        fstr = string.Template(self.nodefactory_template)
        result = fstr.safe_substitute(NAME=f.get_python_name(),
                                      PNAME=repr(f.name),
                                      DESCRIPTION=repr(f.description),
                                      )
        return result



           
