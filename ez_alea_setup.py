#!python
"""Bootstrap setuptools installation

If you want to use setuptools in your package's setup.py, just include this
file in the same directory with it, and add this to the top of your setup.py::

    from ez_setup import use_setuptools
    use_setuptools()

If you want to require a specific version of setuptools, set a download
mirror, or use an alternate download directory, you can do so by supplying
the appropriate options to ``use_setuptools()``.

This file can also be run as a script to install or upgrade setuptools.
"""
__revision__ = " $Id$ "

import sys
import os
from optparse import *

DEFAULT_VERSION = "0.6c11"
DEFAULT_URL     = "http://pypi.python.org/packages/%s/s/setuptools/" % sys.version[:3]
ALEA_PI_URL = "http://openalea.gforge.inria.fr/pi"
NO_ENTER = False #If True, no request to press RETURN will be done.

md5_data = {
    'setuptools-0.6b1-py2.3.egg': '8822caf901250d848b996b7f25c6e6ca',
    'setuptools-0.6b1-py2.4.egg': 'b79a8a403e4502fbb85ee3f1941735cb',
    'setuptools-0.6b2-py2.3.egg': '5657759d8a6d8fc44070a9d07272d99b',
    'setuptools-0.6b2-py2.4.egg': '4996a8d169d2be661fa32a6e52e4f82a',
    'setuptools-0.6b3-py2.3.egg': 'bb31c0fc7399a63579975cad9f5a0618',
    'setuptools-0.6b3-py2.4.egg': '38a8c6b3d6ecd22247f179f7da669fac',
    'setuptools-0.6b4-py2.3.egg': '62045a24ed4e1ebc77fe039aa4e6f7e5',
    'setuptools-0.6b4-py2.4.egg': '4cb2a185d228dacffb2d17f103b3b1c4',
    'setuptools-0.6c1-py2.3.egg': 'b3f2b5539d65cb7f74ad79127f1a908c',
    'setuptools-0.6c1-py2.4.egg': 'b45adeda0667d2d2ffe14009364f2a4b',
    'setuptools-0.6c10-py2.3.egg': 'ce1e2ab5d3a0256456d9fc13800a7090',
    'setuptools-0.6c10-py2.4.egg': '57d6d9d6e9b80772c59a53a8433a5dd4',
    'setuptools-0.6c10-py2.5.egg': 'de46ac8b1c97c895572e5e8596aeb8c7',
    'setuptools-0.6c10-py2.6.egg': '58ea40aef06da02ce641495523a0b7f5',
    'setuptools-0.6c11-py2.3.egg': '2baeac6e13d414a9d28e7ba5b5a596de',
    'setuptools-0.6c11-py2.4.egg': 'bd639f9b0eac4c42497034dec2ec0c2b',
    'setuptools-0.6c11-py2.5.egg': '64c94f3bf7a72a13ec83e0b24f2749b2',
    'setuptools-0.6c11-py2.6.egg': 'bfa92100bd772d5a213eedd356d64086',
    'setuptools-0.6c2-py2.3.egg': 'f0064bf6aa2b7d0f3ba0b43f20817c27',
    'setuptools-0.6c2-py2.4.egg': '616192eec35f47e8ea16cd6a122b7277',
    'setuptools-0.6c3-py2.3.egg': 'f181fa125dfe85a259c9cd6f1d7b78fa',
    'setuptools-0.6c3-py2.4.egg': 'e0ed74682c998bfb73bf803a50e7b71e',
    'setuptools-0.6c3-py2.5.egg': 'abef16fdd61955514841c7c6bd98965e',
    'setuptools-0.6c4-py2.3.egg': 'b0b9131acab32022bfac7f44c5d7971f',
    'setuptools-0.6c4-py2.4.egg': '2a1f9656d4fbf3c97bf946c0a124e6e2',
    'setuptools-0.6c4-py2.5.egg': '8f5a052e32cdb9c72bcf4b5526f28afc',
    'setuptools-0.6c5-py2.3.egg': 'ee9fd80965da04f2f3e6b3576e9d8167',
    'setuptools-0.6c5-py2.4.egg': 'afe2adf1c01701ee841761f5bcd8aa64',
    'setuptools-0.6c5-py2.5.egg': 'a8d3f61494ccaa8714dfed37bccd3d5d',
    'setuptools-0.6c6-py2.3.egg': '35686b78116a668847237b69d549ec20',
    'setuptools-0.6c6-py2.4.egg': '3c56af57be3225019260a644430065ab',
    'setuptools-0.6c6-py2.5.egg': 'b2f8a7520709a5b34f80946de5f02f53',
    'setuptools-0.6c7-py2.3.egg': '209fdf9adc3a615e5115b725658e13e2',
    'setuptools-0.6c7-py2.4.egg': '5a8f954807d46a0fb67cf1f26c55a82e',
    'setuptools-0.6c7-py2.5.egg': '45d2ad28f9750e7434111fde831e8372',
    'setuptools-0.6c8-py2.3.egg': '50759d29b349db8cfd807ba8303f1902',
    'setuptools-0.6c8-py2.4.egg': 'cba38d74f7d483c06e9daa6070cce6de',
    'setuptools-0.6c8-py2.5.egg': '1721747ee329dc150590a58b3e1ac95b',
    'setuptools-0.6c9-py2.3.egg': 'a83c4020414807b496e4cfbe08507c03',
    'setuptools-0.6c9-py2.4.egg': '260a2be2e5388d66bdaee06abec6342a',
    'setuptools-0.6c9-py2.5.egg': 'fe67c3e5a17b12c0e7c541b7ea43a8e6',
    'setuptools-0.6c9-py2.6.egg': 'ca37b1ff16fa2ede6e19383e7b59245a',
}



