"""Script to automatically generate epydoc documentation of the openalea and
vplants modules.

.. warning :: documentation currently moving to sphinx. This module becomes 
    deprecated

"""

__author__ = "Thomas.Cokelaer@sophia.inria.fr"
__revision__ = "$Id$"

import os
import sys
from optparse import OptionParser

# do not change anything below in principle !
epydoc_options = """
--html
--name "OpenAlea API"
--docformat restructuredtext
--graph all
--url http://openalea.gforge.inria.fr
--include-log
--show-sourcecode
"""


def run(cmd, verbose=True, test=True):
    """Simple run command alias

    :param verbose: set the verbose option to True (default) or False.
    :param test: set the test option to True (default) or False.

    If verbose is True, we print the command on the screen.
    If test if True then the command is not run.

    So, setting verbose and test arguments to True  allows to see the commands
    that will be run without launching them.
    """
    if verbose:
        print cmd
    if not test:
        os.system(cmd)


class GenDoc():
    """Provides functionalities to create epydoc documents of a module

    >>> factory = GenDoc(opts)
    >>> factory.getfiles()
    >>> run('epydoc %s -o %s %s ' %
    >>>      (factory.options, factory.outdir, factory.files))

    This class encapsulates several data structure:

    - parent is the parent directory of openalea (to get version numbers)
    - options contains the list of epydoc options
    - outdir is the directory where to save the HTML files
    - files is a list of python files to parse

    """

    def __init__(self, opts):
        """
        :param opts: an optparse structure
        """
        # todo : make it robust to look in ./module/src/module or
        # ./module/src/openalea/module        
        self.parent = os.path.abspath(opts.parent_directory) +'/'

        # make it robust with respect to commas, spaces
        self._setOutputDirectory(opts)

        # the files to parse
        self.files = []

        # set epydoc options
        self.options = ' '.join(epydoc_options.split())
        if opts.verbose:
            self.options += ' -v '
        if opts.extra_epydoc_options:
            self.options += opts.extra_epydoc_options

    def _setOutputDirectory(self, opts):
        """todo"""
        # this statement must be done once the parent directory is set.
        sys.path.append(os.path.abspath(self.parent + './core/src/core')) # to get the release version
        try:
            import version
            version = version.version
        except:
            version= "x"
        self.list_module = opts.module.split(',')
        if len(self.list_module)==1:
            self.outdir = self.parent + opts.module + '/doc/' + opts.module \
                + "-%s"%(version) # where to copy the API
        else:
            self.outdir = self.parent + '/doc/'
            print self.outdir

    def getModulePath(self, module):
        """Returns the module's path"""

        module_path = self.parent +module +'/src/' +module # the python files location

        if not os.path.isdir(module_path):
            module_path = self.parent + module +'/src/openalea/' + module
        if not os.path.isdir(module_path):
            module_path = self.parent + module +'/src/openalea/'
        if not os.path.isdir(module_path):
            raise IOError

        return module_path

    def getfiles(self):
        """read recursively all python files in a directory and returns a string"""
        from openalea.core.path import path

        for module in self.list_module:
            print 'Globbing files in %s.' % module
            module_path = self.getModulePath(module)
            directory = path(module_path)
            files_in_this_module = directory.walkfiles('*.py')
            self.files += files_in_this_module

        list = ""
        for file in self.files:
            if "__wralea__.py" not in file and "__init__.py" not in file:
                list += ' ' + file
        self.files = list

    # to be done !!!!!

    def exclude(self, exclude_pattern):
        if len(exclude_pattern):
            self.options += "  --exclude "
            for elt in exclude_pattern:
                self.options += elt + " "


def ParseParameters():
    """This is the main parsing function to get user arguments

    Launch this script with --help arguments to print all the options help

    Example:
      >>> python gendoc.py --module core --parent-directory . --verbose
    """

    usage = """Usage: %prog [options]

    This script generates the epydoc API of a module, copy it into ./module_name/doc-release
    and scp the content on the gforge URL at
          scm.gforge.inria.fr:/home/groups/openalea/htdocs/doc/

    Example:
      >>> python gendoc.py --module core --parent-directory . --verbose

    """
    parser = OptionParser(usage=usage, \
        version="%prog CVS $Id$ \n" \
      + "$Name:  $\n")
    parser.add_option("-m", "--module", \
        default=None, help="name of the module. E.g., core, visualea, stdlib")
    parser.add_option("-d", "--parent-directory", \
        default=None, action="store", type="string",
        help="give the parent directory where is the module. API doc will be copied in parent_directory/module/doc")
    parser.add_option("-v", "--verbose", action="store_true", \
        default=False, help="verbose option")
    parser.add_option("-t", "--test", action="store_true", \
        default=False, help="do not launch the command, just print them on the screen")
    parser.add_option("-p", "--skip-pdf", action="store_true", \
        default=False, help="do not create the PDF files")
    parser.add_option("-s", "--skip-html", action="store_true", \
        default=False, help="do not create the HTML files")
    parser.add_option("-c", "--skip-scp", action="store_true", \
        default=False, help="do not scp files")
    parser.add_option("-a", "--extra-epydoc-options", \
        default=False, help="add extra epydoc options")

    (opts, args) = parser.parse_args()
    #checking 
    if not os.path.isdir(opts.parent_directory):
         raise ValueError, "--parent-directory must be a valid directory"
    if not opts.module or not opts.parent_directory:
         raise ValueError, "--parent-directory and --module must be provided"
    return opts, args


if __name__ == '__main__':
    # get all python files
    (opts, args) = ParseParameters()

    factory = GenDoc(opts)
    factory.getfiles()
    # to be done
    #factory.exclude(['*pyc'])  # example of file to exclude from the parsing


    # the actual commands
    print '=================Starting EPYDOC command=============== '
    if not opts.skip_html:
        run('epydoc %s -o %s %s  ' % (factory.options, factory.outdir, factory.files),
            verbose=opts.verbose, test=opts.test)

    print '=================Starting EPYDOC command=============== '
    if not opts.skip_pdf:
        run('epydoc %s -o %s %s --pdf ' %
            (factory.options.replace('--include-log', ''),
            factory.outdir, factory.files),
            verbose=opts.verbose, test=opts.test)

    print '=================Starting SCP command=============== '
    # once done, we can scp the documentation
    if not opts.skip_scp:
        run('scp -r %s scm.gforge.inria.fr:/home/groups/openalea/htdocs/doc/'
            % (factory.outdir), verbose=opts.verbose, test=opts.test)
