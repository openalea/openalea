# -*- coding: iso-8859-15 -*-

# Header

#Check dependencies
import sys
from os.path import join as pj

try:
	from openalea import config
	namespace = config.namespace

except ImportError:
	print """
ImportError : openalea.config not found. 
see http://openalea.gforge.inria.fr
"""
	namespace = 'openalea'

try:
	from openalea.distx import setup, find_packages, find_package_dir, Shortcut
except ImportError:
	print """
ImportError : openalea.distx package not found.
See http://openalea.gforge.inria.fr
"""
        sys.exit()


# Package name
name= 'distx_tester'

# Package version 
version= '0.0.1a' 

# Description of the package 
description= 'DistX test package.' #short description
long_description= 'DistX test package'
author= 'Samuel Dufour-Kowalski'
author_email= 'samuel.dufour@sophia.inria.fr'
url= 'http://gforge.inria.fr/projects/openalea/'
license= 'Cecill-C' #LGPL compatible INRIA licence


#MAIN SETUP
setup(

    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    long_description=long_description,
    
    # Execute scons
    # Scons is responsible to put compiled library in the write place ( lib/, package/, etc...)
    scons_scripts = ['SConstruct'],
    scons_parameters = ['lib_dir=lib'],

    namespace=[namespace],

    packages = find_packages(where = 'src', namespace = namespace),
    package_dir = find_package_dir(where = 'src', namespace = namespace),
      
    # Add package platform libraries if any
    include_package_lib = True,
    
    # Copy shared data in default OpenAlea directory
    # Map of 'destination subdirectory' : 'source subdirectory'
    external_data = {pj('external', name) : 'external', },
    
    
    # Add to PATH environment variable for openalea lib
    set_win_var = ['PATH='+pj(config.prefix_dir,'lib'), 'PATH=c:\\testass', 'MAVAR=testass'],
    set_lsb_var = ['LD_LIBRARY_PATH='+pj(config.prefix_dir,'lib'), 'TEST=montest'],

    # Add shortcuts
    win_shortcuts = [Shortcut( name=name, target='c:\\python24\pythonw.exe', arguments='', group='OpenAlea', icon =''), ],
    freedesk_shortcuts = [Shortcut ( name = name, target = 'python', arguments = '', group = 'OpenAlea', icon='' )],

    # Windows registery (list of (key, subkey, name, value))
    winreg = [ ('HKCR', '.aaa', '', 'AAAA FILE') ]
   
      )


    
