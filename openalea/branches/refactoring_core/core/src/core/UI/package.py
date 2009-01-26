# -*- python -*-
#
#       OpenAlea.Core.UI: OpenAlea Interfaces 
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Fred Theveny <theveny@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
This module define a User Interface for a Package
"""

__license__= "Cecill-C"
__revision__=" $Id: observer.py 229 2007-01-22 10:17:17Z tyvokka-toufou $ "

###############################################################################

class Package (object) :
	"""
	User Interface for packages
	"""
	def __init__ (self, name, metainfo) :
		raise RuntimeError()
	
	#######################################################
	#
	#		Package Acces
	#
	#######################################################
	def name (self) :
		raise RuntimeError()
	
	def metainfo (self, keyname) :
		raise RuntimeError()
	
	#######################################################
	#
	#		ObjectType Acces
	#
	#######################################################
	def instantiate (self, object_name) :
		"""
		Instantiate a node from his name
		"""
		raise RuntimeError()
	
	#######################################################
	#
	#		Mutable Concept
	#
	#######################################################
	def add_type (self, object_type) :
		"""
		Add a new type of object to the package
		"""
		raise RuntimeError()
	
	def add_from_instance (self, object_instance) :
		"""
		Add a new type of object to the package
		"""
		raise RuntimeError()
	

