# -*- python -*-
#
#       misc: miscellaneous functions
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

"""
Small functions to access packages files
"""

from os import listdir
from os.path import isfile,isdir,join,splitext

def is_package (name) :
	"""Tells wether the given directory
	is a python package.
	
	Look if it finds an '__init__.py' inside
	"""
	return '__init__.py' in listdir(name)

def list_modules (pkgdir) :
	"""List all modules in a package
	
	Parse recursively through all subpackages
	and return each found module as
	pkg.subpkg.module without .py in the end
	
	:Parameters:
	 - `pkgdir` (str) - abs path to head directory
	
	:Returns Type: iter of str
	"""
	for name in listdir(pkgdir) :
		pth = join(pkgdir,name) 
		if isfile(pth) :
			mod_name,ext = splitext(name)
			if ext == ".py" :
				yield mod_name
		elif isdir(pth) :
			if not name.startswith(".") and is_package(pth) :
				for mod_name in list_modules(pth) :
					yield ".".join( (name,mod_name) )

