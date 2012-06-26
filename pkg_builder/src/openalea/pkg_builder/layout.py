"""

.. topic:: PackageBuilder

    A module that allows to automatically create a new package

    :Code status: mature
    :Documentation status: mature
    :Author: Christophe Pradal

    :Revision: $Id$

"""

__license__ = "Cecill-C"
__revision__ = " $Id$"

import sys, re
import getopt
from string import Template

from openalea.core.path import path
from optparse import OptionParser


#class Usage(Exception):
#    def __init__(self, msg):
#        self.msg = msg


class PackageBuilder(object):
    """
    Provide methods to build a standard layout package.
    Creates standard directories, files.
    May also build templae setup file and SConstruct.

    :param name: name of the package (directory name, import in python)
    :param package: name as it appears in the egg name e.g., VisuAlea in OpenAlea.VisuAlea
    :param project: a proper project name (openalea/vplants/alinea)
    :param release: a relase version 


    :Usage:

    ::

        pkg = PackageBuilder(name='test', package='Test', projec='openalea', release='0.8')
        pkg.mkdirs()
        pkg.set_files()
        pkg.template_legal()
        pkg.template_setup()
        pkg.template_scons()
        pkg.template_wralea()
        pkg.template_doc()
    """
    good_name = re.compile( "[a-z_]{3,}" )

    project_name = dict(openalea='OpenAlea', vplants='VPlants', alinea='Alinea')

    def __init__(self, name=None, project='', dir = '.', release='0.1'):
        
        self.name = name # e.g. name = PlantGL
        self.package = name.lower() # e.g. name = plantgl
        self.dir = dir
        self.pkg_dir = path(dir) / self.package
        self.languages = ['python']
        self.project = project.lower()
        self.release = release

        self.check_project()

        self.metainfo = {'PACKAGE':self.package,
                        'PACKAGE_NAME':self.name,
                        'PROJECT':self.project,
                        'PROJECT_NAME':self.project_name[self.project] if self.project else '',
                        'RELEASE':self.release,
                }

    def check_project(self):
        """Checks that the project is the official list of projects [openalea, vplants ,alinea]"""
        if self.project and self.project not in self.project_name:
            raise ValueError("wrong project name. should be in openalea/vplants/alinea")

    def check_name(self):
        """ Check correctness of pkg name. """
        if not self.good_name.match( self.package):
            print "Error, package name %s is invalid" % ( self.package, )
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

        for f in files:
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
               self.pkg_dir/"doc"/"user",
               self.pkg_dir/"doc"/"_static",
               self.pkg_dir/"doc"/"_build",
               self.pkg_dir/"test",
               self.pkg_dir/"example",
               self.pkg_dir/"share",
               ]

        # alias
        dirs = self.dirs
        wralea_name = self.package+"_wralea"
        if 'python' in self.languages:
            dirs.extend([
               self.pkg_dir/"src"/self.project/self.package,
               self.pkg_dir/"src"/self.project/wralea_name,
               ])
        if 'cpp' in self.languages:
            dirs.extend([
               self.pkg_dir/"src"/"cpp",
               self.pkg_dir/"src"/"wrapper",
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
        self.files = [self.pkg_dir/"src"/self.project/self.package/'__init__.py'] 
        if self.project:
            self.files.append(self.pkg_dir/"src"/self.project/'__init__.py')
        self.files += self.legalfiles()
        self.files += self.wraleafiles()
        self.files += self.sconsfiles()
        self.files += self.setupfiles()
        self.files += self.docfiles()

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
        wralea_name = self.package+"_wralea"
        return [
        self.pkg_dir/"src"/self.project/wralea_name/"__init__.py",
        self.pkg_dir/"src"/self.project/wralea_name/"__wralea__.py",
        ]

    def sconsfiles(self):
        if 'cpp' in self.languages:
            return [
                    self.pkg_dir/"options.py",
                    self.pkg_dir/"SConstruct",
                    self.pkg_dir/"src"/"cpp"/"SConscript",
                    self.pkg_dir/"src"/"wrapper"/"SConscript",
                   ]
        else:
            return []

    def setupfiles(self):
        return [
        self.pkg_dir/"setup.py",
        self.pkg_dir/"metainfo.ini",
        ]

    def docfiles(self):
        """setup the filenames for the doc layout"""

        return [
            self.pkg_dir/"doc"/"contents.rst",
            self.pkg_dir/"doc"/"Makefile",
            self.pkg_dir/"doc"/"make.bat",
            self.pkg_dir/"doc"/"conf.py",
            self.pkg_dir/"doc"/"user"/"overview.txt",
            self.pkg_dir/"doc"/"user"/"manual.rst",
            self.pkg_dir/"doc"/"user"/"index.rst",
            self.pkg_dir/"doc"/"user"/"autosum.rst",
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
        wralea_txt = wralea_txt.substitute(self.metainfo)

        print "Creating a template version for %s ..." % ( wralea_py, )
        f = open(wralea_py, "w")
        f.write(wralea_txt)
        f.close()

    def template_doc(self):
        files = self.docfiles()
        tpl_files = []
        for f in files:
            if not f.exists() or f.size == 0:
                tpl_file = path(__file__).dirname()/'template_'+f.namebase+'.txt'
                tpl_files.append((f, tpl_file))

        for f, tpl in tpl_files:
            txt = Template(open(tpl).read())
            txt = txt.substitute(self.metainfo)
            print "Creating a template version for %s ..." % ( f, )
            py_file = open(f, "w")
            py_file.write(txt)
            py_file.close()



    def template_legal(self):
        ''' Build new files from a default one.

        If the template file exist and the current file is empty, create a new one.
        '''
        files = self.legalfiles()
        tpl_files = []
        for f in files:
            if not f.exists() or f.size == 0:
                tpl_file = path(__file__).dirname()/'template_'+f.namebase+'.txt'
                tpl_files.append((f, tpl_file))

        for f, tpl in tpl_files:
            txt = Template(open(tpl).read())
            txt = txt.substitute(self.metainfo)

            print "Creating a template version for %s ..." % ( f, )
            py_file = open(f, "w")
            py_file.write(txt)
            py_file.close()


    def template_setup(self):
        ''' Build a setup.py and an associated metainfo.ini '''
        files = self.setupfiles()

        tpl_files = []
        for f in files:
            if not f.exists() or f.size == 0:
                tpl_file = path(__file__).dirname()/'template_'+f.namebase+'.txt'
                tpl_files.append((f, tpl_file))

        for f, tpl in tpl_files:
            txt = Template(open(tpl).read())
            txt = txt.substitute(HAS_SCONS='cpp' in self.languages, **self.metainfo)

            print "Creating a template version for %s ..." % ( f, )
            py_file = open(f, "w")
            py_file.write(txt)
            py_file.close()


    def template_scons(self):
        ''' Build default SConstruct and SConscript files. '''
        files = self.sconsfiles()
        tpl_files = []
        for f in files:
            if not f.exists() or f.size == 0:
                if 'wrapper' in f:
                    tpl_file = path(__file__).dirname()/'template_SConscript_wrapper.txt'
                else:
                    tpl_file = path(__file__).dirname()/'template_'+f.namebase+'.txt'
                tpl_files.append((f, tpl_file))
            
        for f, tpl in tpl_files:
            txt = Template(open(tpl).read())
            txt = txt.substitute(**self.metainfo)

            print "Creating a template version for %s ..." % ( f, )
            py_file = open(f, "w")
            py_file.write(txt)
            py_file.close()


def main():
    """This function is called by alea_create_package script that is installed 
    on your system when installing OpenAlea.PkgBuilder package.

    To obtain specific help, type::

        alea_create_package --help


    """

    usage = """
    %prog create a package layout automatically

    :Examples:

        python %prog --name MyPackage --languages cpp
        %prog --name MyPackage [--languages cpp fortran] [--project openalea]

    """

    parser = OptionParser(usage=usage)

    parser.add_option("--project", dest='project', default='',  
        help="project name in [openalea, vplants, alinea]")
    parser.add_option("--languages", dest='languages', default=None,  
        help="languages separated by a space [cpp, c, fortran]")
    parser.add_option("--release", dest='release', default='1.0', help="the package release")
    parser.add_option("--name", dest='name', default=None, 
                      help="The name of the package as it appear in the eggname: e.g., VisuAlea in OpenAlea.VisuAlea")

    (opts, args)= parser.parse_args()

    print "Running create_layout version %s" % __revision__.split()[2]

    if opts.name==None:
        raise ValueError("""--name must be provided. See help (--help)""")
    pkg = PackageBuilder(name=opts.name, release=opts.release, project=opts.project)

    if opts.languages is not None:
        languages = opts.languages.split(" ")
        for language in languages:
            pkg.set_languages({language:True})

    if not pkg.check_name():
        print "Error, package name %s is invalid" % ( opts.name, )
        return 1

    pkg.mkdirs()
    pkg.mkfiles()

    pkg.template_legal()
    pkg.template_setup()
    pkg.template_scons()
    pkg.template_wralea()
    pkg.template_doc()


if __name__ == "__main__":
    main()
