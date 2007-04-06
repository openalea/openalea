# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
This module contains persitence objects
They allow to read and write package declaration
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


from core import Package, NodeFactory
from subgraph import SubGraphFactory
import os
import sys
import imp
import string


################################################################################



class PackageReader(object):
    """ Default base class (define the interface) """

    def __init__(self, filename):
        """ filename : the file path to read"""
        
        self.filename = filename

    def register_packages(self, pkgmanager):
        """ Load packages in pkgmanager """

        # Function must be overloaded
        raise RuntimeError()

    def register_session(self, session):
        """ Load session data """

        # Function must be overloaded
        raise RuntimeError()


class PackageWriter(object):
    """ Default base class (define the interface) """

    def __init__(self):
        pass

    def write(self, filehandle):
        """ Write data to filehandle """
        pass
    
    
    

class PyPackageReader(PackageReader):
    """ Read package as a Python file """

    def __init__(self, filename):
        """  Filename is a wralea.py file """
        
        PackageReader.__init__(self, filename)


    def filename_to_module (self, filename):
        """ Transform the filename ending with .py to the module name """

        # delete the .py at the end
        if(filename.endswith('.py')):
            modulename = filename[:-3]

        l = modulename.split(os.path.sep)
        modulename = '.'.join(l)

        return modulename


    def register_packages(self, pkgmanager):
        """ Execute Wralea.py """

        retlist = []

        basename = os.path.basename(self.filename)
        basedir = os.path.abspath( os.path.dirname( self.filename ))

        if(not basedir in sys.path):
            sys.path.append(basedir)
        
        modulename = self.filename_to_module(basename)

        (file, pathname, desc) = imp.find_module(modulename,  [basedir])

        try:
            wraleamodule = imp.load_module(modulename, file, pathname, desc)
            wraleamodule.register_packages(pkgmanager) 

        except Exception, e:
            print '%s is invalid :'%(self.filename,), e

        
        if(file) :
            file.close()

        


class PyPackageWriter(object):
    """ Write a wralea python file """

    wralea_tpl = """
# This file has been generated at $TIME

from openalea.core import *

def register_packages(pkgmanager):

    $PKG_DECLARATION

"""

    pkg_tpl = """

    metainfo = $METAINFO 

    pkg = UserPackage("$PKGNAME", metainfo, __file__)

    $FACTORY_DECLARATION
    
    pkgmanager.add_package(pkg)

"""

    def __init__(self, package):
        """ Package to write """

        self.package = package
        

    def get_factories_str(self):
        """ Return a string with all factory declaration """

        # generate code for each factory
        result_str = ""
        for f in  self.package.values():
            writer = f.get_writer()
            if(writer):
                result_str += str(writer)
            
        return result_str


    def get_package_str(self):
        """ Return a string with the package declaration """

        fstr = self.get_factories_str()
        pstr = string.Template(self.pkg_tpl)
        
        result = pstr.safe_substitute(PKGNAME=self.package.name,
                                      METAINFO=repr(self.package.metainfo),
                                      FACTORY_DECLARATION=fstr,
                                      )

        return result


    def write(self, filehandler):
        """ Write package description to file handler """

        pstr = self.get_package_str()
        wtpl = string.Template(self.wralea_tpl)
        result = wtpl.safe_substitute(PKG_DECLARATION=pstr)
        filehandler.write(result)
        

    def write_wralea(self, fullfilename):
        """ Write the wralea.py in the specified filename """

        handler = open(fullfilename, 'w')

        self.write(handler)

        handler.close()

        # Recompile
        import py_compile
        py_compile.compile(fullfilename)





class PyNodeFactoryWriter(object):
    """ NodeFactory python Writer """

    nodefactory_tpl = """

    nf = Factory(name="$NAME", 
                 description="$DESCRIPTION", 
                 category="$CATEGORY", 
                 nodemodule="$NODEMODULE",
                 nodeclass="$NODECLASS",
                 widgetmodule="$WIDGETMODULE",
                 widgetclass="$WIDGETCLASS",
                 )

    pkg.add_factory( nf )

"""

    def __init__(self, factory):
        self.factory = factory

    def __repr__(self):
        """ Return the python string representation """
        f = self.factory
        fstr = string.Template(self.nodefactory_tpl)
        result = fstr.safe_substitute(NAME=f.name,
                                      DESCRIPTION=f.description,
                                      CATEGORY=f.category, 
                                      NODEMODULE=f.nodemodule_name,
                                      NODECLASS=f.nodeclass_name,
                                      WIDGETMODULE=f.widgetmodule_name,
                                      WIDGETCLASS=f.widgetclass_name,)
        return result
           


class PySGFactoryWriter(object):
    """ SubGraphFactory python Writer """

    sgfactory_tpl = """

    nf = SubGraphFactory(pkgmanager,
                         name="$NAME", 
                         description="$DESCRIPTION", 
                         category="$CATEGORY",
                         doc="$DOC",
                         nin=$NIN,
                         nout=$NOUT,
                         elt_factory=$ELT_FACTORY,
                         elt_connections=$ELT_CONNECTIONS,
                         elt_data=$ELT_DATA,
                         )

    pkg.add_factory(nf)

"""

    def __init__(self, factory):
        self.factory = factory

    def __repr__(self):
        """ Return the python string representation """
        f = self.factory
        fstr = string.Template(self.sgfactory_tpl)
        result = fstr.safe_substitute(NAME=f.name,
                                      DESCRIPTION=f.description,
                                      CATEGORY=f.category,
                                      DOC=f.doc,
                                      NIN=f.nb_input,
                                      NOUT=f.nb_output,
                                      ELT_FACTORY=repr(f.elt_factory),
                                      ELT_CONNECTIONS=repr(f.connections),
                                      ELT_DATA=repr(f.elt_data),
                                      )
        return result