PYDISTUTILS_NOTE = """
Note that the file ~/.pydistutils will be used for any future use of
distutils (setup.py). You can delete this file to get back to normal
usage. However, this file will be automatically created again if you
use ez_alea_setup with --install-dir argument.
"""


try: from hashlib import md5
except ImportError: from md5 import md5

def _validate_md5(egg_name, data):
    if egg_name in md5_data:
        digest = md5(data).hexdigest()
        if digest != md5_data[egg_name]:
            print >>sys.stderr, (
                "md5 validation of %s failed!  (Possible download problem?)"
                % egg_name
            )
            sys.exit(2)
    return data

#Allow us to log in from deploy.
#get the auth file that we need:
try:
    import os.path
    import urllib, getpass, urllib2
    urllib2.urlopen("http://gforge.inria.fr/", timeout=4) #raises an error if timeouts.
    filename = os.path.join(os.getcwd(), "auth.py")
    urllib.urlretrieve( "http://gforge.inria.fr/scm/viewvc.php/*checkout*/trunk/deploygui/src/openalea/deploygui/auth.py?root=openalea",
                        filename )

    import auth
    #now that it is imported (in memory), we don't need it anymore:
    os.remove(filename)
    os.remove(filename+"c")
    GFORGE_LOGIN_AVAILABLE = True
except Exception, e:
    print e
    print >> sys.stderr, ("GForge authentification disabled")
    GFORGE_LOGIN_AVAILABLE = False
    
def cli_login():
    if not GFORGE_LOGIN_AVAILABLE : print "GForge not available, auth module cannot be loaded."
    print 'GFORGE login\n'
    print "gforge username: ",
    login = raw_input()
    password = getpass.getpass("gforge password: ")

    values = {'form_loginname':login,
              'form_pw':password,
              'return_to' : '',
              'login' : "Connexion avec SSL" }

    login_url = "https://gforge.inria.fr/account/login.php"

    auth.cookie_login(login_url, values)


