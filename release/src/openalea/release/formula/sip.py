from openalea.release import Formula
from openalea.release.utils import sh, apply_patch, pj, option_to_sys_path
from openalea.release.formula.qt4 import qt4
from openalea.release.formula.bisonflex import bisonflex
import sys
from os.path import abspath, dirname, exists

PATCH_DIR = abspath(dirname(__file__))

class sip(Formula):
    download_url = "http://sourceforge.net/projects/pyqt/files/sip/sip-4.14.7/sip-4.14.7.zip"
    #download_url = "http://www.riverbankcomputing.com/hg/sip/archive/0869eb93c773.zip" #downloading from the mercurial tag
    #download_url = "http://www.riverbankcomputing.com/hg/sip/archive/0869eb93c773.zip" #downloading from the mercurial tag
    #url = "http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-4.13.2.zip"
    download_name  = "sip_src.zip"
    
    required_tools = ['bisonflex']

    def __init__(self, *args, **kwargs):
        super(sip, self).__init__(*args, **kwargs)
        # we install pyqt4 binaries in the qt bin installation directory to easily recover it
        # for the egg. The eggs are built in the historical layout used by openalea packagers.
        # This doesn't mean it's good. It doesn't mean it's bad though it does look a bit messy.
        qt4_ = qt4()
        self.install_bin_dir  = qt4_.install_bin_dir
        self.install_site_dir = pj(self.installdir, "site")
        self.install_inc_dir  = pj(self.installdir, "include")
        self.install_sip_dir  = pj(self.installdir, "sip")

        self.inst_paths = self.install_bin_dir, self.install_site_dir, self.install_inc_dir, \
                          self.install_sip_dir

    @option_to_sys_path("bisonflex_path")
    def configure(self):
        if exists(pj(self.sourcedir,"configure.py") ):
            # The -S flag is needed or else configure.py
            # sees any existing sip installation and can fail.
            return sh(sys.executable + \
                   " -S configure.py --platform=win32-g++ -b %s -d %s -e %s -v %s"%self.inst_paths) == 0
        else:
            #if configure.py doesn't exist then we might
            #be using a zipball retreived directly from
            #sip's mercurial repository. This type of source
            #needs a step before actually calling configure.py
            if exists("build.py"):
                print "Will try to build sip from mercurial source zipball"
                try:
                    #We neeeed bison and flex
                    sh("bison.exe")
                except:
                    print "Could not find bison flex, use --bisonflex"
                    return False
                apply_patch( pj(PATCH_DIR,"sip_build.patch") )
                sh(sys.executable + " -S build.py prepare")
                return self.configure()
            else:
                #we don't have a clue of what type of source we're in
                #so dying cleanly can seem like a good option:
                return False
    '''
    def make(self):
        return True
        
    def install(self):
        return True
    '''
    
    def extra_paths(self):
        return self.sourcedir, pj(self.sourcedir, "sipgen")

    def extra_python_paths(self):
        return self.sourcedir, pj(self.sourcedir, "siplib")

    def patch(self):
        return True
        
        '''
        # Patching sipconfig.py so that its
        # paths point to the qt4 egg path we are building.
        # Feel free to do better
        header = """
import re
from os.path import join as pj
from pkg_resources import Environment

# Default Path.
qtdev = os.environ.get('QTDIR') if 'QTDIR' in os.environ else 'C:\\Qt\\4.6.0'
sip_bin     = pj(sys.prefix,'sip')
sip_include = pj(sys.prefix, 'include')
env = Environment()
if 'qt4' in env:
    qt = env['qt4'][0].location # Warning: 0 is the active one
if 'qt4-dev' in env:
    qtdev       = env['qt4-dev'][0].location # Warning: 0 is the active one
    sip_bin     = pj(qtdev,'bin','sip.exe')
    sip_include = pj(qtdev, 'include')
    """

        txt = ""
        print "sip patching", os.getcwd()
        with open("sipconfig.py") as f:
            txt = f.read()

        # inject our new header
        txt = txt.replace("import re", header)

        prefix = sys.prefix.replace("\\", r"\\\\")
        # Evil massive regexp substitutions. RegExp are self-explanatory! Just kidding...
        txt = re.sub(r"(\s*'default_bin_dir':\s*)'%s'"%prefix,    r"\1sys.prefix", txt)
        txt = re.sub(r"(\s*'default_mod_dir':\s*)'%s.*'"%prefix,  r"\1pj(sys.prefix,'Lib\site-packages')", txt)
        txt = re.sub(r"(\s*'default_sip_dir':\s*)'[A-Z]:\\\\.*'", r"\1pj(qtdev,'sip')", txt)
        txt = re.sub(r"(\s*'py_conf_inc_dir':\s*)'%s.*'"%prefix,  r"\1pj(sys.prefix,'include')", txt)
        txt = re.sub(r"(\s*'py_inc_dir':\s*)'%s.*'"%prefix,       r"\1pj(sys.prefix,'include')", txt)
        txt = re.sub(r"(\s*'py_lib_dir':\s*)'%s.*'"%prefix,       r"\1pj(sys.prefix,'libs')", txt)
        txt = re.sub(r"(\s*'sip_bin':\s*)'[A-Z]:\\\\.*'",         r"\1sip_bin", txt)
        txt = re.sub(r"(\s*'sip_inc_dir':\s*)'[A-Z]:\\\\.*'",     r"\1sip_include", txt)
        txt = re.sub(r"(\s*'sip_mod_dir':\s*)'[A-Z]:\\\\.*'",     r"\1qt", txt)

        shutil.copyfile( "sipconfig.py", "sipconfig.py.old" )
        with open( pj(self.install_site_dir,"sipconfig.py"), "w") as f:
            f.write(txt)

        return True
        '''