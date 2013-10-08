import sys, os
import datetime
import glob
import shutil
from os.path import abspath, dirname
from os.path import join as pj, splitext, exists
from path import path

from openalea.release.utils import unpack as utils_unpack
from openalea.release.utils import install as util_install
from openalea.release.utils import in_dir, try_except, TemplateStr, sh, sj, makedirs
from openalea.release.utils import Pattern, recursive_glob_as_dict, get_logger, url

from openalea.release.aliases import dependency_filter

logger = get_logger()   
    
def eggify_formula(formula_name, dest_dir=None):
    """
    Build egg
    :param formula_name: string name (or list of strings) of the formula
    :param dest_dir: directory where to put the egg when it is created
    :return: instance of the eggified formula
    """
    formula_name = dependency_filter(formula_name)
    
    if isinstance(formula_name, list):
        # Works with a list of formula
        for form in formula_name:
            eggify_formula(form, dest_dir=dest_dir)
    else:    
        # import formula
        cmd_import = "from openalea.release.formula.%s import %s" %(formula_name,formula_name)
        exec(cmd_import, globals(), locals())
        
        # instanciate formula
        cmd_instanciate = "%s()" %formula_name
        formula = eval(cmd_instanciate)

        if dest_dir is not None:
            formula.dist_dir = abspath(dest_dir)
        
        ret = True
        ret = ret & formula._download()
        ret = ret & formula._unpack()
        ret = ret & formula._patch()
        
        ret = ret & formula._install()
        
        ret = ret & formula._configure()
        ret = ret & formula._make()
        ret = ret & formula._make_install()

        ret = ret & formula._bdist_egg()
        
        ret = ret & formula._copy_installer()
        
        logger.debug("Eggify formula %s, success : %s" %(formula_name,ret))
        return formula, ret

