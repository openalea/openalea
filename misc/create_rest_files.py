""" script to launch  rest and postprocessing procedures 

This script launch the sphinx_tools module to create reST files.

Then, postprocessing is started if required.
"""
import os
import sys
sys.path.append(os.path.abspath('../../misc'))
import sphinx_tools # to use the run function
from optparse import OptionParser
import ConfigParser
import warnings

__author__ = "Thomas.Cokelaer@sophia.inria.fr"
__revision__ = "$Id$"

if __name__ == '__main__':

    
    # get all python files
    config = ConfigParser.RawConfigParser()
    config.read('sphinx.ini')
    try:
        name = config.get('metadata','package')
        project = config.get('metadata','project')
        try:
            api = config.get('metadata','api')
        except:
            print 'api option not found in the sphinx.ini file. You should add one.'      
            api = None
    except Exception, err:
        warnings.warn('Could not find sphinx.ini and/or metadata section. %s' % err)
        sys.exit()
        
    print "-----------------------------------------------------------"
    print "Creating the reST files in ./" + name
    print "Starting the following command: "

    params = {'name': name, 'project': project}
   
     
    if project=='openalea':
        command = "python ../../misc/sphinx_tools.py --package %(name)s --parent-directory  ../ --verbose --project %(project)s --inheritance" % params
    elif project=='vplants':
        command = "python ../../../openalea/misc/sphinx_tools.py --package %(name)s --parent-directory  ../ --verbose --project %(project)s --inheritance" % params
    else:
        print """ERROR: project must be either openalea or vplants. 
Check you sphinx.ini file"""
        sys.exit()

    if api=='automated':
        command += ' --no-index --no-contents '
    else:
        pass

    sphinx_tools.run(command, verbose=True, test=False)

    print "------------------------------------------------------------"
    print  'Post processing if required'

    if os.path.isfile('postprocess.py'):
        sphinx_tools.run('python postprocess.py', verbose=False, test=False)
    else:
        print 'No postprocess.py file found. continue'

    print 'Normal termination'
    print "------------------------------------------------------------"

