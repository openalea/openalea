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

class FormatError(Exception):
    def __init__(self, str):
        Exception.__init__(self, str)

################################################################################

# READERS


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


class PackageWriter(object)
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
        wraleamodule = imp.load_module(modulename, file, pathname, desc)

        wraleamodule.register_packages( pkgmanager )
        
        if(file) :
            file.close()


class PyPackageWriter(object):
    """ Write a wralea python file """

    def __init__(self, package):
        """ Package to write """

        self.package = package

    def get_factory_str(self):
        """ Return a string with all factory declaration """

        # generate code for each factory
        result_str = ""
        for f in  package.values():
            fstr = string.Template(factory_tpl)
            fstr.safe_subtitute(NAME=f.name,
                                DESCRIPTION=f.description,
                                CATEGORY=f.category, 
                                NODEMODULE=f.nodemodule_name,
                                NODECLASS=f.nodeclass_name,
                                WIDGETMODULE=f.widgetmodule_name,
                                WIDGETCLASS=f.widgetclass_name,
            result_str += fstr

        return result_str


    def get_package_str(self):
        """ Return a string with the package declaration """

        fstr = self.get_factory_str()
        
        pstr = string.Template(pkg_tpl)
        pstr.safe_subtitute(**self.package.metainfo)
        pstr.safe_subtitute(PKGNAME = self.package.name)
        pstr.safe_subtitute(FACTORY_DECLARATION = fstr)

        return pstr


    def write(self, filehandle):
        """ Write package data to file hnalde in python """


        



wralea_tpl = """
# This file has been generated at $TIME

from openalea.core import *

def register_packages(pkgmanager):

    $PKG_DECLARATION

"""

pkg_tpl = """

    metainfo= dict(version="$VERSION",
                   license="$LICENSE",
                   authors="$AUTHORS",
                   institutes="$INSTITUTES",
                   description="$DESCRIPTION",
                   url="$URL"
               }

    package = Package( $PKGNAME, metainfo)

    $FACTORY_DECLARATION
    
    pkgmanager.add_package(package)

"""

factory_tpl = """

    nf = Factory( name= "$NAME", 
                  description= "$DESCRIPTION", 
                  category = "$CATEGORY", 
                  nodemodule = "$NODEMODULE",
                  nodeclass = "$NODECLASS",
                  widgetmodule = "$WIDGETMODULE",
                  widgetclass = "$WIDGETCLASS",
                  )

    package.add_factory( nf )


"""






# class SessionWriter(XmlWriter):
#     """ Class to write the Session in a XML structure """

#     def __init__(self, session):
#         """
#         Constructor:
#         @param session : a session instance
#         """
#         self.session = session
        

#     def fill_structure(self, newdoc, top_element):
#         """ Fill XML structure in newdoc with top_element as Root """

     