def use_setuptools(
    version=DEFAULT_VERSION, download_base=DEFAULT_URL, to_dir=os.curdir,
    download_delay=15
):
    """Automatically find/download setuptools and make it available on sys.path

    `version` should be a valid setuptools version number that is available
    as an egg for download under the `download_base` URL (which should end with
    a '/').  `to_dir` is the directory where setuptools will be downloaded, if
    it is not already available.  If `download_delay` is specified, it should
    be the number of seconds that will be paused before initiating a download,
    should one be required.  If an older version of setuptools is installed,
    this routine will print a message to ``sys.stderr`` and raise SystemExit in
    an attempt to abort the calling script.
    """
    was_imported = 'pkg_resources' in sys.modules or 'setuptools' in sys.modules
    def do_download():
        egg = download_setuptools(version, download_base, to_dir, download_delay)
        sys.path.insert(0, egg)
        import setuptools; setuptools.bootstrap_install_from = egg
    try:
        import pkg_resources
    except ImportError:
        return do_download()
    try:
        pkg_resources.require("setuptools>="+version); return
    except pkg_resources.VersionConflict, e:
        if was_imported:
            print >>sys.stderr, (
            "The required version of setuptools (>=%s) is not available, and\n"
            "can't be installed while this script is running. Please install\n"
            " a more recent version first, using 'easy_install -U setuptools'."
            "\n\n(Currently using %r)"
            ) % (version, e.args[0])
            sys.exit(2)
        else:
            del pkg_resources, sys.modules['pkg_resources']    # reload ok
            return do_download()
    except pkg_resources.DistributionNotFound:
        return do_download()

def download_setuptools(
    version=DEFAULT_VERSION, download_base=DEFAULT_URL, to_dir=os.curdir,
    delay = 15
):
    """Download setuptools from a specified location and return its filename

    `version` should be a valid setuptools version number that is available
    as an egg for download under the `download_base` URL (which should end
    with a '/'). `to_dir` is the directory where the egg will be downloaded.
    `delay` is the number of seconds to pause before an actual download attempt.
    """
    import urllib2, shutil
    egg_name = "setuptools-%s-py%s.egg" % (version,sys.version[:3])
    url = download_base + egg_name
    saveto = os.path.join(to_dir, egg_name)
    src = dst = None
    if not os.path.exists(saveto):  # Avoid repeated downloads
        try:
            from distutils import log
            if delay:
                log.warn("""
---------------------------------------------------------------------------
This script requires setuptools version %s to run (even to display
help).  I will attempt to download it for you (from
%s), but
you may need to enable firewall access for this script first.
I will start the download in %d seconds.

(Note: if this machine does not have network access, please obtain the file

   %s

and place it in this directory before rerunning this script.)
---------------------------------------------------------------------------""",
                    version, download_base, delay, url
                ); from time import sleep; sleep(delay)
            log.warn("Downloading %s", url)
            src = urllib2.urlopen(url)
            # Read/write all in one block, so we don't create a corrupt file
            # if the download is interrupted.
            data = _validate_md5(egg_name, src.read())
            dst = open(saveto,"wb"); dst.write(data)
        finally:
            if src: src.close()
            if dst: dst.close()
    return os.path.realpath(saveto)



def main(argv, version=DEFAULT_VERSION):
    """Install or upgrade setuptools and EasyInstall"""

    try:
        import setuptools
    except ImportError:
        egg = None
        try:
            egg = download_setuptools(version, delay=0)
            sys.path.insert(0, egg)
            from setuptools.command.easy_install import main
            return main(list(argv)+[egg])   # we're done here
        finally:
            if egg and os.path.exists(egg):
                os.unlink(egg)
    else:
        if setuptools.__version__ == '0.0.1':
            print >>sys.stderr, (
            "You have an obsolete version of setuptools installed.  Please\n"
            "remove it from your system entirely before rerunning this script.")
            sys.exit(2)
    
    req = "setuptools>="+version
    import pkg_resources
    try:
        pkg_resources.require(req)                
    except pkg_resources.VersionConflict:
        try:
            from setuptools.command.easy_install import main
        except ImportError:
            from easy_install import main
        main(list(argv)+[download_setuptools(delay=0)])
        sys.exit(0) # try to force an exit
    else:
        # hardcoded version of --install-dir        
        if '--install-dir' in argv:
            argv = None

        if argv:
            from setuptools.command.easy_install import main
            main(argv)
        else:            
            print "Setuptools version %s or greater has been installed." % \
                version
            print '(Run "ez_setup.py -U setuptools" to reinstall or upgrade.)'


