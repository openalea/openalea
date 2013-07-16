import traceback
import sys, os
import subprocess
import shutil
import glob
import zipfile
import tarfile
import string
import fnmatch
from path import path
import requests
from re import compile as re_compile

from os.path import join as pj, splitext, split
from collections import defaultdict

# WARNING :  use deploy here
from openalea.deploy.system_dependencies import patch
from openalea.deploy.util import get_repo_list
from setuptools.package_index import PackageIndex
import logging

__oldsyspath__ = sys.path[:]

pi = PackageIndex(search_path=[])
pi.add_find_links(get_repo_list())

sj = os.pathsep.join

def uj(*args):
    """Unix-style path joining, useful when working with qmake."""
    return "/".join(args)
    
def get_logger():
    # TODO : doesn't write in the file if user doesn't want
    logger = logging.Logger('log')
    hdlr = logging.FileHandler('./formula.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter) 
    logger.addHandler(hdlr) 
    return logger    

logger = get_logger()

# A file object to redirect output to NULL:
NullOutput = open("NUL", "w")
    
############################################
# A few decorators to factor out some code #
############################################
def try_except( f ) :
    """Encapsulate the function in a try...except structure
    which prints the exception traceback and returns False on exceptions
    or returns the result of f on success."""
    def wrapper(self, *args, **kwargs):
        try:
            ret = f(self, *args, **kwargs)
        except:
            traceback.print_exc()
            return False
        else:
            return ret
    wrapper.__name__ = f.__name__
    return wrapper

def in_dir(directory):
    def dir_changer( f ) :
        """Encapsulate f in a structure that changes to getattr(self,directory),
        calls f and moves back to BuildEnvironment.get_working_path()"""
        def wrapper(self, *args, **kwargs):
            d_ = rgetattr(self, directory)
            message = "changing to %s for %s" %(d_,f.__name__)
            logger.debug(message)
            os.chdir(d_)
            ret = f(self, *args, **kwargs)
            os.chdir(self.get_working_path())
            return ret
        wrapper.__name__ = f.__name__
        return wrapper
    return dir_changer
    
def with_original_sys_path(f):
    """Calls the decorated function with the original PATH environment variable"""
    def func(*args,**kwargs):
        cursyspath = sys.path[:]
        sys.path = __oldsyspath__[:]
        ret = f(*args, **kwargs)
        sys.path = cursyspath
        return ret
    return func
   
def make_silent(self, silent):
        if silent:
            sys.stdout = self.null_stdout
            sys.stderr = self.null_stdout
        else:
            sys.stdout = self.original_stdout
            sys.stderr = self.original_stderr
            
def memoize(attr):
    def deco_memoize(f):
        def wrapper(self, *args, **kwargs):
            if getattr(self, attr, None) is None:
                v = f(self, *args, **kwargs)
                setattr(self, attr, v)
            return getattr(self, attr)
        return wrapper
    return deco_memoize
    
def option_to_sys_path(option):
    """If optionnal argument "option" was provided on the command line
    it will be prepended to the PATH just for the call this function decorates.
    After the call, the original environment will be restored."""
    def func_decorator(f):
        def wrapper(self, *args, **kwargs):
            opt_pth = self.options.get(option)
            if opt_pth:
                prev_pth = os.environ["PATH"]
                os.environ["PATH"] = sj([opt_pth, prev_pth])
                ret = f(self, *args, **kwargs)
                os.environ["PATH"] = prev_pth
            else:
                message = "option_to_sys_path: %s not provided" %option
                logger.warn(message)
                ret = f(self, *args, **kwargs)
            return ret
        return wrapper
    return func_decorator
   
def option_to_python_path(option):
    """If optionnal argument "option" was provided on the command line
    it will be appended to the PYTHONPATH and sys.path vars just for the
    call this function decorates. After the call, the original environment
    will be restored."""
    def func_decorator(f):
        def wrapper(self, *args, **kwargs):
            opt_pth = self.options.get(option)
            if opt_pth:
                # save original values
                prev_pth = sys.path[:]
                prev_py_pth = os.environ.get("PYTHONPATH", "")
                # modify environment
                sys.path += opt_pth.split(";")
                os.environ["PYTHONPATH"] = sj([opt_pth, prev_py_pth])
                # call the function
                ret = f(self, *args, **kwargs)
                # restore original values
                sys.path = prev_pth
                os.environ["PYTHONPATH"] = prev_py_pth
            else:
                message = "option_to_python_path: %s not provided" %option
                logger.warn(message)
                ret = f(self, *args, **kwargs)
            return ret
        return wrapper
    return func_decorator
   
############################################
# Useful small functions                   #
############################################

def sh(cmd,shell=True):
    """ Execute a cmd """
    return subprocess.call(cmd, shell=shell)

def url(name, dir=None, dl_name=None):
    """ Download from url into dir and renamed it into dl_name. 
    """
    ret = True
    
    if dir is None:
        dir = '.'
    dir = path(dir).abspath()
    if not dir.exists():
        makedirs(dir)
    
    filename = name.split('/')[-1]
    filename = filename.split('#')[0]
    complete_fn = dir/filename
    if dl_name:
        complete_fn = dir/dl_name

    try:
        reponse = requests.get(name)
        with open(complete_fn, "wb") as code:
            code.write(reponse.content)
            logger.debug("%s Downloaded." %filename)
            ret = complete_fn
    except:
        ret = False
        
    return ret
 
def install(filename):
    ext = filename.split(".")[-1]
    if ext.lower() == "msi":
        sh('msiexec /i %s' %filename)
        logger.debug("%s Installed." %filename)
    elif ext.lower() == "exe":
        sh(filename)
        logger.debug("%s Installed." %filename)
    else:
        logger.debug("---We can't install %s. Unknow extension.---" %filename)
 
def apply_patch(patchfile):
    """ Apply patch from file
    """
    p = patch.fromfile(patchfile)
    return p.apply()   

def get_dirs():
    """ Return list of directories to create.
        - install dir (install): where 3rd party will be installed
        - source dirs (src): where svn dirs will be checkout
        - egg dirs (egg): where "bdist_egg" will work
        - download dirs (dl) : where files will be download
        - dist dirs (dist) : where the final release files will be copied
    """
    cwd = path(os.getcwd())
    dirs = [
       cwd/"dl",
       cwd/"src",
       cwd/"install",
       cwd/"dist",
       cwd/"egg",
       ]
    return dirs

def rm_temp_dirs():
    """ Remove old directories."""
    dirs = get_dirs()
    for f in dirs:
        if f.exists():
            if f.isdir():
                f.rmtree()
            else:
                f.remove()
        else:
            logger.debug( "Can't remove %s" %f)
    
def mk_temp_dirs():
    """ Create the working directories:
    """
    dirs = get_dirs()
    makedirs(dirs)

def download_egg(eggname, dir):
    """Download an egg to a specific place
    
    :param eggname: name of egg to download
    :param dir: destination directory
    :return: local path
    """
    logger.debug("Downloading %s"%eggname)
    return pi.download(eggname, dir)
        
def checkout(url, dir=None):
    """ Checkout (SVN) url into dir
    """
    if dir is None:
        dir = '.'
    dir = path(dir)
    cmd = "svn co %s %s " %(url, dir)
    sh(cmd)    
    
def set_windows_env():
    """ Set window environment path
    """
    cmd = "set PATH=%PATH%;%INNO_PATH%;%SVN_PATH%;%PYTHON_PATH%;%PYTHON_PATH%\Scripts"
    sh(cmd)
'''
def unpack(arch, where):
    """ Unpack a ZIP, TGZ or TAR file from 'where'
    """
    arch = arch
    base, ext = splitext( arch )
    logger.debug("unpacking %s" %arch)
    # TODO : verify that there is no absolute path inside zip.
    if ext == ".zip":
        zipf = zipfile.ZipFile( arch, "r" )
        zipf.extractall( path=where )
    elif ext == ".tgz":
        tarf = tarfile.open( arch, "r:gz")
        tarf.extractall( path=where )
    elif ext == ".tar":
        tarf = tarfile.open( arch, "r")
        tarf.extractall( path=where )
    logger.debug("done")
    return True
'''   
def unpack(arch, where):
    """ Unpack a ZIP, TGZ or TAR file from 'where'
    """
    arch = arch
    base, ext = splitext( arch )
    logger.debug("unpacking %s" %arch)
    # TODO : verify that there is no absolute path inside zip.
    if ext == ".zip":
        zipf = zipfile.ZipFile( arch, "r" )
        zipf.extractall( path=where )
    elif ext == ".tgz":
        tarf = tarfile.open( arch, "r:gz")
        tarf.extractall( path=where )
    elif ext == ".tar":
        tarf = tarfile.open( arch, "r")
        tarf.extractall( path=where )
    logger.debug("done")
    
    # If ZIP contained only one directory, unpack move everything.
    # ex:
    # ./ann_src.zip/ann_1.1.2/... will begin after unpack ./ann_src/...
    where = path(where).abspath()
    listdirs = os.listdir(where)
    if len(listdirs) == 1:
        from_dirs = where/listdirs[0]
        move(from_dirs, where)
    return True
    
def move(from_src, to_src):
    """ Move a tree from from_src to to_src.
    """
    # If 'from' inside 'to' move in a temp repo and works well
    if to_src in from_src:
        temp_src = path(to_src)/".."/".temp"
        shutil.move(from_src, temp_src)
        from_src = temp_src
    # If 'to' already exists, erase it... Careful!
    if path(to_src).exists():
        shutil.rmtree(to_src)
    shutil.move(from_src, to_src)
    return True

class Later(object):
    """ Just a way to be able to check if a process should be done later,
    and not mark it as done or failed (the third guy in a tribool)"""
    pass

def rgetattr(c, attrs):
    """Like getattr, except that you can provide sub attributes:

    >>> rgetattr(obj, "attr.subattr")
    """
    attrs = attrs.split(".")
    value = c
    while len(attrs):
        value = getattr(value, attrs.pop(0))
    return value

class TemplateStr(string.Template):
    delimiter = "@"
    
def into_subdir(base, pattern):
    if pattern is not None:
        pths = glob.glob(pj(base,pattern))
        if len(pths):
            return pths[0]
        else:
            return None
    else:
        return base
        
CompiledRe = type(re_compile(""))
def recursive_glob(dir_, patterns=None, strip_dir_=False, levels=-1):
    """ Goes down a file hierarchy and returns files paths
    that match filepatterns or regexp."""
    files = []
    if isinstance(patterns, CompiledRe):
        filepatterns, regexp = None, patterns
    else:
        filepatterns, regexp = patterns.split(","), None

    lev = 0
    for dir_path, sub_dirs, subfiles in os.walk(dir_):
        if lev == levels:
            break
        if filepatterns:
            for pat in filepatterns:
                for fn in fnmatch.filter(subfiles, pat):
                    files.append( os.path.join(dir_path, fn) )
        elif regexp:
            for fn in subfiles:
                if regexp.match(fn): files.append(os.path.join(dir_path, fn))
        lev += 1
    dirlen = len(dir_)
    return files if not strip_dir_ else [ f[dirlen+1:] for f in files]

def recursive_glob_as_dict(dir_, patterns=None, strip_dir_=False,
                           strip_keys=False, prefix_key=None, dirs=False, levels=-1):
    """Recursively globs files and returns a list of the globbed files.
    The globbing can use regexps or shell wildcards.
    """
    files     = recursive_glob(dir_, patterns, strip_dir_, levels)
    by_direct = defaultdict(list)
    dirlen = len(dir_)
    for f in files:
        target_dir = split(f)[0]
        if strip_keys:
            target_dir = target_dir[dirlen+1:]
        if prefix_key:
            target_dir = pj(prefix_key, target_dir)
        if dirs:
            f = os.path.split(f)[0]
            if f not in by_direct[target_dir]:
                by_direct[target_dir].append(f)
        else:
            by_direct[target_dir].append(f)
    return by_direct
    
    
def ascii_file_replace(fname, oldstr, newstr):
    """ Tries to find oldstr in file fname and replaces it with newstr.
    Doesn't do anything if oldstr is not found.
    File is overwritten. Doesn't handle any exception.
    """
    txt = ""
    patch = False
    with open(fname) as f:
        txt = f.read()

    if oldstr in txt:
        patch = True
        txt = txt.replace(oldstr, newstr)

    if patch:
        with open(fname, "w") as f:
            logger.debug("patching %s" %fname)
            f.write(txt)
            
def merge_list_dict(li):
    """ Converts li which is a list of (key,value) into
    a dictionnary where items with the same keys get appended
    to a list instead of overwriting the key."""
    d = defaultdict(list)
    for k, v in li:
        d[k].extend(v)
    return dict( (k, sj(v)) for k,v in d.iteritems() )
    
# -- Glob and regexp patterns --
class Pattern:
    # -- generalities --
    any     = "*"
    exe     = "*.exe"
    dynlib  = "*.dll"
    stalib  = "*.a"
    include = "*.h,*.hxx"

    # -- pythonities --
    pymod   = "*.py"
    pyext   = "*.pyd"
    pyall   = ",".join([pymod, pyext])

    # -- scintillacities --
    sciapi  = "*.api"

    # -- sip --
    sipfiles = "*.sip"

    # -- Qtities --
    qtstalib = "*.a,*.prl,*.pri,*.pfa,*.pfb,*.qpf,*.ttf,README"
    qtsrc    = "*"#.pro,*.pri,*.rc,*.def,*.h,*.hxx"
    qtinc    = re_compile(r"^Q[0-9A-Z]\w|.*\.h|^Qt\w")
    qtmkspec = "*"
    qttransl = "*.qm"
    
def recursive_copy(sourcedir, destdir, patterns=None, levels=-1, flat=False):
    """Like shutil.copytree except that it accepts a filepattern or a file regexp."""
    src = recursive_glob( sourcedir, patterns, levels=levels )
    dests = [destdir]*len(src) if flat else \
            [ pj(destdir, f[len(sourcedir)+1:]) for f in src]
    bases = set([ split(f)[0] for f in dests])
    for pth in bases:
        makedirs(pth)
    for src, dst in zip(src, dests):
        #print src, dst
        shutil.copy(src, dst)
        
def makedirs(pth, verbose=False):
    """ A wrapper around os.makedirs that prints what
    it's doing and catches harmless errors. """
    try:
        os.makedirs( pth )
    except os.error:
        if verbose:
            traceback.print_exc()
         
def get_python_scripts_dirs():
    dirs = []
    for pth in sorted(sys.path):
        pth = [part for part in pth.split(os.sep)]
        try:
            pth_low = [part.lower() for part in pth]
            idx = pth_low.index("lib")
        except:
            continue
        else:
            script_dir_name = "scripts" if sys.platform == "win32" else "bin"
            script_path = pj(*pth[:idx]+[script_dir_name])
            # sys.path contains absolute namesso the split operation above has to
            # be compensated:
            if sys.platform == "win32":
                # restore "driveletter:\\" on windows
                script_path = script_path.replace(":", ":"+os.sep)            
            else:
                # restore "/" on unixes
                script_path = "/"+script_path
            if script_path not in dirs:
                dirs.append(script_path)
    return dirs
    
    
    
    
    
    
########################################    
## UNINSTALL   
########################################     
def get_python_dir():
    return path(sys.prefix)/'Lib'/'site-packages'

def scripts_dir():
    return path(sys.prefix)/'Scripts'

def remove_packages(dirs):

    # TODO : svn remove
    for f in dirs:
        if f.exists():
            if f.isdir():
                f.rmtree()
            else:
                f.remove()
        else:
            print "Can't remove %s" %f
                
def uninstall_all():
    """ Try to remove all the openalea, Vplants and alinea packages
    """
    pp = get_python_dir() # python_path
    
    # remove egg-link
    oa = pp.glob('openalea*.egg-link')
    vp = pp.glob('vplants*.egg-link')
    al = pp.glob('alinea*.egg-link')
    remove_packages(oa+vp+al)
            
    # remove egg
    oa = pp.glob('openalea*.egg')
    vp = pp.glob('vplants*.egg')
    al = pp.glob('alinea*.egg')
    remove_packages(oa+vp+al)
        
    # remove shared_lib.pth
    pths = pp.glob('shared-lib.pth')
    if pths:
        if pths[0].exists():
            pths[0].remove()
        else:
            print "Can't remove %s" %pths[0]
    
    # Modify the easy_install.pth file
    pths = pp.glob('easy-install.pth')
    eapth = pths[0]
    
    f = eapth.open()
    easy = f.read()
    f.close()
    
    new_ea = []
    for l in easy.split('\n'):
        if 'openalea' in l.lower() or 'vplants' in l.lower():
            pass
        else:
            new_ea.append(l)
            
    s = '\n'.join(new_ea)
    f = eapth.open('w')
    f.write(s)
    f.close()
    
    # Uninstall scripts 
    # How to know what are the installed console scripts?
    scripts = scripts_dir()
    # remove alea
    l = scripts.glob('alea*')
    l+= scripts.glob('aml2py*')
    l+= scripts.glob('cpfg2lpy*')
    l+= scripts.glob('flowerdemo*')
    l+= scripts.glob('gforge*')
    l+= scripts.glob('lpy*')
    l+= scripts.glob('make_develop*')    
    l+= scripts.glob('phyllotaxis*')    
    l+= scripts.glob('upload_dist*')
    l+= scripts.glob('visualea*')
    l+= scripts.glob('vplab*')
    l+= scripts.glob('secondnature*')
    
    remove_packages(l)
        
    # Update Environment variable
    
    # Change PATH before changing OPENALEA_LIB
    # Remove the registery in the same spirit than environ_var in deploy...
    # TODO
    """
    import _winreg
    regpath = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    key = _winreg.OpenKey(reg, regpath, 0, _winreg.KEY_ALL_ACCESS)
    libs = _winreg.QueryValueEx(key,'PATH')[0]
    libs = libs.split(';')
    
    new_libs = []
    
    for l in libs:
        if "%OPENALEA_LIB%" not in l:
            new_libs.append(l)
    
    set_win_env['PATH=%s'%new_libs]"""
    
    # Remove dirs in openalea_lib
    libs=os.environ['OPENALEA_LIB']
    libs = libs.split(';')
    # extract all the egg from OPENALEA_LIB
    eggs = [path(x.split('egg')[0]+'egg') for x in libs if 'egg' in x]
    
    remove_packages(eggs)
    
    sh_libs = [path(x) for x in libs if 'shared_libs' in x]
    remove_packages(sh_libs)

    libs = [path(x) for x in libs if 'egg' not in x and 'shared_libs' not in x]
    
    os.putenv('OPENALEA_LIB','')