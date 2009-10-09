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

from subprocess import call
from openalea.core.path import path


try:
    from path import path
except:
    pj = os.path.join
    sys.path.insert( 0, pj('..', 'openalea', 'core', 'src', 'core'))
    try:
        from path import path
    except:
        from openalea.core.path import path


#Internal commands for Multisetup object 
commands_keys = {'html': 'build_sphinx --builder html -E',
                 'latex': 'build_sphinx --builder latex -E',
                 'release' : 'bdist_egg -d ../../dist sdist -d ../../dist'
                 #'pdf': 'build_sphinx --builder pdf -E',  #command pdf ???
                 }



class Commands():


    def __init__(self, project, command, directory, options=None):
        self.extra_options = {
            'clean': '-a',
            'undevelop': '-u',
            'develop':  '',
            'install':  '',
            'nosetests': '-w test',
            'distribution': '' ,
            'sdist':'',
            'pylint':'',
            'bdist':'',
            'bdist_egg':'',
            'release':  'install bdist_egg -d ../../dist ',
            'html': "--builder html -E",
            'latex': "--builder latex -E",
            'sphinx_upload': "",
            'pdf': "",
            'upload_dist':'--verbose',
            }
        
        #install_cmd = "python setup.py install bdist_egg -d ../../dist sdist -d ../../dist --format=gztar"
    
        self.oa_dirs = """
        deploy 
        deploygui 
        core 
        visualea 
        sconsx
        stdlib 
        scheduler 
        misc
	openalea_meta 
        """
        
        self.vp_dirs = """
        PlantGL 
        tool 
        stat_tool 
        sequence_analysis 
        amlobj 
        mtg 
        tree_matching 
        aml 
        fractalysis
        tree
        tree_statistic
        container
        newmtg 
        WeberPenn 
        lpy
        """
        #""" vplants_meta"""
        self.alinea_dirs = """caribu graphtal adel topvine"""
        
        self.openalea_sphinx_dirs="""deploy deploygui core visualea sconsx
         stdlib misc openalea_meta scheduler""" 
        self.vplants_sphinx_dirs="""PlantGL stat_tool tool vplants_meta 
        sequence_analysis lpy container newmtg"""
        self.alinea_sphinx_dirs="""caribu"""

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

    def recursive_call(self, cmd, dirs, root_dir, cwd, doc=False):
        """run a command though the different directories """

        print dirs
        for udir in dirs:
            if doc:
                udir = os.path.join(udir, 'doc')
                udir = os.path.join(udir, 'latex')
            print '\n\n'
            print "########## Make develop switches to %s directory ##########"\
                % udir.upper()
            print "= Executing %s =" % cmd

            udir = root_dir/udir
            os.chdir(udir)
    
            import subprocess
            status = subprocess.call(cmd, stdout=None, stderr=None, shell=True)
            
            
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

        if command == 'undevelop':
            command = 'develop -u'
        directory = self.directory
        options = self.options
        # create the actual command to run
        _prefix =  "python setup.py"
        cmd = ' '.join([_prefix, command, self.extra_options[self.command]])

        # for the documentation, we skip some directories
        if self.command == 'html':
            cmd = cmd.replace('html', 'build_sphinx', 1)
        elif self.command == 'latex':
            cmd = cmd.replace('latex', 'build_sphinx', 1)

        # if the options exists, we complete the command
        if options and options.install_dir: 
            cmd += ' --install-dir ' + options.install_dir

        # setup for the release command
        cwd = path(os.getcwd())
        if self.command == 'release':
            cmd = cmd.replace('release ', '', 1)
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
            if self.options.project:
                cmd += ' --project %s' % self.project

        # setup for the undevelop command
        if self.command == 'undevelop':
            # if undevelop, we uninstall in the reversed order
            # of the installation. For instance, in OpenAlea case, we want
            # deploy package to be installed first be removed last. This
            # prevents warnings and potential errors due to original 
            # distutils being used.
            dirs.reverse() 

        if self.command == 'nosetests':
            cmd += ''
    
        root_dir = path(directory)
        dirs_under_root = root_dir.dirs()
        
        if self.command == 'pdf':
            cmd = 'make'
            self.recursive_call(cmd, dirs, root_dir, cwd,doc=True)
            return

        # check if the dirs are under the given directory.
        for udir in dirs:
            if root_dir/udir not in dirs_under_root:
                print "%s is not a directory of %s" % \
                    (udir, str(root_dir.realpath()))
                print "---- EXIT ----"
                return

        # finally, call the command in each directory
        self.recursive_call(cmd, dirs, root_dir,cwd)



