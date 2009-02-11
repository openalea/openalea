"""
Script to automatically generate sphinx documentation of an openalea package.

 
Example:

>>> python sphinx_tools 
    --package core 
    --parent-directory /home/user/openalea/core
    --verbose
    --project openalea
    --inheritance

..todo ::
    - create a python script with all the import needed, which can be read by conf.py
      in order to prevent issues with metaclass when create inheritance diagrams
"""
__author__ = "Thomas.Cokelaer@sophia.inria.fr"
__revision__ = "$Id: gendoc.py 1586 2009-01-30 15:56:25Z cokelaer $"

import os
import sys
from optparse import OptionParser

# Some template to include in the reST files.


template_release = \
""".. _%(reference)s_release:

%(title)s

:Version: |version|
:Release: |release|
:Date: |today|

.. versionadded:: x.y.z
   to be filled
   
"""


template_index = \
""".. _%(package)s_%(type1)s:


%(title)s

:Version: |version|
:Release: |release|
:Date: |today|

This reference manual details functions, modules, and objects include in 
%(project)s.%(package)s, describing what they are and what they do. For learning
how to use %(project)s.%(package)s see :ref:`%(package)s_%(type2)s`.

.. warning::

   This "Reference Guide" is still very much work in progress; the material
   is not organized, and many aspects of %(project)s.%(package)s are not 
   covered.

   More documentation can be found on the
   `openalea <http://openalea.gforge.inria.fr>`__ wiki.

.. toctree::
    :maxdepth: 1
"""

template_source = \
"""
%(underline)s

.. module:: %(title)s

.. note:: This source code is not included in the LaTeX output file.

.. htmlonly::
    .. literalinclude:: %(fullpathname)s
        :linenos:
        :language: python
"""

template_reference = \
""".. module:: %(module)s
    :synopsis: todo
    
%(title)s

Description
***********

.. htmlonly::

    This documentation is automatically extracted from the docstrings contained 
    in the python modules. 

.. toctree::

    %(import_name_underscored)s_src.rst

Reference
********* 

- Inheritance diagram:

.. inheritance-diagram:: %(import_name_for_diagram)s
    :parts: 2

------

.. automodule:: %(import_name)s
    :members:
    :undoc-members:%(inheritance)s
    :show-inheritance:     
"""



def underline(text, symbol='^'):
    """
    print the text and an underline with the input symbol
    
    :param text: the text to print and underline
    :param symbol: symbol use to create the underline
    """
    _underline = text + '\n'
    for _c in text:
        _underline += symbol
    #underline+='\n'
    return _underline


def contains(this_file, words):
    """check the existence of kwywords such as class and def in a file
    """
    text = open(this_file,'r').read()
    lines = text.split('\n')
     
    for line in lines:
        # remove all data after the # (including the #)
#        line = [0:line.find('#')]
#        print line
        for word in words:
            if word+' ' in line:
                # remove all spaces. The class keyword should then be first,
                # otherwise, it is either commented or a different 
                # keyword (e.g., metaclass)
                line = line.replace(' ','')
                if line.startswith(word):
                    return True
              
    return False



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


class Globber():
    """ This is a simple class to get the list of python 
    files contained in a directory and its sub-directories.
    
    It excludes the __init__ and __wralea__ files.
    
    The :func:`exclude` function allows to exclude more files, 
    
    The :func:`exclude_non_code` function excludes files that contains 
    no functions
    """
    
    def __init__(self, package=None, path=None, verbose=True):        
        self.path = path
        self.package = package 
        self.verbose = verbose
        self.files = []
        
    def __len__(self):
        return len(self.files)
                 
    def getfiles(self):
        """return list of python files to be scanned

        .. note:: do not include __init__ and __wralea__ file
        """ 
        from openalea.core.path import path

        if self.verbose:
            print 'Globbing files in package %s.' % self.package
            print 'in directory %s' % self.path    
            
        _directory = path(self.path)
        self.files = _directory.walkfiles('*.py')
        
        _list = []
        for this_file in self.files:
            if "__wralea__.py" not in this_file and \
                "__init__.py" not in this_file:
                _list.append(str(this_file))
        
        self.files = _list
        self.print_len()
        return self.files
    
    def exclude_files(self, pattern):
        """Remove files that match the pattern

        .. note:: Changes self.files

        :param pattern: pattern to match 
        """
        # make a copy to loop over the original list
        _copy = self.files[:]
        
        for this_file in _copy:
            if pattern in this_file:
                self.files.remove(this_file)

        self.print_len(pattern=pattern)
        
    def print_len(self, pattern=None):
        """alias to print the number of files"""
        if self.verbose:
            if pattern:
                print 'Remains %i files after exclusion of the pattern \'%s\'' \
                    % (self.__len__(), pattern)
            else:
                print 'Found %i files to parse' % self.__len__()

    def exclude_non_code(self):
        """do not consider files that contain neither classes nor 
        definitions

        ..note :: changes self.file 
        """
        _copy = self.files[:]
        for this_file in _copy:            
            if not contains(this_file, ['class', 'def']):
                self.files.remove(this_file)
                
        self.print_len(self)

        
