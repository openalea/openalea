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
"""Functions used to automatize documentation of code
"""

__license__ = "Cecill-C"
__revision__ = " $Id:$"

from os import remove,tmpnam

def execfile_partial (local_vars, filename,
                      anchor_from = None, anchor_to = None) :
	"""Apply execfile on a subpart of a file
	
	.. seealso:: `execfile` statement in python
	
	:Parameters:
	 - `local_vars` (dict) - usually 'vars()', python dictionary of local
	    variable instances
	 - `filename` (str) - name of the file to execute
	 - `anchor_from` (str) - only the portion of text that start after this
	    string will be executed. If None, starts from the beginning of the file
	 - `anchor_to` (str) - only the portion of text situated before (excluding)
	    this string will be executed. If None, execute the file up to the end
	
	:Returns: None, will modify local_vars
	"""
	#read text
	f = open(filename,'r')
	lines = f.readlines()
	f.close()
	
	#find relevant portions
	start_ind = 0
	if anchor_from is not None :
		while not lines[start_ind].startswith(anchor_from) :
			start_ind += 1
		
		start_ind += 1
	
	if anchor_to is None :
		end_ind = len(lines) + 1
	else :
		end_ind = start_ind + 1
		while not lines[end_ind].startswith(anchor_to) :
			end_ind += 1
	
	#write tmp file
	tmp = "%s.tmp" % tmpnam()
	f = open(tmp,'w')
	for line in lines[start_ind:end_ind] :
		f.write(line)
	
	f.close()
	
	#execfile
	execfile(tmp,local_vars)
	
	#clean file
	remove(tmp)

