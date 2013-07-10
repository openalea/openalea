""" Script to install OpenAlea dependencies 

First install Python and easy_install or pip

    # python
    http://python.org/ftp/python/2.7.5/python-2.7.5.msi
    
    # setup tool
    https://pypi.python.org/packages/source/s/setuptools/setuptools-0.7.4.tar.gz
    OR
    http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe

Then install path.py >> easy_install path.py
Then install request >> easy_install requests

Now install all the dependencies
Download the source from svn or tar.gz
Build the source
Create binary distribution and install it 
Create windows installer
Upload
"""

from path import path
import os
from os.path import abspath, dirname
from collections import OrderedDict, namedtuple
from openalea.release.utils import sh, install, checkout, url, rm_temp_dirs, \
mk_temp_dirs, set_windows_env

FILE_DIR = abspath(dirname(__file__))

def default():
    """ Return default url and path for download projects from url to path.
    Projects are "OpenAlea", "VPlants" and "Alinea".
    Struct is: OrderedDict(namedtuple('Project', 'url dir'))
    """
    URL_OA = "https://scm.gforge.inria.fr/svn/openalea/branches/release_1_0"
    URL_VP = "https://scm.gforge.inria.fr/svn/vplants/vplants/branches/release_1_0"
    URL_AL = "https://scm.gforge.inria.fr/svn/openaleapkg/branches/release_1_0"

    DIR_OA = path(os.getcwd())/"src"/"openalea"
    DIR_VP = path(os.getcwd())/"src"/"vplants"
    DIR_AL = path(os.getcwd())/"src"/"alinea"

    Project = namedtuple('Project', 'url dir')
    projects = OrderedDict()
    projects['openalea'] = Project(URL_OA,DIR_OA)
    projects['vplants'] = Project(URL_VP,DIR_VP)
    projects['alinea'] = Project(URL_AL,DIR_AL)
    return projects

######################################################################
#############       Install Dev dependencies            ##############
######################################################################  
def get_build_deps(filename = None):
    """ Return dict of dependencies:
    name : url
    
    :param filename: name of the file where dependencies are
    """
    dependencies = dict()
    
    if not filename:
        filename = path(FILE_DIR)/"urls.ini"
    else:
        filename = path(filename)

    if filename.exists():
        with open(filename, 'r') as f:
            for line in f:
                line = line.rstrip('\n').split(" ")
                dependencies[line[0]] = line[2]
        return dependencies
    else:
        print("%s doesn't exist." %filename)
        print("We can't install 3rd party dependencies.")
        return -1
    
def install_build_deps():
    """ Install the 3rd party dependencies needed for compiling (build) sources.
    """
    dependencies = get_build_deps()
        
    for dependency in dependencies:
        #   - TODO! Be smart and don't download if already here!
        filename = url(dependencies[dependency],"./dl")
        install(filename) 
        
######################################################################
#############       Install RunTime dependencies        ##############
######################################################################         
def get_rt_deps():
    ret = ["ann", "mingw", "mingw_rt", "qhull", "boost", "rpy2",\
    "qt4", "qt4_dev", "pyqt4", "qscintilla", "pyqscintilla",\
    "sip", "qglviewer", "pyqglviewer", "pylsm", "pil", "numpy",\
    "scipy", "matplotlib", "gnuplot", "cgal"]
    return ["numpy"]
    
def install_rt_deps():
    """ Install the 3rd party dependencies needed for runing (rt = runtime) packages.
    """
    dependencies = get_rt_deps()
        
    for dependency in dependencies:
        # import formula
        cmd_import = "from openalea.release.formula.%s import %s" %(dependency,dependency)
        exec(cmd_import, globals(), locals())
        
        # instanciate formula
        cmd_instanciate = "%s()" %dependency
        formula = eval(cmd_instanciate)
        
        # work with formula
        _install_formula(formula) 
        
def _install_formula(formula):
    print "========== INSTALL ", formula.__class__, " BEGIN ==========="
    formula._download()
    formula._unpack()
    formula._patch()
    formula._configure()
    formula._make()
    formula._install()
    print "========== INSTALL ", formula.__class__, " DONE ==========="   
        