def update_md5(filenames):
    """Update our built-in md5 registry"""

    import re
    from md5 import md5

    for name in filenames:
        base = os.path.basename(name)
        f = open(name, 'rb')
        md5_data[base] = md5(f.read()).hexdigest()
        f.close()

    data = ["    %r: %r,\n" % it for it in md5_data.items()]
    data.sort()
    repl = "".join(data)

    import inspect
    srcfile = inspect.getsourcefile(sys.modules[__name__])
    f = open(srcfile, 'rb')
    src = f.read()
    f.close()

    match = re.search("\nmd5_data = {\n([^}]+)}", src)
    if not match:
        print >>sys.stderr, "Internal error!"
        sys.exit(2)

    src = src[:match.start(1)] + repl + src[match.end(1):]
    f = open(srcfile, 'w')
    f.write(src)
    f.close()


########################## OpenAlea Installation #############################


def install_deploy(opts=None):
    """ Install OpenAlea.Deploy with setuptools

    :param opts: contain a field install_dir to indicate the
    root directory of the lib and bin directories for a non-root
    installation.
    """

    from pkg_resources import require
    require('setuptools')
    from setuptools.command.easy_install import main

    dependency_links = [ALEA_PI_URL]
    if not opts is None and opts.gforge :
        dependency_links.append("http://gforge.inria.fr/frs/?group_id=43")
    try:
        print 'Installing openalea.Deploy'
        main(['-f', dependency_links, "openalea.deploy"])
        print 'OpenAlea.Deploy installed'
    except Exception, e:
        print e
        print "Cannot install openalea.deploy. Do you have root permission ?"
        print "Add sudo before your python command, or use --install-dir."
        sys.exit(-1)


def install_pkg(name):
    """ Install package with alea_install """

    from pkg_resources import require
    require('openalea.deploy')
    from openalea.deploy.alea_install import main

    try:
        print 'Installing ' + name
        main(['-f', ALEA_PI_URL, name])
        print '%s installed' % name
    except:
        print "Cannot install %s. Do you have root permission ?" % name
        print "Add sudo before your python command, or use --install-dir."

def welcome_setup():
    try:
        revision = __revision__.strip().split()
        if len(revision) > 2:
            revision = revision[2]
        else:
            revision = '0.8'
        print "Running ez_alea_setup version %s" % revision
    except:
        pass
    print  """
    
-----------------------------------------------------------------------------
-                       OPENALEA Installation Initialisation                -
-----------------------------------------------------------------------------
"""



def welcome():
    """ Print welcome message """

    print """
-----------------------------------------------------------------------------
-                       OPENALEA Installation                               -
-----------------------------------------------------------------------------
This script will download and install OpenAlea Installer.
The process can take a long time depending of your network connection.
Please, be patient !"""
    if(not NO_ENTER): raw_input("Press Enter to continue...")
    print "\n"


def install_openalea(opts=None):
    """ Install the base packages """

    welcome()
    install_deploy(opts)
    pkgs = ["openalea.deploygui", ]

    if("win32" in sys.platform or "win64" in sys.platform or "darwin" in sys.platform):
        pkgs = ["qt4 >= 4.5.3", ] + pkgs

    for pkg in pkgs:
        install_pkg(pkg)


def install_setuptools():
    """INSTALL Setup tools"""
    if len(sys.argv)>2 and '--md5update' in sys.argv:
        update_md5(sys.argv[2:])
    else:
        main(sys.argv[1:])


def finalize_installation():
    try:
        from openalea.deploy import check_system
        import os

        print """
\nTo install OpenAlea packages you can start the graphical Installer:
  - On Windows : Start Menu -> OpenAlea -> Installer
  - On Linux/Unix : use the shell command 'alea_install_gui'
  - You can also use the command 'alea_install' in a shell
"""

        env = check_system()
        os.environ.update(env)

        os.system('%s -c "import openalea.deploygui.alea_install_gui as gui; gui.main()"'%(sys.executable))
    except:
        print "OpenAlea is not installed properly."


def finalize_non_root_installation(opts):
    """print information to update environmental variables"""

    if opts.install_dir:
        dirname = os.path.abspath(opts.install_dir)
        print PYDISTUTILS_NOTE
        print """
==============================================================================
As a non root installation, your PYTHON libraries have been installed in:
%(dirname)s/lib
Therefore, you need to update your PYTHONPATH environmental variable by adding
this line in your .bashrc (in bash shell):

export PYTHONPATH=$PYTHONPATH:%(dirname)s/lib
export PYTHONPATH=$PYTHONPATH:%(dirname)s    (if setuptools was installed)

Moreover, the visualea script can be found in:
%(dirname)s/bin.
You can create an alias in your bashrc:

alias visualea='%(dirname)s/bin/visualea'
==============================================================================
""" % {'dirname': dirname}
    else:
        return


