
# This file should be mianted by the administrators only; not the users or developpers.
# New functionalities and options should be handled by sphinx.ini, 
# openalea/doc/common.ini and misc/sphinx_tools.py  files.
# This file is execfile()d with the current directory set to its containing dir.

import sys, os
import time
import ConfigParser
import warnings

sys.path.append(os.path.join('../'))

print "Reading configuration file conf.py"
# Check that sphinx version is correct
try:
    import sphinx
except ImportError, e:
    print e
    print 'Could not find sphinx on your system'
else:
    if float(sphinx.__version__) < 0.6:
        print 'Sphinx 0.6 or higher required. found %s' % sphinx.__version__
        sys.exit(0)


# get year
year = time.ctime().split()[4]

# Get the metadata from sphinx.ini -------------------------------------------
print "...Reading sphinx.ini file"
config = ConfigParser.RawConfigParser()
config.read('sphinx.ini')
section = 'metadata'
for option in config.options(section):
    print '...%s %s' % (option, config.get(section, option))
    exec( ' '.join([option, "=", "'" + config.get(section, option) + "'"]) )
# Check that we have the release 
try:
    Project = project.capitalize()
    Package = package.capitalize()
    version = version # just to check it exsits
    release = release # just to check it exists
    api = api           # check if it exists
    intersphinx = intersphinx
except NameError:
    """
Please, provide the \'api\', \'version\', \'release\', \'project\', 
\'package\'variable within your setup.py file
"""



# set project path -----------------------------------------------------------
# TODO: make it robust
if project=='openalea':
    openalea = os.path.join(os.getcwd(), '../../')
elif project=='vplants':
    openalea = os.path.join(os.getcwd() , '../../openalea/')
elif project=='alinea':
    openalea = os.path.join(os.getcwd() , '../../alinea/')
else:
    print "openalea path not implemented yet for this configuration. FIXME"

# create all the API documentation automatically (ref+src)
# TODO: clean up this piece of code
if api=='automated':
    warnings.warn('API automatically generated. To avoid it, change the api option in sphinx.ini')
    try:
        cmd = 'python ' + os.path.join(openalea, 'misc/sphinx_tools.py --project %s --package %s --verbose --inheritance' %(project, package))
        status = os.system(cmd)
    except:
        print 'sphinx_tools call failed'
        sys.exit()



# read common parameters -----------------------------------------------------
print "...Reading common.ini file"
config = ConfigParser.RawConfigParser()
config.read(os.path.join(openalea, 'doc/common.ini'))

# Read sections: general, HTML, Latex
for section in config.sections():
    print "......Parsing section '%s' found in common.ini file. " % section ,
    for option in config.options(section):
        exec( ' '.join([option, "=", config.get(section, option)]) )
    print 'done'

# Set the extensions --------------------------------------------------------- 
# These paths are required to access extensions
print "...Setting the extensions"
sys.path.append(os.path.join(openalea , 'doc/sphinxext'))
sys.path.append(os.path.join(openalea , 'doc/sphinxext/numpyext'))
sys.path.append(os.path.join(openalea , package , 'src'))
import ipython_console_highlighting

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest', 
    'sphinx.ext.intersphinx',
    'inheritance_diagram', 
    'sphinx.ext.pngmath',
    'sphinx.ext.todo', 
    'numpydoc',
    'phantom_import', 
    'autosummary',
    'sphinx.ext.coverage',
    'only_directives'
    ]

# Example configuration for intersphinx: refer to the Python standard library.
try:
    if intersphinx is not 'True':
        intersphinx_mapping = {}
except:
    pass
