#!/usr/python
"""A script to call setup.py recursively in a set of packages.

The commands are similar to those expected by setup.py. In addition,
there are a few commands dedicated to multisetup (see --help).

:Example:

>>> python multisetup install
>>> python multisetup install sdist --dist-dir ../dist
>>> python multisetup --quiet --keep-going install sdist --dist-dir ../dist
"""

__license__ = "Cecill-C"
__revision__ = " $Id$"

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

try:
    from openalea.deploy.console import bold, red, green, \
        color_terminal, nocolor, underline, purple
except:
    pj = os.path.join
    sys.path.insert(0, pj('deploy', 'src', 'openalea', 'deploy'))
    from console import bold, red, green, \
        color_terminal, nocolor, underline, purple

""" some remaining examples of setuptools commands:
            'clean': '-a',
            'distribution': '' ,
            'release':  'install bdist_egg -d ../../dist ',
            'html': "--builder html -E",
            'latex': "--builder latex -E",
            'sphinx_upload': "",
            'pdf': "",
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




class Multisetup(object):

    def __init__(self, commands, packages=None, curdir='.', verbose=True):
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
        print "  --quiet                        do not show setup outputs [default=False]"
        print "  -k, --keep-going               force the commands running[default=False]"
        print "  -h, --help                     show detailed help message"
        print "  --packages                     list of packages to run"
        print "                                 [default: deploy / deploygui / core / scheduler / visualea / stdlib / sconsx / misc]"
        print "  --exclude-packages              list of packages to not run"
        print "usage: multisetup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]\n"

    def parse_packages(self):
        """Search and remove package from multisetup command(e.g., --package)

        .. todo:: known issue: python multisetup.py --packages with two 
            packages will be confuse by following commands. Must be put 
            at the end of the command
        """
        if '--packages' in self.commands:
            index = self.commands.index('--packages')
            self.commands.remove('--packages')
            self.packages = set()
            found = True
            while found is True:
                try: #test is no more argument
                    self.commands[index]
                except: # then breaks
                    break
                # otherwise if next argument starts with -, break
                if self.commands[index].startswith('-'):
                    break
                # or carry on to gather package names
                else:
                    self.packages.add(self.commands[index])
                    self.commands.remove(self.commands[index])
                    continue
            #self.commands.pop(index)

        if '--exclude-packages' in self.commands:
            # keep track of --exclude-package index
            index = self.commands.index('--exclude-packages')
            # remove it from the commands
            self.commands.remove('--exclude-packages')
            # remove all packages provided afterwards until next arguments is found
            found = True
            while found is True:
                # look for next argument/package that may be the end of the command
                try:
                    package_to_remove = self.commands[index]
                except:
                    break
                # if this is a valid package name
                if package_to_remove in self.packages:
                    # remove it from the package list
                    self.packages.remove(package_to_remove)
                    # and from the command line
                    self.commands.remove(package_to_remove)
                    # until we found another package
                    continue
                # otherwise, it is an argument that 
                else:
                    #starts with a - sign
                    if package_to_remove.startswith('-'):
                        break
                    # or is invalid
                    raise ValueError('--exclude-packages error: package %s not found in package list' \
                        % self.commands[index])

            #self.commands.pop(index)


    def parse_commands(self):
        """Search and remove multisetup options

        Get the user command line arguments (self.commands) that are dedicated
        to multisetup such as --help, --quiet, --keep-going so that the
        remaining commands are fully comptatible with setuptools.
        """

        if '--quiet' in self.commands:
            self.verbose = False
            self.commands.remove('--quiet')

        if '-k' in self.commands:
            self.force = True
            self.commands.remove('-k')
        if '--keep-going' in self.commands:
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

        """
        import sys
        import os		
        if color:
            try:
                from openalea.deploy.console import bold, red, green, \
                    color_terminal, nocolor, underline, purple
            except:
                try:
                    sys.path.insert(0, os.path.join('deploy', 'src', 'openalea', 'deploy'))
                    from console import bold, red, green, \
                        color_terminal, nocolor, underline, purple
                except:
                    pass
            if not color_terminal():
                # Windows' poor cmd box doesn't understand ANSI sequences
                nocolor()
        else:
            bold = purple = red = green = underline = str

        print bold("Running multisetup version %s" % __revision__.split()[2])

        project_dir = self.curdir.basename()
        directories = [self.curdir.joinpath(package) for package in self.packages]


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


                #print underline('Entering %s package' % directory.basename())
                for cmd in self.commands:
                    setup_command = 'python setup.py %s ' % cmd
                    print "\tExecuting " + setup_command + '...processing',


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
                    if process.returncode == 0:
                        print green('done')
                    else:
                        if not self.verbose:
                            print red('\tFailed. ( error code %s) ' %
                                  (process.returncode))
                            os.chdir(self.curdir)

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