def non_root_initialisation():
    """ Creating directories where to install the data (non-root usage)

    If a non-root installation is required, we need to :
        - check the existence of the opts.install_die directory
        - create the lib and bin directories
        - add a shared-lib.pth file with the appropriate path to the libs
        - create and/or check the .pydistutils content
        - update the PYTHONPATH for this session
    """
    print 'non_root_initialisation'
    # check existence of ./lib and ./bin if non-root
    if opts.install_dir:
        print """
-----------------------------------------------------------------------------
-                alea_install_gui NON-ROOT pre-installation                 -
-----------------------------------------------------------------------------
 * Checking existence of the %s directory and its sub-directories""" % opts.install_dir

        # check the presence of the main directory
        if not os.path.isdir(opts.install_dir):
            print 'Creating directory %s and subdirectories (lib and bin) done'\
                % opts.install_dir
            # create the main and sub-directories
            os.mkdir(opts.install_dir)
            os.mkdir(opts.install_dir+'/bin')
            os.mkdir(opts.install_dir+'/lib')

        # the previous command guarantee to enter in this if-block
        if os.path.isdir(opts.install_dir):
            # create the main directory if needed
            try:
                os.mkdir(opts.install_dir+'/bin')
            except:
                print ' -- Using existing directory ' + opts.install_dir + '/bin'
            # create the sub-directories lib if neede
            try:
                os.mkdir(opts.install_dir+'/lib')
            except:
                print ' -- Using existing directory ' + opts.install_dir + '/lib'

            # create the shared-lib.pth that will be read by deploy to add the link
            # to dynamic librairies
            dirname = os.path.abspath(opts.install_dir) + '/lib/'
            filename = dirname + 'shared-lib.pth'
            try:
                # overwrite the shared-lib.pth for non-root installation so that
                # deploy/install_lib.py uses the install-dyn-lib option
                print " * Creating the shared-lib.pth file in %s done " % filename
                f = open(filename, 'w')
                f.write(dirname)
                f.close()
            except:
                print 'Error: could not create the file shared-lib.pth in %s' % (filename)
                sys.exit(0)
        else:
            print 'Creating directory %s and subdirectories (lib and bin)' % opts.install_dir
            # create the main and sub-directories
            os.mkdir(os.path.abspath(opts.install_dir))
            os.mkdir(opts.install_dir+'/bin')
            os.mkdir(opts.install_dir+'/lib')

    if(not NO_ENTER): raw_input("\n== Press Enter to continue. ==\n")

    # check presence of ~/.pydistutils
    if opts.install_dir:
        print " * .pydistutils configuration "
        # this file must be present and valid for non-root installation.
        home = os.environ['HOME']
        file = home + '/.pydistutils.cfg'

        # check the presence of the file and check its content
        print """ -- ~/.pydistutils is required for a non-root installation"""
        if os.path.isfile(file):
            print(" -- File ~/.pydistutils found. Reading its content ([install] section).")
        else:
            # create the pydisutils file
            print " -- File ~/.pydistutils not found. Creating it. Done"
            f = open(home + '/.pydistutils.cfg', 'w')
            f.write("[install]\n")
            f.write("install_lib = %s \n" % (os.path.abspath(opts.install_dir) + '/lib'))
            f.write("install_scripts = %s\n" % (os.path.abspath(opts.install_dir) + '/bin'))
            f.close()

        print PYDISTUTILS_NOTE

        import ConfigParser
        config = ConfigParser.RawConfigParser()
        config.read(file)

        # check the pydistutils config file (lib path)
        try:
            lib = config.get('install', 'install_lib')
            bin = config.get('install', 'install_scripts')
            lib = os.path.expanduser(lib) # append the home
            bin = os.path.expanduser(bin) # append the home
        except:
            print 'Error: install_lib or install_scripts not found in ~/.pydistutils'
            sys.exit(0)

        # print some information
        if os.path.isdir(lib) and os.path.isdir(bin):
            print 'Librairies will be installed in: %s' % lib
            print 'Binaries will be installed in: %s\n' % bin
        else:
            print 'Error: the directory specified in ~.pydistutils %s does not exists. ' % lib
            print 'You provided the directory (--install-dir) %s' % os.path.abspath(opts.install_dir)
            print "Solution: edit the .pydistutils or simply remove it !"
            sys.exit(0)

    # temporary update of the pythonpath to put share-lib.pth in the PYTHONPATH
    if opts.install_dir:
        if 'PYTHONPATH' in os.environ:
            os.environ['PYTHONPATH'] = \
                os.environ['PYTHONPATH'] + ':' + os.path.abspath(opts.install_dir) +'/lib'
        else:
            os.environ['PYTHONPATH'] =  os.path.abspath(opts.install_dir) +'/lib'

        os.environ['PYTHONPATH'] = \
                os.environ['PYTHONPATH'] + ':' + os.path.abspath(opts.install_dir)


    # check that ~/.pydistutils is not present
    if(not 'win32' in sys.platform):
        if not opts.install_dir:
            home = os.environ['HOME']
            file = home + '/.pydistutils.cfg'
            if os.path.isfile(file):
                print """
Remove the ~/.pydistutils.cfg present in your HOME directory if you want a root
installation."""


