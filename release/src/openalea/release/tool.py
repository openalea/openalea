from openalea.release.utils import memoize, NullOutput, pj, sh, \
get_python_scripts_dirs, sys, into_subdir, url, unpack, os, glob, path
from openalea.release import Formula
import time
import threading

class MSingleton(type):
    """ Singleton Metaclass."""
    def __init__(cls, name, bases, dic):
        type.__init__(cls, name, bases, dic)
        cls.instance=None
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance=type.__call__(cls, *args, **kw)
        return cls.instance
        
        
class MTool(MSingleton):
    def __init__(cls, name, bases, dic):
        MSingleton.__init__(cls, name, bases, dic)
        if object not in bases:
            cls.cmd_options = cls.cmd_options or []
            cls.cmd_options.insert(0, (name, None, "Path to "+ (cls.exe or name+".exe") ) )
            if cls.installable:
                cls.arch_name   = name+"."+cls.arch_name_ext


class Tool(object):
    __metaclass__ = MTool

    class PyExecPaths(object):
        """Include this symbol in the default_paths
        list to add the python "scripts" folder to
        the search list"""
        pass

    class OriginalSystemPaths(object):
        """Include this symbol in the paths listes in %PATH%
        to the search list"""
        pass

    # If this is not true, there will be no attempt
    # to install the tool if it hasn't been found
    installable = True

    # URL at which we can download
    # a release of the tool.
    url = None

    # extension of the downloaded archive.
    # the extension determines the unpacker to use.
    arch_name_ext = None

    # a glob pattern to move into subdirectories
    archive_subdir = None

    # Executable that can be called to test for availability
    exe = None

    # Places to look for the exe by default.
    default_paths = None

    # if not None, it is then a list of triplets specifying additionnal
    # command line options that are needed for this package.
    # the MTool metaclass will automatically add a self.name+"_path"
    # command line to this list.
    cmd_options = None

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def options(self):
        return Formula().options

    @memoize("path")
    def get_path(self, no_install=False):
        print "Looking for %s path"%self.name
        pth = self._get_path(no_install)
        if pth:
            print "\tGot it:", pth
        return pth

    def _get_path(self, no_install=False):
        #NOTE:
        #The BuildEnvironment class cleans the PATH.
        #no need to look into that variable.

        def pth_test(pth):
            exe_path = pj(pth, self.exe)
            if path(exe_path).exists():
                # see if we can actually call it
                try:
                    sh(exe_path, stdout=NullOutput, stderr=NullOutput)
                except OSError:
                    print "\tCalling", exe_path, "failed: bad path"
                    return False
                else:
                    return True
            return False

        # First look at the user provided command line option.
        pth = self.options[self.name]
        if pth is not None:
            if pth_test(pth):
                return pth

        # Look in default_paths:
        if self.default_paths is None or not len(self.default_paths):
            print "\tNo default paths given, skipping"
        else:
            # 1) - Expand PyExecPaths and OriginalSystemPaths placeholders
            if Tool.PyExecPaths in self.default_paths:
                self.default_paths.remove(Tool.PyExecPaths)
                self.default_paths.extend(get_python_scripts_dirs())
            if Tool.OriginalSystemPaths in self.default_paths:
                self.default_paths.remove(Tool.OriginalSystemPaths)
                self.default_paths.extend(os.environ["PATH"].split(os.pathsep))
            # 2) - Do the lookup (might be possible to speed things up later on)
            for pth in self.default_paths:
                matches = glob.glob( pth )
                if len(matches):
                    matches.sort()
                    pth = matches[-1] # -1 is supposed toget highest version
                    if pth_test(pth):
                        return pth

        if not self.installable or no_install:
            return False

        # Is it installed locally?
        wp = Formula().get_working_path()
        archpath = pj(wp, self.arch_name)
        toolpath = pj(wp, self.name)

        pth = into_subdir(toolpath, self.archive_subdir)
        if pth is not None:
            if pth_test(pth):
                return pth

        # Haven't found it yet, let's install it in wdr
        if self.url is None:
            print "\tNo url to download tool from, skipping"
            return None
        if not self.__prompt_user():
            print "\tUser refused download"
            return None

        print "\tWill now install %s to %s"%(self.name, wp)
        if not url(self.url, archpath, self.arch_name):
            print "\tCouldn't download", self.name
            return None
        if not unpack(archpath, toolpath):
            print "\tCouldn't unpack", self.name
            return None

        pth = into_subdir(toolpath, self.archive_subdir)
        return pth if pth_test(pth) else None

    def __prompt_user(self):
        """Prompt the user for download, wait 5 seconds and download if no input"""
        do_dl = None
        delay = 5000
        def ask_user_if_download():
            try:
                do_dl = raw_input().lower() == "y"
            except:
                do_dl = True

        prompt = "\tLocally install %s (%s seconds)? (y/n, default:y): \r"
        def print_prompt():
            sys.stdout.write(prompt%(self.name, delay))
            sys.stdout.flush()

        thInput = threading.Thread(target=ask_user_if_download)
        thInput.start()
        while delay > 0 and do_dl is None:
            if delay%1000==0:
                print_prompt()
            delay -= 1
            time.sleep(1/1000)
        thInput._Thread__stop()
        if do_dl is None:
            do_dl = True
        return do_dl

