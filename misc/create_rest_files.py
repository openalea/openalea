""" script to launch  rest and postprocessing procedures 

This script launch the sphinx_tools module to create reST files.

Then, postprocessing is started if required.
"""
import os
import sys
sys.path.append(os.path.abspath('../../misc'))
import sphinx_tools # to use the run function
from optparse import OptionParser

__author__ = "Thomas.Cokelaer@sophia.inria.fr"
__revision__ = "$Id$"


# NOTHING to change below -------------------------------

def ParseParameters():
    """main parsing method

    :Example:
    
    >>> python create_rest_files --package stdlib
    """

    usage = """Usage: %prog [options]

    """
    parser = OptionParser(usage=usage, \
        version = "%prog CVS $Id$ \n" \
      + "$Name:  $\n")

    parser.add_option("-m", "--package", metavar='PACKAGE',
        default=None, 
        type='string',
        help="name of the module. E.g., core, visualea, stdlib")

    (_opts, _args) = parser.parse_args()

    if not _opts.package:
        print "--package must be provided! type --help to get help"
        sys.exit()

    if os.path.isdir('../'+ _opts.package):
        print 'Package does not seem to exists in ../'
        print 'Check the spelling'
        sys.exit()
    return _opts, _args

if __name__ == '__main__':
    # get all python files
    (opts, args) = ParseParameters()

    name = opts.package
    print "-----------------------------------------------------------"
    print "Creating the reSt files in ./" + name
    print "Starting the following command: "

    params = {'name': name}
    command = "python ../../misc/sphinx_tools.py --package %(name)s --parent-directory  ../ --verbose --project openalea --inheritance" % params
    sphinx_tools.run(command, verbose=True, test=False)
    print "------------------------------------------------------------"
    print  'Post processing if required'

    if os.path.isfile('postprocess.py'):
        sphinx_tools.run('python postprocess.py', verbose=False, test=False)
    else:
        print 'No postprocess.py file found. continue'
    print 'Normal termination'
    print "------------------------------------------------------------"

