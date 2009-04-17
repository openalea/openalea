#!/usr/python
"""A script to install all modules (listed in this script) within a package.

Should work like setup.py script

:Example:

>>> python make_develop install -p vplants -d ./vplants/trunk  
>>> python make_develop install -p alinea -d ./openaleapkg

type --help to get more help and usage  

"""

__license__ = "Cecill-C"
__revision__ = " $Id: make_develop.py 1695 2009-03-11 17:54:15Z cokelaer $"

import sys, os
from optparse import OptionParser

try:
    from path import path
except:
    pj = os.path.join
    sys.path.insert( 0, pj('..', 'openalea', 'core', 'src', 'core'))
    try:
        from path import path
    except:
        from openalea.core.path import path


class Commands():


    def __init__(self, project, command, directory, options=None):
        self.extra_options = {
            'clean': '-a',
            'undevelop': '',
            'develop':  '',
            'install':  '',
            'release':  'bdist_egg -d ../../dist sdist -d ../../dist',
            'html': "--builder html -E",
            'latex': "--builder latex -E",
            'sphinx_upload': "",
            'pdf': ""
            }
        
        #install_cmd = "python setup.py install bdist_egg -d ../../dist sdist -d ../../dist --format=gztar"
    
        self.oa_dirs = """deploy deploygui core visualea sconsx stdlib openalea_meta misc"""
        self.vp_dirs = """PlantGL tool stat_tool sequence_analysis amlobj mtg tree_matching aml fractalysis newmtg WeberPenn vplants_meta"""
        self.alinea_dirs = """caribu graphtal adel topvine"""
        
        self.openalea_sphinx_dirs="""deploy deploygui core visualea sconsx stdlib misc"""                
        self.vplants_sphinx_dirs="""PlantGL stat_tool"""                
        self.alinea_sphinx_dirs="""PlantGL stat_tool"""                

        self.project = project 
        self.command = command
        self.directory = directory
        self.options = options

    def _setdirs(self, project): 
        """ returns a list of directories

        if the command is pdf, or latex or html or sphinx_upload, then the request
        is about Sphinx documentaion. since the directories that can be processed are
        different from those related to compilation and release, we have a switch to different
        list of packages.
        """
        if self.command in ['latex', 'html', 'pdf', 'sphinx_upload']:
            if project == 'openalea':
                _dirs = self.openalea_sphinx_dirs
            elif project == 'vplants':
                _dirs = self.vplants_sphinx_dirs
            elif project == 'alinea':
                _dirs = self.alinea_sphinx_dirs        
        else:
            if project == 'openalea':
                _dirs = self.oa_dirs
            elif project == 'vplants':
                _dirs = self.vp_dirs
            elif project == 'alinea':
                _dirs = self.alinea_dirs        
            
        return  _dirs.split()

    def recursive_call(self, cmd, dirs, root_dir, cwd,doc=False ):
        """run a command though the different directories """

        print dirs
        for dir in dirs:
            if doc:
                dir = os.path.join(dir, 'doc')
                dir = os.path.join(dir, 'latex')
            print "--------------"
            print "cd %s" % dir
            print "Executing %s" % cmd
            print '\n'

            dir = root_dir/dir
            os.chdir(dir)
    
            status = os.system(cmd)
            if status != 0:
                print "Error during the execution of %s" % cmd
                print "---- EXIT ----"
                return
    
            os.chdir(cwd)

    def run(self):
        """run the setup.py command
        
        TODO: clean part related to html/latex
        """

        dirs = self._setdirs(self.project)

        """
        if project == 'vplants':
            release_cmd += '--package=VPlants'
        elif project == 'alinea':
            release_cmd += '--package=Alinea'
        """

        command = self.command

        if command=='undevelop':
            command = 'develop'
        directory = self.directory
        options = self.options
        # create the actual command to run
        _prefix =  "python setup.py"
        cmd = ' '.join([_prefix, command, self.extra_options[self.command]])

        # for the documentation, we skip some directories
        if self.command == 'html':
            cmd = cmd.replace('html', 'build_sphinx', 1)
        elif self.command == 'latex':
            cmd = cmd.replace('latex', 'build_sphinx' ,1)

        # if the options exists, we complete the command
        if options and options.install_dir: 
            cmd += ' --install-dir ' + options.install_dir

        # setup for the release command
        cwd = path(os.getcwd())
        if self.command == 'release':
            dist = cwd/'..'/'dist'
            try:
                if dist.exists():
                    dist.removedirs()
            except:
                pass
   
        # 
        if self.command == 'sphinx_upload':
            if self.options.username:
                cmd += ' -u %s' % self.options.username
            if self.options.password:
                cmd += ' -p %s' % 'XXX'

        # setup for the undevelop command
        if self.command == 'undevelop':
            # if undevelop, we uninstall in the reversed order
            # of the installation. For instance, in OpenAlea case, we want
            # deploy package to be installed first be removed last. This
            # prevents warnings and potential errors due to original 
            # distutils being used.
            dirs.reverse() 
    
        root_dir = path(directory)
        dirs_under_root = root_dir.dirs()
        
        if self.command == 'pdf':
            cmd = 'make'
            self.recursive_call(cmd, dirs, root_dir, cwd,doc=True)
            return

        # check if the dirs are under the given directory.
        for dir in dirs:
            if root_dir/dir not in dirs_under_root:
                print "%s is not a directory of %s" % \
                    (dir, str(root_dir.realpath()))
                print "---- EXIT ----"
                return

        # finally, call the command in each directory
        self.recursive_call(cmd, dirs, root_dir,cwd)

def main():
    """ Define command line and parse options. """

    usage = """
    %prog [options] develop
    or %prog [options] install
    or %prog [options] release
    or %prog [options] undevelop
    or %prog [options] html
    or %prog [options] latex
    or %prog [options] clean
    or %prog [options] sphinx_upload
    or %prog [options] pdf
"""

    parser = OptionParser(usage=usage)

    parser.add_option( "-p", "--project", dest="project",
                       help="project: openalea, vplants or alinea [default: %default]",
                       default='openalea')
    parser.add_option( "-d", "--dir", dest="directory",
                       help="Directory which contains the various modules [default: %default]",
                       default='.')
    parser.add_option( "-i", "--install-dir", dest="install_dir",
                       help="Directory where to install librairies",
                       default=None)
    parser.add_option( "-u", "--username", help="gforge username",
                       default=None)
    parser.add_option( "-w", "--password", help="gforge password",
                       default=None)


    

    available_mode = ['develop', 'undevelop', 'install', 'release', 'clean', 'html', 'latex', 'sphinx_upload', 'pdf']
    available_project = ['openalea', 'vplants', 'alinea']

    
    try:
        (options, args)= parser.parse_args()
    except Exception,e:
        parser.print_usage()
        print "Error while parsing args:", e
        return

    if (len(args) < 1 or args[0] not in available_mode):
        parser.error("Incomplete command : specify develop, undevelop, install release, clean, html, latex or sphinx_upload", "pdf")
    if (options.project not in available_project):
        parser.error("Incomplete command : project must be either alinea, openalea or vplants")

    mode = args[0]

    if mode=='sphinx_upload':
        print 'Uploading sphinx documentation on the gforge'
        print 'Requires username and password'
        if not options.username:
            options.username = raw_input('login:')
        if not options.password:
            options.password = raw_input('password:')
    
    
    commands = Commands(options.project, mode, options.directory, options)
    commands.run() 

if(__name__ == "__main__"):
    main()


