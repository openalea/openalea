# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
""" openalea.image """

__revision__ = " $Id: __wralea__.py 2245 2010-02-08 17:11:34Z cokelaer $ "

from os.path import join
from glob import glob

def register_frames (viewer, step, im_path, name_template) :
	"""Save a snapshot of viewer content
	"""
	if viewer is not None and viewer.isVisible() :
		imname = join(im_path,name_template % step)
		viewer.saveSnapshot(imname)
	else :
		imname = ""
		print "open viewer first :)"
	
	return imname,

def frame_list (im_path, name_template) :
	"""Construct the ordered list of files that obey name_template
	"""
	if "%" in name_template :
		ind1 = name_template.index("%")
		try :
			ind2 = name_template.index("d",ind1)
		except ValueError :
			raise UserWarning("invalid template %s" % name_template)
		tpl = name_template[:ind1] + "*" + name_template[ind2 + 1:]
	else :
		tpl = name_template
	
	files = glob(join(im_path,tpl) )
	files.sort()
	
	return files,