############################################
# Formula                                  #
############################################
class Formula(object):
    required_tools = None
    version = '1.0'
    description = ""
    homepage = ""
    license = ""
    authors = ""
    # List of dependencies of the formula
    dependencies = ""
    # The URL to fetch the sources from
    # A None url implies the download has already done by someone else
    download_url = None
    # Name of the  local archive
    download_name  = ""
    # The egg depends on the Python version (allows correct egg naming)
    py_dependent   = True
    # The egg depends on the os and processor type (allows correct egg naming)
    arch_dependent = True 
    # Only for package like Pillow which use another name for import (<<import Pil>> and not <<import Pillow>>)
    __packagename__ = None
    working_path  = os.getcwd()

    DOWNLOAD = UNPACK = PATCH = INSTALL = CONFIGURE = MAKE = MAKE_INSTALL = EGGIFY = COPY_INSTALLER = False
    
    def __init__(self,**kwargs):
        logger.debug("__init__ %s" %self.__class__)
        #self.done_tasks = {}
        self.options = {} 
        #self.pending = None
        self.dldir = self._get_dl_path()
        self.archname  = pj( self._get_dl_path() , self.download_name)
        self.sourcedir = pj( self._get_src_path(), splitext(self.download_name)[0] )
        self.installdir = pj( self._get_install_path(), splitext(self.download_name)[0] )
        self.install_inc_dir = pj(self.installdir, "include")
        self.install_lib_dir = pj(self.installdir, "lib")        
        self.dist_dir = self._get_dist_path()
        
        # Variable to check if the source directory is yet fixed
        self._source_dir_fixed = False

        if "no_env" in kwargs:
            self.eggdir         = ""
            self.setup_in_name  = ""
        else:
            self.eggdir         = pj(self._get_egg_path(), self.egg_name())
            self.setup_in_name  = pj(abspath(dirname(__file__)), "setup.py.in")
        self.setup_out_name = pj(self.eggdir, "setup.py")
        self.use_cfg_login  = False # ?
        
        makedirs(self._get_src_path())
        makedirs(self._get_install_path())
        makedirs(self.sourcedir)
        makedirs(self._get_dl_path())
        makedirs(self.dist_dir)
        makedirs(self.eggdir)
        
        makedirs(self.installdir)
        

    def default_substitutions_setup_py(self):
        """
        :return: default dict to fill "setup.py" files
        """
    
        # if package is python and yet installed
        try:
            packages, package_dirs = self.find_packages_and_directories()
            
            install_dir = os.path.dirname(self.package.__file__)

            # py_modules = recursive_glob(self.install_dir, Pattern.pymod)
            data_files = recursive_glob_as_dict(install_dir,
                        ",".join(["*.example","*.txt",Pattern.pyext,"*.c",".1"])).items()
        # evreything else
        except:
            packages, package_dirs, data_files = None, None, None
                        
        d = dict ( NAME                 = self.egg_name(),
                   VERSION              = self.version,
                   THIS_YEAR            = datetime.date.today().year,
                   SETUP_AUTHORS        = "Openalea Team",
                   CODE_AUTHOR          = self.authors,
                   DESCRIPTION          = self.description,
                   HOMEPAGE             = self.homepage,
                   URL                  = self.download_url,
                   LICENSE              = self.license,

                   ZIP_SAFE             = False,
                   PYTHON_MODS          = None,
                   PACKAGE_DATA         = {},

                   INSTALL_REQUIRES     = self.required_tools,
                   
                   PACKAGES             = packages,
                   PACKAGE_DIRS         = package_dirs,
                   DATA_FILES           = data_files,
                   LIB_DIRS             = None,
                   INC_DIRS             = None,
                   BIN_DIRS             = None,
                  )
            
        lib = path(self.sourcedir)/'lib'
        inc = path(self.sourcedir)/'include'
        bin = path(self.sourcedir)/'bin'

        if lib.exists(): d['LIB_DIRS'] = {'lib' : pj(self.sourcedir,'lib') }
        if inc.exists(): d['INC_DIRS'] = {'include' : pj(self.sourcedir,'include') }
        if bin.exists(): d['BIN_DIRS'] = {'bin' : pj(self.sourcedir,'bin') }
        
        return d

    def get_dependencies(self):
        """
        :return: list of dependencies of the formula 
        """
        if self.dependencies is None:
            self.dependencies = ""
        return list(self.dependencies)
    
    @property
    def name(self):
        return self.__class__.__name__
    
    @classmethod
    def egg_name(cls):
        return cls.__name__.split("egg_")[-1]
        
    def _download(self):
        if self.DOWNLOAD:
            # a proj with a none url implicitely means
            # the sources are already here because some
            # other proj installed it.
            if self.download_url is None:
                return True    
            dir=self._get_dl_path()
            if self.download_name in os.listdir(dir):
                message = "%s already downloaded!" %self.download_name
                logger.debug(message) 
                return True
            else:
                ret = url(self.download_url, dir=self._get_dl_path(), dl_name=self.download_name)
                logger.debug("Download %s" %ret)
                return bool(ret)
        return True
    
    def _unpack(self):
        if self.UNPACK:
            # a proj with a none url implicitely means
            # the sources are already here because some
            # other proj installed it.
            if self.download_url is None:
                logger.debug("No url")
                ret = True
            if exists(self.sourcedir):
                if os.path.getsize(self.sourcedir) > 0:
                    message =  'already unpacked in %s' %repr(self.sourcedir)
                    logger.debug(message)
                    ret = True
                else:
                    ret = self.unpack()
            else:
                ret = self.unpack()
            logger.debug("Unpack %s" %ret)
            return ret 
        return True
    
    # def _permanent_extend_sys_path(self):
        #### Do NOT USE "REG ADD..." !!!
        # """
        # Warnings: this method extend PERMANENTLY Path for WINDOWS (and only windows) and need a REBOOT of the computer
        
        # more here:
        # http://fr.wikipedia.org/wiki/Variable_d%27environnement#.3CPATH.3E_pour_l.27emplacement_des_ex.C3.A9cutables
        # and here:
        # http://technet.microsoft.com/fr-fr/library/cc742162%28v=ws.10%29.aspx
        
        # Modifie register... So, please use it carefully...
        
        ### TODO: test it...
        # """
        # exp = self.extra_paths()
        # if exp is not None:
            ### _permanent_extend_sys_path not tested...
            # warnnings.warn("You need to restart the computer to really extend the Path!")
            # cmd = 'REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /d "%PATH%;%s" /f', %exp
            # return sh(cmd) == 0
        ### nothing to add in sys path
        # return True
            
    # def _permanent_extend_python_path(self):
        # """
        # See _permanent_extend_sys_path
        
        # Same for PYTHON_PATH and not PATH
        # """
        # exp = self.extra_python_paths()
        # if exp is not None:
            ### _permanent_extend_python_path not tested...
            # warnnings.warn("You need to restart the computer to really extend the Python_Path!")
            # cmd = 'REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Python_path /d "%PYTHON_PATH%;%s" /f', %exp
            # return sh(cmd) == 0
        ### nothing to add in sys path
        # return True
        
    def _extend_sys_path(self):
        exp = self.extra_paths()
        if exp is not None:
            if isinstance(exp, tuple):
                exp = sj(exp)
            os.environ["PATH"] = sj([exp,os.environ["PATH"]])

            # cmd = " PATH "
            # for e in exp.split(";"):
                # cmd = cmd + "\"" + e + "\";"
            # cmd = cmd + "%PATH%"
            cmd = " PATH \""
            for e in exp.split(";"):
                cmd = cmd + e + ";"
            cmd = cmd + "%PATH%\""            
            
            # set temp PATH
            cmd1 = "SET" + cmd
            logger.debug( cmd1 )
            sh(cmd1)
            
            # set permanent PATH
            cmd2 = "SETX" + cmd
            logger.debug( cmd2 )
            sh(cmd2)
            
        return True

    def _extend_python_path(self):
        exp = self.extra_python_paths()
        if exp is not None:
            if isinstance(exp, tuple):
                sys.path.extend(exp)
                exp = sj(exp)
            elif isinstance(exp, str):
                sys.path.extend(exp.split(os.pathsep))

            os.environ["PYTHON_PATH"] = sj([exp,os.environ.get("PYTHON_PATH","")])
            
            cmd = " PYTHON_PATH "
            for e in exp.split(";"):
                cmd = cmd + "\"" + e + "\";"
            cmd = cmd + "%PYTHON_PATH%"
            
            # set temp PYTHON_PATH
            cmd1 = "SET" + cmd
            logger.debug( cmd1 )
            sh(cmd1)
            
            # set permanent PYTHON_PATH
            cmd2 = "SETX" + cmd
            logger.debug( cmd2 )
            sh(cmd2)

        return True

    # -- Top level process, they delegate to abstract methods, try not to override --
    @in_dir("sourcedir")
    @try_except
    def _configure(self):
        if self.CONFIGURE:
            self._extend_sys_path()
            self._extend_python_path()
            ret = self.configure()
            logger.debug("Configure %s" %ret)
            return ret
        return True
        
    @in_dir("sourcedir")
    @try_except
    def _make(self):
        if self.MAKE:
            ret = self.make()
            logger.debug("Make %s" %ret)
            return ret
        return True
        
    @in_dir("sourcedir")
    @try_except
    def _patch(self):
        if self.PATCH:
            ret = self.patch()
            logger.debug("Patch %s" %ret)
            return ret
        return True
        
    @in_dir("sourcedir")
    @try_except
    def _make_install(self):
        if self.MAKE_INSTALL:
            ret = self.make_install()
            logger.debug("Make_install %s" %ret)
            return ret 
        return True
        
    @in_dir("dldir") 
    @try_except
    def _install(self):
        if self.INSTALL:
            ret = self.install()
            logger.debug("Install %s" %ret)
            return ret
        return True
        
    @try_except
    def _configure_script(self):
        with open( self.setup_in_name, "r") as input, \
             open( self.setup_out_name, "w") as output:
             
            conf = self.default_substitutions_setup_py()
            conf.update(self.setup())
            conf = dict( (k,repr(v)) for k,v in conf.iteritems() )
            template = TemplateStr(input.read())
            output.write(template.substitute(conf))
        return True

    @in_dir("eggdir")
    @try_except
    def _bdist_egg(self):
        if self.EGGIFY:
            ret = self._configure_script()     
            ret = ret & self.bdist_egg()
            logger.debug("Bdist_egg %s" %ret)
            return ret
        return True
        
    @in_dir("eggdir")
    @try_except
    def _upload_egg(self):
        return True
        # if not self.options["login"] or not self.options["passwd"]:
            # self.use_cfg_login = True
            # ret = self.upload_egg()
            # if not ret:
                # warnings.warn("No login or passwd provided, skipping egg upload")
                # logger.warn( "No login or passwd provided, skipping egg upload" )
                # return Later
            # return ret
        # return self.upload_egg()
    
    @in_dir("dldir") 
    @try_except    
    def _copy_installer(self):
        if self.COPY_INSTALLER:
            return self.copy_installer()
        return True

    def unpack(self):
        return utils_unpack(self.archname, self.sourcedir)
            
    def setup(self):
        return(dict())

    # -- The ones you can override are these ones --
    def copy_installer(self):
        shutil.copy(self.download_name, pj(self.dist_dir, self.download_name))
        return True
    
    def extra_paths(self):
        return None
        
    def extra_python_paths(self):
        return None
        
    def patch(self):
        return True        
        
    def install(self):
        return util_install(self.download_name)

    def configure(self):
        return True
        
    def make(self):
        try:
            opt = str(self.options["jobs"])
        except:
            opt = None
        logger.debug(opt) 
        if opt:
            cmd = "mingw32-make -j " + str(self.options["jobs"])
        else:
            cmd = "mingw32-make"
        logger.debug(cmd)  
        return sh( cmd ) == 0

    def make_install(self):
        return sh("mingw32-make install") == 0

    def _glob_egg(self):
        eggs = glob.glob( pj(self.dist_dir, self.egg_name()+"*.egg") )
        return None if not eggs else eggs[0]    
        
    def bdist_egg(self):
        return sh(sys.executable + " setup.py bdist_egg -d %s"%(self.dist_dir,)) == 0
        
    def install_egg(self):
        # Try to install egg (to call after bdist_egg)
        egg = glob.glob( pj(self.dist_dir, self.egg_name()) )
        if egg:
            egg = egg[0]
        else: 
            return False
        cmd = "alea_install -H None -f . %s" %egg
        return sh(cmd) == 0

    def upload_egg(self):
        if not self.use_cfg_login:
            opts = self.options["login"], self.options["passwd"], \
                    self.egg_name(), "\"ThirdPartyLibraries\"", "vplants" if not self.options["release"] else "openalea"
            return sh(sys.executable + " setup.py egg_upload --yes-to-all --login %s --password %s --release %s --package %s --project %s"%opts) == 0
        else:
            opts = self.egg_name(), "\"ThirdPartyLibraries\"", "vplants" if not self.options["release"] else "openalea"
            return sh(sys.executable + " setup.py egg_upload --yes-to-all --release %s --package %s --project %s"%opts) == 0
    
    #################################
    ## Come from InstalledPackageEggBuilder
    #################################
    @property
    def package(self):
        return __import__(self.packagename)

    @property
    def packagename(self):
        return self.__packagename__ or self.egg_name()

    def _filter_packages(self, pkgs):
        parpkg = self.packagename + "."
        return [ p for p in pkgs if (p == self.packagename or p.startswith(parpkg))]

    def find_packages(self):
        from setuptools import find_packages
        install_dir = os.path.dirname(self.package.__file__)
        pkgs   = find_packages( pj(install_dir, os.pardir) )
        pkgs = self._filter_packages(pkgs)
        return pkgs

    def find_packages_and_directories(self):
        pkgs = self.find_packages()
        dirs = {}
        install_dir = os.path.dirname(self.package.__file__)
        base = abspath( pj(install_dir, os.pardir) )
        for pk in pkgs:
            dirs[pk] =  pj(base, pk.replace(".", os.sep))
        return pkgs, dirs          
            
    #################################
    ## Get PATHs
    #################################
    def get_working_path(self):
        return self.working_path
        
    def _get_dl_path(self):
        return pj( self.get_working_path(), "download")
    
    def _get_src_path(self):
        return pj( self.get_working_path(), "src")
    
    def _get_install_path(self):
        return pj( self.get_working_path(), "install")
        
    def _get_egg_path(self):
        return pj( self.get_working_path(), "egg")
        
    def _get_dist_path(self):
        return pj( self.get_working_path(), "dist")