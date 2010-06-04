"""
Script creating a valid OpenAlea package layout

Usage:
  python layout.py PKG_NAME [ src_subdirs ]

"""

import sys, re
import getopt
from string import Template

from openalea.core.path import path

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


class PackageBuilder(object):
    """
    Provide methods to build a standard layout package.
    Creates standard directories, files.
    May also build templae setup file and SConstruct.
    """
    good_name = re.compile( "[a-z_]{3,}" )

    def __init__(self, name, dir = '.'):
        self.name = name
        self.dir = dir
        self.pkg_dir = path(dir) / name
        self.languages = ['python']

    def check_name(self):
        """ Check correctness of pkg name. """
        if not self.good_name.match( self.name ):
            print "Error, package name %s is invalid" % ( self.name, )
            return False
        return True

    def mkdirs(self, dirs=None):
        """ Create directories. """
        if not dirs:
            self.set_dirs()
            dirs = self.dirs

        for d in dirs:
            if d.exists():
                print " WARNING: Directory %s already exists ..." % (d,)
                continue

            print "Creating %s ..." % ( d, )
            try:
                d.makedirs()
            except OSError, e:
                if e.args[ 0 ] != 17:
                    raise
            
    def mkfiles(self, files=None):
        """ Create files on the disk. """
        if not files:
            self.set_files()
            files = self.files

        for f in self.files:
            print "Creating %s ..." % ( f, )
            f.touch()

    def set_languages(self, cpp = False, c = False, fortran = False):
        if cpp: 
            self.languages.append('cpp')
        if c:
            self.languages.append('c')
        if fortran:
            self.languages.append('fortran')

    def set_dirs(self,dirs=None):
        if dirs:
            self.dirs = [self.pkg_dir] + dirs
        else:
             self.dirs = [
               self.pkg_dir,
               self.pkg_dir/"src",
               self.pkg_dir/"doc",
               self.pkg_dir/"test",
               self.pkg_dir/"example",
               self.pkg_dir/"share",
               ]

        # alias
        dirs = self.dirs
        wralea_name = self.name+"_wralea"
        if 'python' in self.languages:
            dirs.extend([
               self.pkg_dir/"src"/"openalea"/self.name,
               self.pkg_dir/"src"/"openalea"/wralea_name,
               ])
        if 'cpp' in self.languages:
            dirs.extend([
               self.pkg_dir/"src"/"cpp",
               ])
        if 'c' in self.languages:
            dirs.extend([
               self.pkg_dir/"src"/"c",
               ])
        if 'fortran' in self.languages:
            dirs.extend([
               self.pkg_dir/"src"/"fortran",
               ])

    def set_files(self):
        self.files = [] 
        self.files += self.legalfiles()
        self.files += self.wraleafiles()
        self.files += self.sconsfiles()
        self.files += self.setupfiles()

    def legalfiles(self):
        return [
        self.pkg_dir/"LICENSE.txt",
        self.pkg_dir/"README.txt",
        self.pkg_dir/"ChangeLog.txt",
        self.pkg_dir/"AUTHORS.txt",
        self.pkg_dir/"NEWS.txt",
        self.pkg_dir/"TODO.txt",
        ]

    def wraleafiles(self):
        wralea_name = self.name+"_wralea"
        return [
        self.pkg_dir/"src"/"openalea"/wralea_name/"__init__.py",
        self.pkg_dir/"src"/"openalea"/wralea_name/"__wralea__.py",
        ]

    def sconsfiles(self):
        if 'cpp' in self.languages:
            return [
                    self.pkg_dir/"options.py",
                    self.pkg_dir/"SConstruct",
                    self.pkg_dir/"src"/"cpp"/"SConscript",
                   ]
        else:
            return []

    def setupfiles(self):
        return [
        self.pkg_dir/"setup.py",
        self.pkg_dir/"metainfo.ini",
        ]

    def template_wralea(self):
        files = self.wraleafiles()
        for f in files:
            if "__wralea__.py" in f:
                break
        if not f.exists():
            self.mkfiles(files)
            
        wralea_py = f

        tpl_wralea = path(__file__).dirname()/'template_wralea.txt'

        print tpl_wralea

        wralea_txt = Template(open(tpl_wralea).read())
        wralea_txt = wralea_txt.substitute(NAME=self.name)

        print "Creating a template version for %s ..." % ( wralea_py, )
        f = open(wralea_py, "w")
        f.write(wralea_txt)
        f.close()

    def template_legal(self):
        ''' Build new files from a default one.

        If the template file exist and the current file is empty, create a new one.
        '''
        files = self.legalfiles()
        tpl_files = []
        for f in files:
            if not f.exists() or f.size == 0:
                tpl_file = path(__file__).dirname()/'template_'+f.basename()
                tpl_files.append(tpl_file)
            
        wralea_py = f

        wralea_txt = Template(open(tpl_wralea).read())
        wralea_txt = wralea_txt.substitute(NAME=self.name)

        print "Creating a template version for %s ..." % ( wralea_py, )
        f = open(wralea_py, "w")
        f.write(wralea_txt)
        f.close()
        

    def template_setup(self):
        ''' Build a setup.py and an associated metainfo.ini '''
        files = self.setupfiles()

        tpl_setup = path(__file__).dirname()/'template_setup.txt'
        setup_py = self.pkg_dir/"setup.py"

        if setup_py.exists() and setup_py.size != 0:
            return

        setup_txt = Template(open(tpl_setup).read())
        setup_txt = setup_txt.substitute(HAS_SCONS=bool(self.cpp))
        print "Creating a template version for %s ..." % ( setup_py, )
        f = open(setup_py, "w")
        f.write(setup_txt)
        f.close()

    def template_scons(self):
        ''' Build default SConstruct and SConscript files. '''
        pass


def create( name, 
            python=True, cpp=False, c=False, fortran=False,
            project='openalea', release='0.8' ):

    pkg = PackageLayout(name)
    pkg.set_languages(cpp=cpp, c=c, fortran=fortran)
    pkg.set_project(project)

    if not pkg.check_name():
        print "Error, package name %s is invalid" % ( name, )
        return 1

    pkg.mkdirs()
    pkg.mkfiles()
    pkg.template_wralea()

    return 0

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
  python %s PKG_NAME [ c cpp fortran ]
""" % (argv[0],)
    return 3 

    name = argv[ 1 ]
    languages = argv[ 2: ]

    return create_layout(name, languages)

        
if __name__ == "__main__":
    sys.exit(main())

