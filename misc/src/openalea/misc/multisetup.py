#!/usr/python
"""A script to call setup.py recursively in a set of packages.

The commands are similar to those expected by setup.py. In addition,
there are a few commands dedicated to multisetup (see --help).

:Example:

>>> python multisetup install
>>> python multisetup install sdist --dist-dir ../dist
>>> python multisetup --verbose --keep-going install sdist --dist-dir ../dist
"""

__license__ = "Cecill-C"
__revision__ = " $Id: make_develop.py 1695 2009-03-11 17:54:15Z cokelaer $"

import sys, os
from optparse import OptionParser

from subprocess import call, PIPE, Popen


try:
    from path import path
except:
    pj = os.path.join
    sys.path.insert( 0, pj('..', 'openalea', 'core', 'src', 'core'))
    try:
        from path import path
    except:
        from openalea.core.path import path



""" some remaining examples of setuptools commands:
            'clean': '-a',
            'undevelop': '-u',
            'distribution': '' ,
            'release':  'install bdist_egg -d ../../dist ',
            'html': "--builder html -E",
            'latex': "--builder latex -E",
            'sphinx_upload': "",
            'pdf': "",
            'upload_dist':'--verbose',
"""


oa_dirs = """deploy
        deploygui
        core
        visualea
        sconsx
        stdlib
        scheduler
        misc
        openalea_meta
        """

vp_dirs = """
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

alinea_dirs = """
    caribu
    graphtal
    adel
    topvine"""

"""
        self.openalea_sphinx_dirs=deploy deploygui core visualea sconsx
         stdlib misc openalea_meta scheduler
        self.vplants_sphinx_dirs=PlantGL stat_tool tool vplants_meta sequence_analysis lpy container newmtg
        self.alinea_sphinx_dirs=caribu
"""

"""
        #
        if self.command == 'sphinx_upload':
            if self.options.username:
                cmd += ' -u %s' % self.options.username
            if self.options.password:
                cmd += ' -p %s' % 'XXX'
            if self.options.project:
                cmd += ' --project %s' % self.project
"""


"""        # setup for the undevelop command
        if self.command == 'undevelop':
            # if undevelop, we uninstall in the reversed order
            # of the installation. For instance, in OpenAlea case, we want
            # deploy package to be installed first be removed last. This
            # prevents warnings and potential errors due to original
            # distutils being used.
            dirs.reverse()
