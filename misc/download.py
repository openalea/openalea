"""script to download projects from the SVN and compile them"""

__Id__ = "$Id$"
__author__ = "Thomas Cokelaer, Thomas.Cokelaer@inria.fr "
__license__ = "Cecill-C"

import getopt
import sys
import os
from optparse import *

# you should not change this dictionary that must reflect the SVN structure
packages = {'openalea': ['trunk', 'tags', 'branches'],
            'vplants': ['vplants/trunk', 'vplants/tags', 'vplants/devel', \
                'vplants/branches'],
            'openaleapkg': ['']}


def ParseParameters():
    """This is the main parsing function to get user arguments"""

    usage = """Usage: %prog [options]

    This script allows to download openalea SVN packages from the GFORGE and
    to compile them on a local directory (no root permission needed).

    Example:
      >>> python download.py --login <your gforge login> --skip openaleapkg
    """
    parser = OptionParser(usage=usage, \
        version="%prog CVS $Id$ \n" \
      + "$Name:  $\n")
    parser.add_option("-l", "--login-name", action="store", \
        default='anonymous', \
        help="the gforge login to access SVN repository. If no login is \
        provided anonymous method will be used.", dest="login")
    parser.add_option("-v", "--verbose", action="store_true", \
        default=False, help="print information")
    parser.add_option("-f", "--force", action="store_true", \
        default=False, help="print information", dest="force")
    parser.add_option("-s", "--skip-svn", action="store_true",\
        default=False, help="skip svn download", dest="skip_svn")
    parser.add_option("-c", "--skip-compilation", action="store_true",\
        default=False, help="skip compilation of the packages", \
        dest="skip_compilation")
    parser.add_option("-o", "--skip-openaleapkg", action="store_true",\
        default=False, \
        help="skip download and compilation of openaleapkg package")
    parser.add_option("-p", "--skip-vplants", action="store_true",\
        default=False, help="skip download and compilation of vplants package")

    (opts, args) = parser.parse_args()
    return opts, args


def question(question, action=None, force=False):
    """
    :param question: a string containing the question
    """
    question += '(yes/no?)'
    _answer = ''
    while (_answer!='yes') and (_answer!='no'):
        if force:
            _answer = 'yes'
        else:
            _answer = raw_input(question)
        if _answer == 'yes':
            try:
                if action is not None:
                    status = os.system(action)
                else:
                    status = 0
            except:
                print 'Error. check the error and try again.'
            finally:
                if status != 0:
                    print 'Error status' + str(status)
                    sys.exit(0)
        elif _answer=='no':
            print 'skipped'
            return False
        else:
            print 'answer by yes or no please!'

    # if here, then everything went well and the return value is True
    # (meaning the answer was yes)
    return True


def start_cmd(cmd, force=False):
    """launch a command with a optional prompt
    :param cmd: a string containing the command to launch
    :param force: a boolean to force the answer to be yes (no interaction)
    """
    str = 'shall we start the following command:\n' + '--->"'+ cmd
    question(question=str, action=cmd, force=force)


def create_svn_command(package, login='anonymous', \
        branch='trunk', target=None):
    """
    :param package: the name of the SVN archive to download
    :param login: the SVN login namename
    :param branch: the main directory to download (trunk, branch, devel)
    :param target: the directory name where to copy the data
     """
    # First, we use either an anonymous access or a login.
    # todo: check that the login is correct, otherwise quit
    if login == 'anonymous':
        cmd = 'svn checkout svn://' + login + '@scm.gforge.inria.fr/svn/'
    else:
        cmd = 'svn checkout svn+ssh://' + login + '@scm.gforge.inria.fr/svn/'
    cmd += package

    # add the package name to download
    cmd += '/' + branch + ' ' # keep the extra space

    # where to place the SVN archive
    if target == None or target == 'Default':
        cmd += os.environ['OPENALEA_HOME'] + '/'+package
    else:
        cmd += os.environ['OPENALEA_HOME'] + '/' + target

    return cmd


