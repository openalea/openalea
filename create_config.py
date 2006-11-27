# -*- coding: cp1252 -*-
################################################################################
# -*- python -*-
#
#       OpenAlea.Config :  OpenAlea configuration
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#          http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

__revision__=" $Id$ "
__license__="Cecill-C"

__doc__="""
Create a python module which provide precise description of where
files have to be or had been installed.
Thus, the configuration is not hard coded, but depends on the
generated config.py file.


Usage:
-----
  python create_config.py openalea_prefix=/usr/local/openalea
 or
  python create_config.py openalea_prefix=C:\openalea


Configuration file provides:
---------------------------
 * Naming information 
   + `namespace`: python package namespace.
   + `version`: OpenAlea version number

 * Directory information
   + `prefix_dir`: prefix directory.
   + `lib_dir`: library directory for shared lib of OpenAlea packages
   + `include_dir`: include base directory for each package include directoy.
   + `bin_dir`: binary directory

* Other optional directory
   + `doc_dir`: documentation directory.
   + `test_dir`: test directory.
   + `setting_dir`: setting directory.

"""

import sys
import os
import time
from optparse import OptionParser

def pj(*args):
    if args[-1] == "":
        return os.path.join(*args[:-1])
    else:
        return os.path.join(*args)

class Config(object):
    """
    Platform independant configuration information and utilities.
    """
    namespace= 'openalea'
    version= '0.1.0'
    
    lib_dir='lib'
    include_dir='include'
    bin_dir='bin'

    doc_dir='doc'
    test_dir='test'
    setting_dir= ""    

    header= '# OpenAlea config file generated on %s'%( time.asctime(),)

    def __str__(self):
        return """
%s
namespace= '%s'
version= '%s'
prefix_dir= r'%s'
lib_dir= r'%s'
include_dir= r'%s'
bin_dir= r'%s'

doc_dir=r'%s'
test_dir=r'%s'
setting_dir=r'%s'     

"""%( self.header, self.namespace, self.version,
      self.prefix_dir,
      pj(self.prefix_dir, self.lib_dir),
      pj(self.prefix_dir, self.include_dir),
      pj(self.prefix_dir, self.bin_dir),
      pj(self.prefix_dir, self.doc_dir),
      pj(self.prefix_dir, self.test_dir),
      pj(self.prefix_dir, self.setting_dir))
            
    def write(self, fn):
        """ Write config file `fn`. """
        try:
            f= open(fn, 'w')
            f.write(str(self))
            print " Create %s" % (fn,)
            f.close()
        except:
            raise Exception( "Can not write on file %s"%(fn,) )

    def create_namespace(self):
        if not os.path.exists(self.namespace):
            print " Create %s directory" % (self.namespace,)
            os.mkdir(self.namespace)
        else:
            print " !! Warning: %s directory already exists" % (self.namespace,)

        fn= pj(self.namespace, "__init__.py")
        f= open(fn,'w')
        print " Create %s file " % (fn,)
        f.close()



class PosixConfig(Config):
    """
    Specific  configuration information and utilities for POSIX platform.
    """
    prefix_dir='/usr/local/openalea'

    def __init__(self, prefix= prefix_dir):
        if(prefix):
            self.prefix_dir= prefix

class WindowsConfig(Config):
    """
    Specific  configuration information and utilities for Windows platform.
    """
    prefix_dir=pj('C:/', 'openalea')
    
    def __init__(self, prefix= prefix_dir):
        if(prefix):
            self.prefix_dir= prefix
    

def config( prefix ):
    """Return the config object for the local platform"""
    
    platform= sys.platform
    if 'win' in platform:
        return WindowsConfig(prefix)
    else:
        return PosixConfig(prefix)

    

def main():

    #parse options
    parser= OptionParser()

    #prefix options
    parser.add_option( "--prefix", dest="prefix",
                  help="OpenAlea prefix directory")
    (options, args)= parser.parse_args()

    prefix= options.prefix
    if prefix: 
        print " prefix= "+prefix

    #get config object
    conf=config(prefix)

    #create config file
    conf.create_namespace()
    conf.write(pj(conf.namespace,'config.py'))


if __name__ == '__main__':
    main()