class reST():
    """A class to generate reST code (API reference)."""
    
    def __init__(self, 
                 fullname, package=None, project=None,
                 parent_directory=None):
        """todo"""
        self.fullname = fullname
        self.filename = os.path.split(self.fullname)[1]
        self.module = self.filename.split('.')[0]
        self.text_reference = ""
        self.text_source = ""
        
        self.package = package
        self.project = project
        
        self.path = os.path.join(parent_directory, 'doc',  self.package) 
        self.title = self.project + '.' + self.package + '.' + self.module
        self.import_name ='to be done in next call'
        self.get_path_to_module(delimiter=self.project)
        
                                                
    def get_path_to_module(self, delimiter='openalea'):
        """Create the import name """
        
        openalea_packages = ['core', 'stdlib']
        
        if self.project == 'openalea' and self.package in openalea_packages:
            
            _module = self.fullname.split(self.package+'/src')[1]
            _module = _module.replace('.py','') # has to be at the beginning
            _module = _module.replace('openalea/', '.')
            _module = _module.replace('/', '.')
            _module = _module.replace('..', '.')
            self.import_name = 'openalea' + _module            
        else:
            raise 'Combinaison of package and module not implemented' 
                   
    def _create_text_reference(self):
        """todo"""
        a = underline(self.import_name,'#')
        if opts.inheritance:
            inheritance = "\n    :inherited-members:"
            if contains(self.fullname, ['class']):
                import_name_for_diagram = self.import_name
            else:
                import_name_for_diagram = ''
        else: 
            inheritance='' 
            import_name_for_diagram = ''
        
                
        _params = {
                "module": self.module, 
                "title": underline(self.import_name + " API", '#'),                  
                "import_name_underscored": self.import_name.replace('.','_'),
                "import_name_for_diagram": import_name_for_diagram,
                "import_name": self.import_name, 
                "inheritance":inheritance
                  }
        self.text_reference = template_reference % _params

    def _create_text_source(self):
        """todo"""       
        _params = {
              "title": self.title, 
              "underline": underline("Source file", '#'),                  
              "fullpathname": self.fullname,
              }

        self.text_source = template_source % _params

    def write_reference(self):
        """todo"""
        
        # fill the string with missing values  
        self._create_text_reference()        
        # save the resulting string in a text
        _stem = self.import_name.replace('.','_')                
        _output = open(self.path +'/'+ _stem + '_ref.rst' , "w")
        _output.write(self.text_reference)
        _output.close()
        
    def write_source(self):
        """todo"""
        # fill the string with missing values
        self._create_text_source()
        # save the resulting string in a text
        _stem = self.import_name.replace('.', '_')
        _output = open(self.path +'/'+ _stem + '_src.rst' , "w")
        _output.write(self.text_source)
        _output.close()
        

