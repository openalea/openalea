"""
Script creating a valid OpenALEA package layout

Usage:
  python layout.py PKG_NAME [ src_subdirs ]

"""

import sys, re
import getopt

from openalea.core.path import path

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    """
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
        # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2
    """
    if argv is None:
        argv = sys.argv

    # Argument parsing
    if len( argv ) < 2:
        print """
Usage:
  python %s PKG_NAME [ src_subdirs ]
""" % (argv[0],)
    return 3 

    name = argv[ 1 ]
    src_subdirs = argv[ 2: ]

    return create_layout(name, src_subdirs)


def create_layout( name, src_subdirs ):

    good_name = re.compile( "[a-z_]{4,}" )

    here = path.getcwd()

    if not good_name.match( name ):
        print "Error, package name %s is invalid" % ( name, )
        return 1

    pkg_dir = here / name

    print pkg_dir

    if pkg_dir.exists():
        print "Warning, the directory %s already exists" % ( pkg_dir, )
        answer = raw_input("Do you want still to continue ? (y/n)\n")
        if answer != "y":
            return 2
    else:
        print "Creating %s ..." % ( pkg_dir, )
        pkg_dir.mkdir(mode=755)

    dirs = [
    pkg_dir/"src",
    pkg_dir/"src"/name,
    pkg_dir/"src"/name/"wralea",
    pkg_dir/"doc",
    pkg_dir/"test",
    pkg_dir/"example",
    ]

    for d in src_subdirs:
        dirs.append( ( pkg_dir/"src"/d ).normpath() )

    for d in dirs:
        print "Creating %s ..." % ( d, )
        try:
            d.mkdir(mode=755)
        except OSError, e:
            if e.args[ 0 ] != 17:
                raise

    files = [
    pkg_dir/"LICENSE.txt",
    pkg_dir/"README.txt",
    pkg_dir/"ChangeLog.txt",
    pkg_dir/"AUTHORS.txt",
    pkg_dir/"NEWS.txt",
    pkg_dir/"TODO.txt",
    pkg_dir/"src"/name/"__init__.py",
    pkg_dir/"src"/name/"wralea"/"wralea.py",
    ]

    for f in files:
        print "Creating %s ..." % ( f, )
        f.touch()

    # Write a sketch of the openalea wrapper file.
    wralea_py = pkg_dir/"src"/name/"wralea"/"wralea.py"
    
    wralea_txt = """
from openalea.core import *

def register_packages(pkgmanager):
    ''' Initialisation function
    
    Return the list of packages to be included in the package manager.
    This function is called by the package manager.
    '''

    metainfo={ 'version' : '0.0.0',
               'license' : 'XXX',
               'authors' : 'XXX',
               'institutes' : 'XXX',
               'description' : 'XXX',
               'url' : 'htp://XXX.org'
               }

    package = Package('%s', metainfo)

    # begin adding Factory after this line.

    # end adding factories

    pkgmanager.add_package(package)

""" % (name,)

    print "Creating a template version for %s ..." % ( wralea_py, )
    f = open(wralea_py, "w")
    f.write(wralea_txt)
    f.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())