"""



class Multisetup(object):

    def __init__(self, commands, packages=None, curdir='.', verbose=False):
        """

        :param commands: list of user commands or command
        :param packages: list of packages to process
        :param curdir: current directory default is .
        :param verbose: verbose option
        :param force:  no-run-errors carry on if errors are encountered

        :type commands: a string or list of strings

        The argument `commands` must be a list of strings combining arguments
        from multisetup and setup.

        **Examples** are ['install'], ['--keep-going','install', 'sdist', '-d',
         '../dist'] or ['install','','']

        >>> Multisetup("install --keep-going", ['deploy', 'visualea'], '.', verbose=True)
        >>> Multisetup(["install","--keep-going"], ['deploy', 'visualea'], '.', verbose=True)
        """
        #default
        self.curdir = path(curdir).abspath()
        if isinstance(commands, list):
            self.commands = list(commands)
        elif isinstance(commands, str):
            self.commands = list(commands.split(" "))
        else:
            raise TypeError("commands argument must be a list of arguments or a string")
        self.packages = list(packages)
        self.verbose = verbose
        self.force = False

        #parsing user arguments
        self.parse_packages()
        #self.parse_intern_commands()
        self.parse_commands()


    @classmethod
    def help(cls):
        """help: to get more help and usage
        """
        print "Multi Setup allows to build and install all the packages of OpenAlea found in this directory\n"
        print "Examples:\n"
        print "# Developer mode : Installation of the pks from svn"
        print ">>> python multisetup.py develop\n"
        print "# User mode: Installation of the packages on the system as root"
        print ">>> python multisetup.py install\n"
        print "# Administrator mode: Create distribution of the packages"
        print ">>> python multisetup.py nosetests -w test install bdist_egg -d ../dist sdist -d ../dist\n"
        print "Common commands:\n"
        print "  mulisetup.py sdist -d ./dist   will create a source distribution underneath 'dist/'"
        print "  multisetup.py install          will install the package\n"
        print "Global options:"
        print "  --verbose                      run verbosely [default=False]"
        print "  --keep-going                   force the commands running[default=False]"
        print "  --help                         show detailed help message"
        print "  --package                      list of packages to run"
        print "                                 [default: deploy / deploygui / core / scheduler / visualea / stdlib / sconsx / misc]"
        print "  --exclude-package              list of packages to not run"
        print "usage: multisetup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]\n"


    def parse_packages(self):
        """Search and remove package from multisetup command(e.g., --package)
        """
        if '--package' in self.commands:
            self.packages = set()
            while '--package' in self.commands:
                index = self.commands.index('--package')
                self.commands.remove('--package')
                # check that commands[p] is in dirs
                self.packages.add(self.commands[index])
                self.commands.pop(index)

        if '--exclude-package' in self.commands:
            while '--exclude-package' in self.commands:
                index = self.commands.index('--exclude-package')
                self.commands.remove('--exclude-package')
                # check that commands[index] is in dirs
                if self.commands[index] in self.packages:
                    self.packages.remove(self.commands[index])
                else:
                    print 'Warnings %s not found in package list' \
                        % self.commands[index]
                self.commands.pop(index)

    """def parse_intern_commands(self):
        ""Search and replace user command from multisetup command (e.g., release, html...)
        ""
        for cmd in self.commands:
            if cmd in commands_keys:
                r = self.commands.index(cmd)
                self.commands.remove(cmd)
                self.commands.insert(r, commands_keys[cmd] )
    """

    def parse_commands(self):
        """Search and remove multisetup options

        Get the user command line arguments (self.commands) that are dedicated
        to multisetup such as --help, --verbose, --keep-going so that the
        remaining commands are fully comptatible with setuptools.
        """

        if ('--verbose') in self.commands:
            self.verbose = True
            self.commands.remove('--verbose')

        if ('--keep-going') in self.commands:
            self.force = True
            self.commands.remove('--keep-going')

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
                i += 1
            L = len(self.commands)


    def run(self, color=True):
        """Enter in all package defined and Executing 'python setup.py' with
           user command.

           Create stdout and stderr files (default)

            .. todo:: Need to clean/refactor this code with respect to
                the log files (stdout/stderr). One solution would be to use the module logger.
        """
        if color:
            try:
                from sphinx.util.console import bold, red, green, \
                    color_terminal, nocolor, underline, purple

                if not color_terminal():
                    # Windows' poor cmd box doesn't understand ANSI sequences
                    nocolor()
            except:
                bold = str
                purple = str
                red = str
                green = str
                underline= str

        else:
            purple = str
            bold = str
            red = str
            green = str
            underline= str

        print bold("Running multisetup version %s" % __revision__.split()[2])

        project_dir = self.curdir.basename()
        directories = [self.curdir.joinpath(package) for package in self.packages]
        if not self.verbose:
            stdout = open('stdout', 'w')
            stderr = open('stderr', 'w')
            stdout.close()
            stderr.close()


        print 'Will process the following directories: ',
        for directory in directories:
            print bold(directory.basename()),
        print ''


        try:
            for directory in directories:
                try:
                    os.chdir(directory)
                    print underline('Entering %s package'
                                    % directory.basename())
                except OSError, e:
                    print underline('Entering %s package'
                                    % directory.basename()),
                    print red("cannot find this directory (%s)"
                              % directory.basename())
                    print e


                if not self.verbose:
                    stdout = open('../stdout', 'a+')
                    stdout.write('#####################################\n')
                    stdout.write('*** running setup.py in: ' + directory + '\n')
                    #stdout.close()

                    stderr = open('../stderr', 'a+')
                    stderr.write('#####################################\n')
                    stderr.write('*** running setup.py in: ' + directory + '\n')
                    #stdout.close()


                #print underline('Entering %s package' % directory.basename())
                for cmd in self.commands:
                    setup_command = 'python setup.py %s ' % cmd
                    print "\tExecuting " + setup_command + '...processing',
                    sys.stdout.flush()


                    #Run setup.py with user commands
                    outputs = None
                    errors = None
                    if self.verbose:
                        process = Popen(setup_command,
                                        shell=True)
                        status = process.wait()
                    else:
                        process = Popen(setup_command, stdout=PIPE, stderr=PIPE,
                                        shell=True)
                        #status = process.wait()
                        outputs, errors = process.communicate()
                        try:
                            stdout.write(outputs)
                            stdout.close()
                        except:
                            pass
                        try:
                            stderr.write(errors)
                            stderr.close()
                        except:
                            pass
                    if process.returncode == 0:
                        print green('done')
                    else:
                        if not self.verbose:
                            print red('\tFailed. (see the file stderr; error code %s) ' %
                                  (process.returncode))
                            os.chdir(self.curdir)
#                            if process.returncode != 0 and not self.verbose:
#                                errorfile = open('stderr', 'r').readlines()
#                                for line in errorfile[-50:]:
#                                    if line.startswith('\n'):
#                                        print line
#                                    else:
#                                        print line.replace('\n', '')


                        if not self.force:
                            raise RuntimeError()

                    if 'pylint' in cmd:
                        if outputs is not None:
                            for x in outputs.split('\n'):
                                if x.startswith('Your code has been'):
                                    print purple('\t%s' % x)
                    if 'nosetests' in cmd:
                        if errors is not None:
                            for x in errors.split('\n'):
                                if x.startswith('TOTAL'):
                                    res = x.replace('TOTAL', 'Total coverage')
                                    res = " ".join (res.split())
                                    print purple('\t%s' % res)
                                if x.startswith('Ran'):
                                    print purple('\t%s' % x)
                                if x.startswith('FAILED'):
                                    print purple('\t%s' % x)




        except RuntimeError:
            sys.exit()

        os.chdir(self.curdir)




#if __name__ == "__main__":
#    mysetup = Multisetup()


