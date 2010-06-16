################################################################################
# -*- python -*-
#
#       OpenAlea.Deploy : OpenAlea setuptools extension
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
"""
Small functions to manipulate autosum files
"""

from os.path import join,dirname,basename,splitext
from list_modules import list_modules

def generate_autosum (pkg_name, filename) :
	"""Generate an autosum file
	
	Parse all modules in the package and create an entry for them
	using automodule
	
	.. warning:: assert the directory tree of the package is one of:
	              - package_name/src/package_name
	              - package_name/src/openalea/package_name
	
	:Parameters:
	 - `pkg_name` (str) - path of the package as used in the import statement
	                      (e.g. pkg_name = 'openalea.svgdraw')
	 - `filename` (str) - name of the file in which to write the autosum
	"""
	#find package root directory
	exec "import %s as pkg" % pkg_name
	
	pkg_dir = dirname(pkg.__file__)
	pkg_dir_name = basename(pkg_dir)
	
	src_dir = dirname(pkg_dir)
	if basename(src_dir) != "src" : #remove 'openalea' dir if needed
		src_dir = dirname(src_dir)
		pkg_dir = join(src_dir,pkg_dir_name)
	
	txt = """
.. this file is dedicated to the reference guide

.. In order to include a module so that it is automatically documented, it must in your python path

.. In other words, sphinx will automatically create the reference guide (using automodule)
   only if it can import the module.

.. Keep the structure of this file as close as possible to the original one


.. _%s_reference:

Reference guide
###############
.. contents::
""" % pkg_name
	
	modules = []
	
	print pkg_dir
	for mod_name in list_modules(pkg_dir) :
		gr = mod_name.split(".")
		if not gr[-1].startswith("_") \
		   and not gr[-1].endswith("_rc") \
		   and not gr[-1].endswith("_ui") :
			modules.append(gr)
	
	modules.sort()
	
	for mod_dec in modules :
		full_mod_name = ".".join([pkg_name] + mod_dec)
		print full_mod_name
		txt += """
.. currentmodule:: %s
""" % full_mod_name
		title = ":mod:`%s` module" % full_mod_name
		txt += "\n" + title + "\n" + "=" * len(title) + "\n\n"
		txt += """
Download the source file :download:`../../src/%s/%s.py`.
""" % (pkg_dir_name,join(*mod_dec) )
		txt += """

.. automodule:: %s
    :members:
    :undoc-members:
    :show-inheritance:
    :synopsis: doc todo
""" % full_mod_name
	
	f = open(filename,'w')
	f.write(txt)
	f.close()

