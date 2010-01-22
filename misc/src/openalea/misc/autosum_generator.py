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
Small functions to manipulate autosum files
"""

from os.path import join,dirname,basename,splitext
from list_modules import list_modules

def generate_autosum (user_doc_path) :
	"""Generate an autosum file
	
	Parse all modules in the package
	and create an entry for them
	using automodule
	
	:Returns Type: str
	"""
	pkg_root = dirname(dirname(user_doc_path) )
	pkg_name = basename(pkg_root)
	
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
	
	for mod_name in list_modules(join(pkg_root,"src",pkg_name) ) :
		gr = mod_name.split(".")
		if not gr[-1].startswith("_") \
		   and not gr[-1].endswith("_rc") :
			modules.append([pkg_name] + gr)
	
	modules.sort()
	
	for mod_dec in modules :
		full_mod_name = ".".join(mod_dec)
		print full_mod_name
		txt += """
.. currentmodule:: openalea.%s
""" % full_mod_name
		title = ":mod:`openalea.%s` module" % full_mod_name
		txt += "\n" + title + "\n" + "=" * len(title) + "\n\n"
		txt += """
Download the source file :download:`../../src/%s.py`.
""" % join(*mod_dec)
		txt += """

.. automodule:: openalea.%s
    :members:
    :undoc-members:
    :show-inheritance:
    :synopsis: doc todo
""" % full_mod_name
	
	return txt