class Multisetup(object):

    def __init__(self, curdir=None, commands=None, packages=None, verbose=False, force=False):
        """Initialization of current directory, user commands, running packages, verbose and no-run-errors options
        """
        #default
        self.curdir = curdir
        self.commands = commands
        self.packages = packages
        self.verbose = verbose
        self.force = force   

        #parsing user arguments
        self.parse_packages()
        self.parse_intern_commands()
        self.parse_commands()


    def Help(self):
        """Help: to get more help and usage  
        """    
        print "Common commands:\n"
        print "  mulisetup.py sdist -d ./dist   will create a source distribution underneath 'dist/'"
        print "  multisetup.py install          will install the package\n"
        print "Global options:"
        print "  --verbose                      run verbosely (default=False)"
        print "  --stop-on-errors               force the commands running"
        print "  --help                         show detailed help message"
        print "  --package                      list of packages to run\n"
        print "usage: multisetup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]\n"


    def parse_packages(self):
        """Search and remove package from multisetup command(e.g., --package)
        """
        if '--package' in self.commands:
            self.packages = []
            while '--package' in self.commands:
                p = self.commands.index('--package')
                self.commands.remove('--package')
                # check that commands[p] is in dirs
                self.packages.append(self.commands[p])                
                self.commands.pop(p)

    def parse_intern_commands(self):
        """Search and replace user command from multisetup command (e.g., release, html...)
        """
        for cmd in self.commands:
            if cmd in commands_keys:
                r = self.commands.index(cmd)
                self.commands.remove(cmd)       
                self.commands.insert(r, commands_keys[cmd] )
                
        
    def parse_commands(self):
        """Parse remaining options that will be use by setup.py
           Search and remove multisetup options (e.g., --help, --verbose, --stop-on-errors)
        """
        if '--help' in self.commands or len(self.commands)==0:
            self.Help()
            sys.exit()

        if ('--verbose') in self.commands:
            self.verbose = True
            self.commands.remove('--verbose')

        if ('--stop-on-errors') in self.commands:
            self.force = True
            self.commands.remove('--stop-on-errors')
    
        L = len(self.commands)
        i = 0
        while (i < L):
            if self.commands[i].startswith('-'):
                try:
                    self.commands[i-1] = self.commands[i-1] + ' ' + self.commands[i] + ' ' + self.commands[i+1]
                    self.commands.pop(i)
                    self.commands.pop(i)
                except:
                    self.commands[i-1] = self.commands[i-1] + ' ' + self.commands[i]
                    self.commands.pop(i) 
            else:
                i+=1
            L =len(self.commands)


    def run(self):
        """Enter in all package defined and Executing 'python setup.py' with user command
           Create stdout and stderr files (default)
        """
        project_dir = self.curdir.basename()
        directories = [self.curdir.joinpath(package) for package in self.packages]
        stdout = open('stdout', 'w')
        stderr = open('stderr', 'w')
        stdout.close()
        stderr.close()
        print 'Will process the following directories'
        for directory in directories:
            print project_dir + '/' +directory.basename()
            os.chdir(directory)
            
            stdout = open('../stdout', 'a+')
            stdout.write('#####################################\n')
            stdout.write('*** running setup.py in : ' + directory + '\n')
            stdout.close()

            stderr = open('../stderr', 'a+')
            stderr.write('#####################################\n')
            stderr.write('*** running setup.py in : ' + directory + '\n')
            stderr.close()
        
            print 'Entering %s package' % directory
            for cmd in self.commands:
                print "    Executing  'python setup.py %s'  " % cmd ,
                sys.stdout.flush()


                #Run setup.py with user commands
                if self.verbose:
                    retcode = call('python setup.py %s ' %cmd, shell=True)
                else:
                    retcode = call('python setup.py %s ' %cmd, stdout=open('../stdout', 'a+'), 
                                    stderr=open('../stderr','a+'), shell=True)
                if retcode == 0:
                    print ' done'
                else:
                    print ' !!!!!!!! failed !!!!!!! (see stderr file)'
                    if not self.force:
                        sys.exit()



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


    

    available_mode = ['develop', 'undevelop', 'install', 'release', 
                      'clean', 'html', 'latex', 'sphinx_upload', 'pdf', 
                      'nosetests', 'distribution', 'sdist', "bdist",
                       "bdist_egg", "pylint", "upload_dist"]
    available_project = ['openalea', 'vplants', 'alinea']

    
    try:
        (options, args)= parser.parse_args()
    except Exception,e:
        parser.print_usage()
        print "Error while parsing args:", e
        return

    if (len(args) < 1 or args[0] not in available_mode):
        parser.error("Incomplete command : specify develop, undevelop, install release, clean, html, latex or sphinx_upload pdf")
    if (options.project not in available_project):
        parser.error("Incomplete command : project must be either alinea, openalea or vplants")

    mode = args[0]

    if mode=='sphinx_upload':
        print 'Uploading sphinx documentation on the gforge'
        print 'Requires username and ssh key on the gforge'
        if not options.username:
            options.username = raw_input('login:')
        #if not options.password:
        #    options.password = raw_input('password:')
    
    
    commands = Commands(options.project, mode, options.directory, options)
    commands.run() 


if(__name__ == "__main__"):
    main()


