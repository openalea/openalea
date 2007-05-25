# -*- coding: cp1252 -*-
################################################################################
# -*- python -*-
#
#       OpenAlea.Installer :  OpenAlea installation
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#          http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__ = """openAlea Configuration functions
Create a python module which provide precise description of where
files have to be or had been installed.
Thus, the configuration is not hard coded, but depends on the
generated config.py file.

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

__revision__=" $Id: create_config.py 310 2007-01-30 17:38:41Z dufourko $ "
__license__="Cecill-C"

import os
import sys
import time
from os.path import join as pj
from os.path import normpath as np

class Config(object):
    """
    Platform independant configuration information and utilities.
    """
    namespace = 'openalea'
    
    lib_dir = 'lib'
    include_dir = 'include'
    bin_dir = 'bin'

    doc_dir = 'doc'
    test_dir = 'test'
    share_dir = 'share'
    setting_dir = ""    

    header = '# OpenAlea config file generated on %s'%( time.asctime(),)

    def __str__(self):
        return """
%s
namespace = '%s'
prefix_dir = r'%s'
lib_dir = r'%s'
include_dir = r'%s'
bin_dir = r'%s'

doc_dir = r'%s'
test_dir = r'%s'
share_dir = r'%s'
setting_dir = r'%s' 

"""%( self.header, self.namespace, 
      np(self.prefix_dir),
      np(pj(self.prefix_dir, self.lib_dir)),
      np(pj(self.prefix_dir, self.include_dir)),
      np(pj(self.prefix_dir, self.bin_dir)),
      np(pj(self.prefix_dir, self.doc_dir)),
      np(pj(self.prefix_dir, self.test_dir)),
      np(pj(self.prefix_dir, self.share_dir)),
      np(pj(self.prefix_dir, self.setting_dir)))
            
    def write(self, fn):
        """ Write config file `fn`. """
        try:
            f = open(fn, 'w')
            f.write(str(self))
            print " Create %s" % (fn,)
            f.close()
        except Exception, inst:
            print inst
            print "Can not write on file %s, Abording..."%(fn,) 
            exit()

    def create_namespace(self, subdir=''):

        destdir = pj(subdir, self.namespace)
        if not os.path.exists(destdir):
            print " Create %s directory" % (destdir)
            os.mkdir(destdir)

        fn = pj(destdir, "__init__.py")
        f = open(fn,'w')
        print " Create %s file " % (fn,)
        f.close()


class PosixConfig(Config):
    """
    Specific  configuration information and utilities for POSIX platform.
    """
    prefix_dir = '/usr/local/openalea'

class WindowsConfig(Config):
    """
    Specific  configuration information and utilities for Windows platform.
    """
    prefix_dir = pj('C:/', 'openalea')
    

   
def create_config(tmp_dir, prefix = None):
    """
    Create config.py file and namespace
    Return the namespace
    """
    confobj = None
    
    if 'win' in sys.platform and sys.platform != 'cygwin':
        confobj = WindowsConfig()
    else:
        confobj = fPosixConfig()

    # get prefix from the user
    while(not prefix):
        prefix = raw_input('Installation directory [%s] :'%(confobj.prefix_dir))
        prefix.strip()
                           
        if (not prefix) : prefix = confobj.prefix_dir
        try:
            if(not os.path.exists(prefix)):
                os.mkdir(prefix)
            if(not os.path.isdir(prefix)):
                raise Exception("%s is a file, not a directory\n"%(prefix))
        except Exception, inst:
            raise
            print "Cannot create %s. (Check if you need to be root)"%(prefix)
            prefix = None

    confobj.prefix_dir = prefix

    # Create config file
    if(not os.path.exists('tmp')): os.mkdir('tmp')
    confobj.create_namespace("tmp")
    confobj.write(pj("tmp", confobj.namespace,'config.py'))
    return confobj.namespace
    
    
def install_config(tmp_dir, namespace):
    """
    Install namespace and
    configuration file in python
    """

    from distutils.sysconfig import get_python_lib
    from distutils.dir_util import copy_tree, remove_tree

    src = pj(tmp_dir, namespace)
    dst = pj(get_python_lib(), namespace)
    print "copy %s to %s"%(src, dst)
    copy_tree(src, dst)
    remove_tree(tmp_dir)
    

def finalize_config():
    from  openalea import config
    
    # create directories
    print "Creating directories:"
    dirs = (config.prefix_dir,
            config.lib_dir, 
            config.include_dir,
            config.doc_dir,
            config.share_dir,
            config.bin_dir,
            config.test_dir)
	
    for directory in dirs:
        try:
            print directory
            os.mkdir(directory)
        except Exception, e:
            print e

    from installer.setenvvar import set_lsb_env, set_win_env
    
    print "Setting environment variables"

    set_lsb_env('openalea', ['LD_LIBRARY_PATH=%s'%(config.lib_dir,),
                             'PATH=%s'%(config.bin_dir,),
                             'OPENALEADIR=%s'%(config.prefix_dir,)])
    
    set_win_env(['PATH=%s'%(config.lib_dir,),
                 'PATH=%s'%(config.bin_dir,),
                 'OPENALEADIR=%s'%(config.prefix_dir,)])


def start():
    """ Configure OpenAlea """
    ns = create_config('tmp')
    install_config('tmp', ns)
    finalize_config()