######################################################################
#############       Bdist_egg                #########################
######################################################################
def bdist_egg_rt_deps():
    """ Install the 3rd party dependencies needed for runing (rt = runtime) packages.
    """
    dependencies = get_rt_deps()
        
    for dependency in dependencies:
        # import formula
        cmd_import = "from openalea.release.formula.%s import %s" %(dependency,dependency)
        exec(cmd_import, globals(), locals())
        
        # instanciate formula
        cmd_instanciate = "%s()" %dependency
        formula = eval(cmd_instanciate)
        
        # work with formula
        _bdist_egg_formula(formula)         
        
def _bdist_egg_formula(formula):
    print "========== EGGIFY ", formula.__class__, " BEGIN ==========="
    formula._fix_source_dir()
    formula._bdist_egg()
    print "========== EGGIFY ", formula.__class__, " DONE ==========="        

def bdist_egg():
    """
    Create eggs into ./"dist"
    """
    # -d option to give destination repository
    
    # python multisetup.py [build] [install] bdist_egg
    # [build] [install] useful???
    cwd = os.getcwd()
    dest = cwd/"dist"
    cmd = "python multisetup.py bdist_egg -d %s" %dest
    projects = default()
    for proj in projects:
        os.chdir(projects[proj].dir)
        sh(cmd)
        os.chdir(cwd)

def checkout_all():
    """ Checkout OpenAlea, VPlants and/or Alinea
    """
    projects = default()
    for proj in projects:
        checkout(projects[proj].url, projects[proj].dir)
   
def multisetup():
    """ Build and install each package
    """
    cwd = os.getcwd()
    projects = default()
    for proj in projects:
        os.chdir(projects[proj].dir)
        sh("python multisetup.py install")
        os.chdir(cwd)
    
def test():
    """ Run the test of each package.
    """
    cwd = os.getcwd()
    projects = default()
    for proj in projects:
        os.chdir(projects[proj].dir)
        # if return 1 : failed    (to verify)
        sh("python multisetup.py nosetests")
        os.chdir(cwd)

def check_source(openalea = True, vplants = True, alinea = True):
    """ Check if all the sources compile.
    
    :return: True if everything success to compile. False if something failed.
    """
    cwd = os.getcwd()
    success = True
    
    def try_compile(name="openalea"):
        try:
            sh("python multisetup.py build")
            print ""
            print("%s compilation succeed !" %name)
            print ""
            return True
        except:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("%s compilation Failed /!\ " %name)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")  
            return False
    projects = default()
    for proj in projects:
        os.chdir(projects[proj].dir)
        success = success & try_compile(proj)
        os.chdir(cwd)
        
    return success
    
def quality():
    """ Run pep8 or pylint and return the result
    """
    pass

def win_installer():
    """ TODO: Create a package which contains all the libs.
    
    !! Doesn't work for the moment !!
    """
    cwd = os.getcwd()
    
    temp_path = path(os.getcwd())/"src"/"openalea"/"deploy"/"scripts"/"winInstallers"
    os.chdir(temp_path)
    projects = default()
    for proj in projects:
        cmd = "python makeWinInstaller.py -u --gforge --pass-path -e system_deploy2_temp -s system_deploy2_temp -o openalea_wi -e %s %s" %(proj,proj)
        sh(cmd)

    os.chdir(cwd)
'''    
def nsis():
    """ Create a windows installer that contains all the egg.
    """
    pass
    
def upload():
    """ Upload the packages on the gforge.
    """
    pass
    
def superpack():
    """ Create an installer of OpenAlea + VPlants + Alinea
    """
    pass
'''    

def install_all():
    # print("1) remove temp dirs")
    # rm_temp_dirs() # remove dirs
    
    # print("\n2) make temp dirs")
    # mk_temp_dirs() # make dirs
    
    print("\n3) install admin deps (build)")
    install_build_deps() # install admin deps to use this script (Python, svn, ...)
    
    # print("\n4) set windows env")
    # set_windows_env() # set environ variables
    
    # print("\n5) checkout all (OpenAlea, VPlants, Alinea)")
    # checkout_all()
    
    print("\n6) install runtime deps (rt)")
    install_rt_deps() # install deps to run projects (matplotlib, numpy, scipy, ...)
    
    print("\n7) multisetup")
    multisetup()

    print("\n8) bdist runtime egg")
    bdist_egg_rt_deps()
    
    print("\n9) bdist openalea egg")
    bdist_egg()  
    
    # print("\n9) win_installer")
    # win_installer()