def compile_all():
    """todo"""
    for package in packages:
        if package == 'openaleapkg':
            pkgname = 'alinea'
            cmd = 'python ' + os.environ['OPENALEA_HOME'] + \
                '/openalea/misc/make_develop.py develop' +\
                ' --install-dir ' + os.environ['OPENALEA_HOME'] + ' -p ' \
                + pkgname +' -d ' + \
                os.environ['OPENALEA_HOME'] + '/' + package
        else:
            pkgname = package
            cmd = 'python ' + os.environ['OPENALEA_HOME'] + \
                '/openalea/misc/make_develop.py develop' +\
                ' --install-dir ' + os.environ['OPENALEA_HOME'] + ' -p ' \
                + pkgname +' -d ' + \
                os.environ['OPENALEA_HOME'] + '/' + pkgname

        start_cmd(cmd, opts.force)


if __name__ == '__main__':

    command_line = sys.argv[1:]
    (opts, args) = ParseParameters()

    if opts.skip_vplants:
        del packages['vplants']
    if opts.skip_openaleapkg:
        del packages['openaleapkg']


#export PATH="$PATH:$VIRTUALPLANTS_HOME"
#export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:/usr/lib/pkgconfig/"

    # ste the environmental variables
    if 'HOME' in os.environ:
        print 'Your home directory is ' + os.environ['HOME']
    else:
        print 'No home directory was found in your environment. '
        print 'Please add HOME in your bashrc'
        sys.exit()

    if 'OPENALEA_HOME' in os.environ:
        dir = os.environ['OPENALEA_HOME']
        print 'Your OPENALEA_HOME directory is ' + dir
        print '!!! All data with be installed in  '.upper() +dir.upper()
        if os.path.isdir(dir) is False:
            print dir +' does not exists. Create it.'
            question('Shall we create it now ? (yes/no)', \
                action='mkdir'+dir, force=opts.force)
    else:
        print 'No OPENALEA_HOME variable found in your environment. '
        dir = os.getcwd()
        str = 'Create temporary environmental variable : OPENALEA_HOME=' + \
            os.getcwd()
        cmd = 'export OPENALEA_HOME=' + os.getcwd()
        question(str, cmd)

        # update the env for this session only
        # (user will need to update their bashrc)
        os.environ['OPENALEA_HOME'] = os.getcwd()

        str = 'do you want to proceed with the installation in  ' + dir + '?'
        # if the answer is no (False), we quit
        if question(question=str, action=None, force=opts.force) is False:
            sys.exit(0)

    #upload svn archives
    if opts.skip_svn is False:
        for package in packages:
            #todo : could be a user option
            # trunk by default or nothing for openaleapkg
            branch = packages[package][0]

            # create the command
            cmd = create_svn_command(package, opts.login, \
                branch=branch, target='Default')
            # launch it if requested
            try:
                start_cmd(cmd, opts.force)
            except:
                print 'Problem while trying to SVN update this package '\
                    + package
                if opts.login == 'anonymous':
                    print """
Since your login is anonymous, you can only obtain openalea package and not
vplants or openaleapkg. Consider adding the options --skip-vplants and
--skip-openaleapkg OR obtain a user login on the gforge at URL =
https://gforge.inria.fr/ and try again this script with the --login
<gforge_username> option."""
                else:
                    print 'could not connect to the SVN repositories'
                sys.exit(0)

    #export python path
    cmd = 'export PYTHONPATH="$PYTHONPATH:$OPENALEA_HOME" '
    start_cmd(cmd, opts.force)

    # compile all
    if opts.skip_compilation is False:
        compile_all()

    # move the executable to a bin directory
    start_cmd('mkdir $OPENALEA_HOME/bin', opts.force)
    start_cmd('mv $OPENALEA_HOME/visualea $OPENALEA_HOME/bin/', opts.force)

    # finally source the bashrc
    status = os.system('source $HOME/.openalea.sh')

    # ending
    # export PATH="$PATH:$VIRTUALPLANTS_HOME"
    print '-----------------------------------------------'
    for package in packages:
        print 'Installation of '+ package +'done'
    print 'Add the following commands at the end of your .bashrc:'
    print 'export OPENALEA_HOME='+ os.environ['OPENALEA_HOME']
    print 'export PATH="$PATH:' + os.environ['OPENALEA_HOME'] + '/bin"'
    print 'export PYTHONPATH="$PYTHONPATH:$OPENALEA_HOME"'
    print 'source ~/.openalea.sh'