def ParseParameters():
    """This is the main parsing function to get user arguments"""

    usage = """Usage: %prog [options]

    Example:
      >>> python ez_alea_setup.py --install-dir /home/user/openalea
      >>> python ez_alea_setup.py
    """
    parser = OptionParser(usage=usage, \
        version="%prog CVS $Id$ \n" \
      + "$Name:  $\n")
    parser.add_option("-i", "--install-dir", action="store", \
        help="the path where to install openalea (non-root installation)")
    parser.add_option("-s", "--install-setuptools", action="store_true", default=False, \
        help="install setuptools (root installation)")
    parser.add_option("-g", "--gforge", action="store_true",default=False,
                      help="Authenticate into the gforge server")
    parser.add_option("-n", "--no-enter-request", action="store_true",default=False,
                      help="Skip all requests for Enter pressing.")
    (opts, args) = parser.parse_args()
    return opts, args


# main part

if (__name__ == "__main__"):

    # parse user's parameters
    command_line = sys.argv[1:]
    (opts, args) = ParseParameters()

    #create a new string to pass on to the new instances of
    #this process.
    original_args_string = ""
    for arg in sys.argv: original_args_string += " " + arg

    # to install setuptools only
    #somewhere down the road a new process is spawned with argv.
    #however, it does not appreciate --gforge and -g so we must delete
    #them.
    if opts.gforge :
        try:    sys.argv.remove('--gforge')
        except: pass
        try:    sys.argv.remove('-g')
        except: pass

    if opts.install_setuptools:
        sys.argv.remove('--install-setuptools')
        install_setuptools()
        sys.exit(0)

    if opts.no_enter_request:
        NO_ENTER = True
        try:    sys.argv.remove('--no-enter-request')
        except: pass
        try:    sys.argv.remove('-n')
        except: pass        

    # Execute the script in 2 process
    # This part is called the second time.
    if("openalea" in sys.argv):       
        # Second call: install openalea.
        if opts.gforge :
            cli_login()

        install_openalea(opts)

        finalize_installation()
        if opts.install_dir:
            finalize_non_root_installation(opts)

    else:
        welcome_setup()
        # First call
        # on linux, check that sudo and -non-root option (--install-dir) are not called together
        if(not 'win32' in sys.platform):
            if 'SUDO_COMMAND' in os.environ and '--install-dir' in sys.argv[:]:
                print """root installation (sudo) and non-root installation (--install-dir) forbidden."""
                sys.exit(0)



        # create the directories if needed (non-root installation).
        print 'Checking your configuration'.upper()
        non_root_initialisation()

        # Install setup tools
        print '\nInstalling setuptools if needed\n'.upper()
        install_setuptools()
  
        # Start again in an other process with openalea option
        # to take into account modifications
        if opts.install_dir:
            os.system('%s "%s" openalea %s ' % \
                (sys.executable, __file__, original_args_string))
        else:
            os.system('%s "%s" openalea %s'%(sys.executable, __file__, original_args_string))

        if(not NO_ENTER): raw_input("\n== Press Enter to finish. ==")