def ParseParameters():
    """This is the main parsing function to get user arguments

    Example:
    >>> python sphinx_tools.py --module core --parent-directory . --verbose
    """

    usage = """Usage: %prog [options]

    This script generates the epydoc API of a module, copy it into ./module_name/doc-release
    and scp the content on the gforge URL at
          scm.gforge.inria.fr:/home/groups/openalea/htdocs/doc/

    Example:
    >>> python sphinx_tools.py --project openalea --package core --parent-directory ./ --verbose

    >>> python sphinx_tools.py --help

    """
    parser = OptionParser(usage=usage, \
        version = "%prog CVS $Id: gendoc.py 1586 2009-01-30 15:56:25Z cokelaer $ \n" \
      + "$Name:  $\n")

    parser.add_option("-m", "--package", metavar='PACKAGE',
        default=None, 
        type='string',
        help="name of the module. E.g., core, visualea, stdlib")

    parser.add_option("-d", "--parent-directory", metavar='PARENT_DIRECTORY',
        default=None, 
        action="store", 
        type="string",
        help="give the parent directory where is the package.\
        API doc will be copied in parent_directory/module/doc")

    parser.add_option("-v", "--verbose", 
        action="store_true", 
        default=False, 
        help="verbose option")
    
    parser.add_option("-i", "--inheritance", 
        action="store_true", 
        default=False, 
        help="set inhereted-members in the module autodocumentation")


    parser.add_option("-n", "--project",  metavar='PROJECT',
        default=None,
        help="the project in which is contained the package <openalea, vplants, alinea>")
    
    (_opts, _args) = parser.parse_args()
     
    if not opts.project:
        print "--project must be provided! type --help to get help"
        sys.exit()
   
    if not opts.package:
        print "--package must be provided! type --help to get help"
        exit()
    
    if not opts.parent_directory:
        print "--parent-directory must be provided! type --help to get help"
        exit()
     
    return _opts, _args


if __name__ == '__main__':
    # get all python files
    (opts, args) = ParseParameters()

    parent_directory = opts.parent_directory

    path = os.path.abspath(parent_directory)
    
    # create an instance
    globber = Globber(path=path, package=opts.package, verbose=opts.verbose)    
    # extract the python files
    globber.getfiles()
    # exclude some files
    globber.exclude_files('test')
    globber.exclude_files('/doc/')
    globber.exclude_files('/build/')
    globber.exclude_files('setup.py')
    globber.exclude_non_code()
    
    output_dir = parent_directory + '/doc/' + opts.package
    
    # create the reST output
    try:        
        os.mkdir(output_dir)
    except:
        print 'Directory %s already existing. ' % output_dir
        print 'Copying reSt files into %s.' % output_dir
    
    # create the indivual file for each module
    foutput = open(output_dir + '/import_modules.py','w')
    for item in globber.files:    
        output = reST(item, opts.package, opts.project, parent_directory)
        output.write_reference()
        output.write_source()
        foutput.write('import ' + output.import_name + '\n')
    foutput.close()
        
    print '.',
    # create the reST file linking to all individual files
    globber.files.sort()
    
    
    
    for item in globber.files:
        output = reST(item, 
                      package=opts.package, 
                      project=opts.project, 
                      parent_directory=parent_directory)
        
        
    # create the index for the reference and user guides
    foutput_ref = open(output_dir + '/reference_index.rst', 'w')
    foutput_user = open(output_dir + '/user_index.rst', 'w')
                    
    params_ref = {'title': underline(opts.package.capitalize() + ' Reference Guide', '#'),
                  'package': opts.package,
                  'project': opts.project.capitalize(),
                  'reference': opts.package,
                  'type1':'reference','type2':'user'}

    params_user = {'title': underline(opts.package.capitalize() + ' User Guide', '#'),
                  'package': opts.package,
                  'project': opts.project.capitalize(),
                  'reference': opts.package,
                  'type1':'user','type2':'reference'}

    foutput_ref.write(template_index % params_ref)
    foutput_user.write(template_index % params_user)
    
    foutput_ref.write('\n')
    foutput_user.write('\n')
            
    for item in globber.files:   
        data = reST(item,
                    opts.package, 
                    opts.project, 
                    opts.parent_directory)
         
        foutput_ref.write('    ' + data.import_name.replace('.', '_') +  '_ref.rst\n')
    foutput_ref.close()
    foutput_user.close()
    
    # create the release
    foutput = open(output_dir + '/release.rst', 'w')
    params = {'title': underline(opts.package.capitalize() + ' Release', '#'),
              'package': opts.package.capitalize(),
              'project': opts.project,
              'reference': opts.package}

    foutput.write(template_release % params)
    foutput.close()
    
    print 'Done'
