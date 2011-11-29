# The point of this file is to create an inno setup script to install openalea/vplants
# on a machine without having to rely on an internet connection during installation
# while leveraging the power off eggs for later updates.

# It uses the following strategy:
# 0 ) Prepare working dir (remove it if necessary and [re]create it)
# 1 ) from a map of package names and bit masks we:
# - go fetch installers for our Python version in srcDir and copy them into the working dir
# - copy test files for packages whose bitmask says it should be tested
# - configure template_win_inst.iss.in in various ways, filling in the blanks:
    # * files to be packaged into the installer
    # * generating testing and installation code
    # * etc...
# 2 ) Write down the configured template_win_inst to the working directory.
#
# BTW think of this module as a root-level class. It behaves mostly like a class excepted I didn't
# encapsulate it inside a class.

import argparse
from collections import OrderedDict
import glob
from os.path import exists, join as pj, basename, abspath, split, dirname
import os
import platform
import shutil
import string
import sys
import types

from setuptools.package_index import PackageIndex
from openalea.deploy.util import get_base_dir, get_repo_list, OPENALEA_PI


err = sys.stderr.write
out = sys.stdout.write
__path__ = dirname(abspath(__file__))

# -- Some Flags : DONT CHANGE THESE IF YOU DON'T KNOW WHAT YOU'RE DOING --
NOFLAG = 0
# Is it an egg, an exe, a zip to install with easy_install or an msi?
EGG     = 2**0
EXE     = 2**1
ZIPDIST = 2**2
MSI     = 2**3
# Does the egg depend on python version?
PY_DEP  = 2**4
# Is it for runtime or development, or both ?
RUNTIME = 2**5
DEVELOP = 2**6
# Should we test for it ?
TEST_ME = 2**7
# If it can't be installed
NOT_INSTALLABLE = 2**8 #if tested and not installable, then fatal!
# Is it architecture dependent (i386 vs x86_64)?
ARCH    = 2**9
# A flag that marks the thing as an innosetup component
COMPONENT = 2**10


# -- Installer and dependency packages description are declared here but are actually defined in the
# -- conf file.
# APPNAME=None
# APPVERSION=None
# thirdPartyPackages = None

class StrictTemplate(string.Template):
    idpattern = r"[_A-Z0-9]*"

# function to test bitmasks
def bt(val, bit):
    return bit==(val&bit)


installerExtensions = { 0:"",
                        EGG:".egg",
                        EXE:".exe",
                        ZIPDIST:".zip",
                        MSI:".msi",
                        }

###########################################################################################
# The following strings will be used as templates to create PascalScript in the installer #
# that test and installs the modules that we wan to install and/or test                   #
###########################################################################################
python_package_test_template = """
(*** Function to detect $PACKAGE ***)
function Detect$PACKAGE(): Boolean;
var
  ResultCode: Integer;
begin
  ExtractTemporaryFile('$PACKAGE_TEST');
  Result:=(Exec(GetPythonDirectory()+'python.exe', MyTempDir()+'$PACKAGE_TEST', '',
          SW_HIDE, ewWaitUntilTerminated, ResultCode)) and (ResultCode=0);
end;

"""

python_package_install_template_exe = """
(*** Function to install $PACKAGE ***)
function Install$PACKAGE(): Boolean;
begin
  ExtractTemporaryFile('$PACKAGE_INSTALLER');
  Result := InstallExe(MyTempDir()+'$PACKAGE_INSTALLER');
end;

"""

python_package_install_template_egg = """
(*** Function to install $PACKAGE ***)
function Install$PACKAGE(): Boolean;
begin
       ExtractTemporaryFile('$PACKAGE_INSTALLER');
       Result := InstallEgg( MyTempDir()+'$PACKAGE_INSTALLER', '-N');
end;

"""

python_package_install_template_zipdist = """
(*** Function to install $PACKAGE ***)
function Install$PACKAGE(): Boolean;
begin
       ExtractTemporaryFile('$PACKAGE_INSTALLER');
       Result := InstallZipdist( MyTempDir()+'$PACKAGE_INSTALLER');
end;

"""

python_package_install_template_msi = """
(*** Function to install $PACKAGE ***)
function Install$PACKAGE(): Boolean;
begin
       ExtractTemporaryFile('$PACKAGE_INSTALLER');
       Result := InstallMsi( MyTempDir()+'$PACKAGE_INSTALLER');
end;

"""

#"ti" stands for "test and install"
python_package_ti_template_exe    = python_package_test_template+python_package_install_template_exe
python_package_ti_template_egg    = python_package_test_template+python_package_install_template_egg
python_package_ti_template_zipdist= python_package_test_template+python_package_install_template_zipdist
python_package_ti_template_msi    = python_package_test_template+python_package_install_template_msi




def prepare_working_dir(instDir):    
    if exists(instDir):
        print instDir, "will be deleted"
        shutil.rmtree(instDir, ignore_errors=False)
    print instDir, "will be created"
    os.makedirs(instDir)

import traceback
def find_installer_files(outDir, srcDir, pyMaj, pyMin, arch, dependencies):

    arch = "win32" if arch == "x86" else "win64"
    
    def globInstaller(pk, mask):
        
        identifier = pk+"*"
        if bt(mask, PY_DEP):
            identifier+=pyMaj+"."+pyMin+"*"
        if bt(mask, MSI): identifier+=".msi"
        elif bt(mask, ZIPDIST): identifier+=".zip"
        elif bt(mask, EGG): identifier+=".egg"
        elif bt(mask, EXE): identifier+=".exe"
        else:
            raise Exception("Unknown installer type: " + pk +":"+str(mask))
            
        try:
            if bt(mask, ARCH): #WE CARE ABOUT THE ARCH
                if arch=="win32": #either it has 32 or nothing but not 64
                    files = [f for f in glob.iglob(pj(srcDir, identifier))  if arch in f or ("win32" not in f and "64" not in f)]
                else:
                    files = [f for f in glob.iglob(pj(srcDir, identifier))  if arch in f]
                return sorted(files, lambda x, y: cmp(len(x), len(y)))[0]
            else:
                return glob.glob(pj(srcDir, identifier))[0]
        except:
            #traceback.print_exc()
            err("\tNo installer found for "+pk+" with for "+srcDir+" "+identifier+"\n")
            return None
                        
    print "Gathering paths to binaries..."
    ok = True
    for pk, info in dependencies.iteritems():
        mask = info[0]
        if bt(mask, NOT_INSTALLABLE):
            continue
        ef = globInstaller(pk, mask)
        if ef is None:
            #err( "\tNo installer found for %s.\n"%pk )
            ok = False
            continue
        info[1] = ef
        out("\tWill install %s\n"%ef)        
    return ok


        
def get_project_eggs(arch, globs, outDir, srcDir):
    # real egg names have the project prefix eg, "OpenAlea", "VPlants".
    # then comes the python version "py2.6"
    # and optionnaly the OS "linux-i686", "win32".
    # However, we don't explicitly know which egg has the os in the name
    # so simply encoding the os in the glob is a bad idea. What we do is:
    # [glob for project_prefix*python_version.egg] + [glob for project_prefix*python_version*os.egg]
    # The egg globs at this stage have the project_prefix*python_version*.egg form.   
    arch = "win32" if arch == "x86" else "64"         
    
    files = []
    for g in globs:
        files += glob.glob(g)

    # -- then we filter these files --
    files = [f for f in files if (arch in f) or (not "win" in f)]
        
    print "Gathering path to eggs..."
    egg_paths = []
    localFiles = map(basename, files)
    for f, filename in zip(files, localFiles):
        egg_paths.append(f)
        out("\tWill install %s\n"%f)
    return egg_paths


# -- ATTENTION PLEASE -- must be run after "copy eggs" and "get_installer_files"<
# -- Override me to generate innosetup [setup] section.       
def generate_inno_installer_setup_group(setup):    
    final = ""
    for k, v in setup.iteritems():
        basev = basename(v)
        if "file" in k.lower():
            src = abspath(v)
            out("\t"+src+"\n")
        final += k + "=" + src + "\n"
    return final
    

# -- ATTENTION PLEASE -- must be run after "copy eggs" and "get_installer_files"<
def generate_inno_installer_files_group(dependencies, egg_pths):
    final = ""
    #installers and test files
    for pk, info in dependencies.iteritems():
        mask = info[0]
        if info[2]: # if we have test files associated
            final += "Source: \""+info[2]+"\"; DestDir: {tmp}; Flags: dontcopy\n"
        if info[1]: #if we have an installer to package
            final += "Source: \""+info[1]+"\"; DestDir: {tmp}; Flags: dontcopy\n"                
    #eggs 
    for f in egg_pths:
        final += "Source: \""+f+"\"; DestDir: {tmp}; Flags: dontcopy\n"        
    return final
    
# -- ATTENTION PLEASE -- must be run after "copy eggs" and "get_installer_files"    
def generate_pascal_test_install_code(dependencies):
    final = ""
    testVariables = {"python":"PyInstalled"} #there's always this variable

    for pk, info in dependencies.iteritems():
        mask = info[0]
        testVariables[pk] = pk+"Installed" #always defined
        if bt(mask,TEST_ME):
            if bt(mask, NOT_INSTALLABLE):
                template = StrictTemplate(python_package_test_template)
                final += template.substitute(PACKAGE=pk,
                                             PACKAGE_TEST=info[2])
            else:            
                #"ti" stands for "test and install"
                if bt(mask, MSI): template = python_package_ti_template_msi
                elif bt(mask, ZIPDIST): template = python_package_ti_template_zipdist
                elif bt(mask, EGG): template = python_package_ti_template_egg
                elif bt(mask, EXE): template = python_package_ti_template_exe
                else: raise Exception("Unknown installer type: " + pk +":"+str(mask))
                template = StrictTemplate(template)
                final+=template.substitute(PACKAGE=pk,
                                           PACKAGE_TEST=basename(info[2]),
                                           PACKAGE_INSTALLER=basename(info[1]) )
        else:
            if bt(mask, NOT_INSTALLABLE):
                continue
            else:
                if bt(mask, MSI): template = python_package_install_template_msi
                elif bt(mask, ZIPDIST): template = python_package_install_template_zipdist
                elif bt(mask, EGG): template = python_package_install_template_egg
                elif bt(mask, EXE): template = python_package_install_template_exe
                else: raise Exception("Unknown installer type: " + pk +":"+str(mask))
                template = StrictTemplate(template)
                final+=template.substitute(PACKAGE=pk,
                                           PACKAGE_INSTALLER=basename(info[1]) )
                                       
    return final, testVariables


    
def generate_pascal_detect_env_body(dependencies, testVars, appname):
    testReportingPascalTemplate = StrictTemplate(
"""
  if not $VAR then
    caption := caption+#13+'$PACKAGE is not installed, $APPNAME will install it for you.'
  else
    caption := caption+#13+'$PACKAGE is already installed.';
""")

    testFatalReportingPascalTemplate = StrictTemplate(
"""
  if not $VAR then
    begin
        caption := caption+#13+'$PACKAGE is not installed, please install it first. Setup will abort';
        MsgBox('$PACKAGE is missing, installation will abort soon.', mbCriticalError, MB_OK);
        ABORTINSTALL := True;
    end
  else
    caption := caption+#13+'$PACKAGE is already installed.';
""")
    testing = ""
    reporting = ""
    for pk, info in dependencies.iteritems():
        mask = info[0]  
        if bt(mask, TEST_ME) or pk == "python":                 
            var = testVars[pk]
            testing += "  "+ var + " := PyInstalled and Detect"+pk+"();\n"
                    
            if bt(mask, NOT_INSTALLABLE): #if tested and not installable, then fatal!
                reporting += testFatalReportingPascalTemplate.substitute(PACKAGE=pk,
                                                                         VAR=var,
                                                                         APPNAME=appname)
            else:       
                reporting += testReportingPascalTemplate.substitute(PACKAGE=pk,
                                                                    VAR=var,
                                                                    APPNAME=appname)
    return testing, reporting
            
 
def generate_pascal_deploy_body(dependencies, testVars, step):
    installationPascalTemplate = StrictTemplate(
"""
  if res and not $VAR then
    begin
      WizardForm.StatusLabel.Caption:='Installing $PACKAGE, please wait...'; 
      WizardForm.ProgressGauge.Position := WizardForm.ProgressGauge.Position + $STEP;
      WizardForm.Update();
      res := Install$PACKAGE();
    end;
""")    
    installation = ""
    
    for pk, info in dependencies.iteritems():
        mask = info[0]
        if bt(mask, NOT_INSTALLABLE):
            continue
        var = testVars[pk]
        installation += installationPascalTemplate.substitute(PACKAGE=pk,
                                                              VAR=var,
                                                              STEP=step)
    return installation
          
# -- Override me to generate postInstall pascal code.          
def generate_pascal_post_install_code(options):
    return ""

# -- Override me to generate application installation pascal code.         
def generate_pascal_install_code(options):        
    return  """
var i, incr:Integer;
var s:String;
begin
    Result:=False;
    incr := (100 - WizardForm.ProgressGauge.Position)/high(Eggs);
    for i:=0 to high(Eggs) do begin
        s := Eggs[i];
        WizardForm.StatusLabel.Caption:='Uncompressing '+s;
        WizardForm.Update();
        ExtractTemporaryFile(s);
        Result := InstallEgg( MyTempDir()+s, '-N');
        WizardForm.ProgressGauge.Position := WizardForm.ProgressGauge.Position + incr;
    end;
    Result := True;
end;"""
    
def configure_inno_setup(appname, appversion, dependencies, args, funcs, egg_pths):
    print "Configuring inno script...",
    f = open( pj(__path__,"template_win_inst.iss.in") )
    s = f.read()
    f.close()

    template = StrictTemplate(s)
    #eggs = options["eggs"]
    eggnum = len(egg_pths)

    eggArrayInit = ""
    for i, e in enumerate(egg_pths):
        eggArrayInit+="Eggs[%i] := '%s';\n"%(i, e)      
            
    step = int(100./(eggnum+len(dependencies)))    
    detect, testVars = funcs["generate_pascal_test_install_code"](dependencies)
    testingBody, reportingBody = funcs["generate_pascal_detect_env_body"](dependencies, testVars, appname)
    installationBody = funcs["generate_pascal_deploy_body"](dependencies, testVars, step)

    modeStr = "" if args.runtime else "dev"
    s = template.substitute(APPNAME=appname,
                            APPVERSION=appversion,
                            INSTTYPE=modeStr.upper(),
                            SETUP_CONF=funcs["generate_inno_installer_setup_group"](args.setup),
                            #configure Python Major and Minor
                            PYTHONMAJOR=args.pyMaj,
                            PYTHONMINOR=args.pyMin,
                            #the pascal booleans that store if this or that package is installed or not.
                            TEST_VARIABLES=reduce(lambda x,y: x+", "+y, testVars.itervalues(), "dummy"),
                            #the files that will be packed by the installer.
                            INSTALLER_FILES=funcs["generate_inno_installer_files_group"](dependencies, egg_pths),
                            #configure number of eggs
                            EGGMAXID=str(eggnum-1),
                            #configure the initialisation of egg array
                            EGGINIT=eggArrayInit,
                            #configure other pascal code
                            STEP=step,
                            #configure the functions that detect and install packages
                            INSTALL_AND_DETECTION_CODE=detect,
                            #configure the body of DetectEnv that tests
                            TEST_VAR_RESULTS=testingBody,
                            #configure the body of DetectEnv that reports
                            REPORT_VAR_RESULTS=reportingBody,
                            INSTALL_APP_BODY=funcs["generate_pascal_install_code"](None),
                            #configure the body of Deploy that installs the dependencies
                            DEPLOY_BODY=installationBody,
                            #Code to run on post install
                            POSTINSTALLCODE=funcs["generate_pascal_post_install_code"](egg_pths),                            
                            )

    
    f = open( pj(args.outDir, appname+"_installer_"+modeStr+".iss"), "w" )
    f.write(s)
    f.close()
    print "ok"

def make_stitcher( eggDir, pyMaj, pyMin):
    """Creates a function that inserts the pyX.X string
    in the egg glob string if it's not there already."""
    pyfix = "py"+pyMaj+"."+pyMin+"*"
    def __stitch_egg_names(eggName):
        if pyfix in eggName:
            return pj(eggDir, eggName)
        part = eggName.partition(".egg")
        return pj(eggDir, part[0] + pyfix + part[1])
    return __stitch_egg_names

def processInstaller(mask, runtimeMode):
    if (runtimeMode==True and bt(mask, RUNTIME)) or (runtimeMode==False and bt(mask, DEVELOP)):
        return True
    return False                                   
   

   
######################
# MAIN AND RELATIVE  #
######################
   
def read_conf_file(confFile, as_globals=False):
        print "Reading conf file:", confFile, "...",
        if as_globals:
            ret = globals()
            execfile(confFile, globals())            
        else:
            d = {} 
            ret = d
            execfile(confFile, globals(), d)
        print "done"
        return ret
   
def epilog():
    msg="""
python makeWinInstaller conf=vplants.conf pyMaj=2 pyMin=6 srcDir=%HOMEPATH%\\Downloads\\ eggGlobs="VPlants*.egg|Openalea*.egg" runtime=True arch=x86


python makeWinInstaller conf=openalea.conf pyMaj=2 pyMin=7 srcDir=%HOMEPATH%\\Downloads\\ eggGlobs="Openalea*.egg" runtime=False arch=x86_64

python makeWinInstaller.py conf=alinea_conf.py srcDir=%DISTBASE%\\..\\thirdPartyPackages eggDir=%DISTBASE%\\al26 arch=x86 
    setup="{'LicenseFile':r'%DISTBASE%\\..\\..\\vplants\\src\\release_0_9\\vplants_meta\\license.txt'}"

You can have multiple globs, just use: eggGlobs="Openalea*.egg|Vplants*.egg".
The glob will be mangled with to incorporate python version information so you
should NOT write "Openalea*py2.6.egg" because it will be done automatically.
"""
    return msg

def _parse_dict_string(d_str):
    return eval(d_str) if not isinstance(d_str, dict) else d_str    
    
def parse_arguments():
    parser = argparse.ArgumentParser(description="Create InnoSetup installers for Windows, for Openalea, VPlants and Alinea",
                                     epilog = epilog(),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,)
    
    default = str(sys.version_info.major)
    parser.add_argument("--pyMaj", "-P", default=default, help="Major python version (default = %s)."%default, type=str)
    default = str(sys.version_info.minor)
    parser.add_argument("--pyMin", "-p", default=default, help="Minor python version (default = %s)."%default, type=str)
    default = pj(abspath(os.curdir), "eggs", "thirdparty")
    parser.add_argument("--srcDir", "-s", default=default, help="Directory to look for third party installers or eggs (default = %s)."%default, type=abspath)
    default = pj(abspath(os.curdir), "output", "PROJECT")
    parser.add_argument("--outDir", "-o", default=default, help="Directory to put output (default=%s)."%default, type=abspath)
    
    parser.add_argument("--eggGlobs", "-b", default=None, help="Pattern to match the PROJECT egg names (is not defined in CONFFILE). Use '|' to specify many patterns.")
    
    default = pj(abspath(os.curdir), "eggs", "PROJECT")
    parser.add_argument("--eggDir", "-e", default=default, help="Directory where we will look for the PROJECT eggs (default = %s)"%default, type=abspath)
    
    parser.add_argument("--devel", "-d", action="store_const", const=False, default=True, help="Build Development Toolkit or Runtime (default=runtime)", dest="runtime")
    default = platform.machine()
    parser.add_argument("--arch", "-a", default=default, help="Build installer for this arch (default=%s)"%default, choices=["x86", "x86_64"])
    parser.add_argument("--setup", "-m", default={}, help="Additinnal values to complete InnoSetup conf file. (example :%s) "%str({'LicenseFile':'c:\\pthtolicensefile'}), 
                        type=_parse_dict_string)
    
    parser.add_argument("--confFile", "-c", default=None, help="Configuration file for to build with", type=abspath)
       
    parser.add_argument("--private-packages", "-g", action="store_const", const=True, default=False, help="Use private packages from gforge.")
    parser.add_argument("--login",  default=None, help="login to connect to GForge")
    parser.add_argument("--passwd", default=None, help="password to connect to GForge")
       
    parser.add_argument("project", default="openalea", help="Which project to build installer for", choices=["openalea", "vplants", "alinea"])
    
    return parser.parse_args()


optionsThatCanBeInConf = set(["eggGlobs", "setup"])
    
def main():
    #print __path__
    #sys.exit(-1)
    args = parse_arguments()
    
    if "PROJECT" in args.outDir:
        args.outDir = args.outDir.replace("PROJECT", args.project+"_"+sys.platform+"_"+args.pyMaj+"."+args.pyMin)
    else:
        args.outDir = pj(args.outDir, args.project+"_"+sys.platform+"_"+args.pyMaj+"."+args.pyMin)
    
    prepare_working_dir(args.outDir)
    
    # -- Find the configuration file
    confFile  = args.confFile or pj(split(__file__)[0], args.project+"_conf.py")        
    confDict = read_conf_file(confFile)    
    
    #   -- funcs will contain function overrides read from confFile --
    funcs = dict( (fname, f) for fname, f in globals().iteritems() if isinstance(f, types.FunctionType) )
    funcs.update(dict( (fname, f) for fname, f in confDict.iteritems() if isinstance(f, types.FunctionType)))    
    #   -- vars will contain vars read from confFile --    
    thirdPartyPackages = confDict["thirdPartyPackages"]
    appname            = confDict["APPNAME"]
    appversion         = confDict["APPVERSION"]
    
    args.eggGlobs = args.eggGlobs or confDict["eggGlobs"]
    args.setup    = args.setup or confDict["setup"]
                            
    # -- Fix the egg globs to include python version and architecture dependency.
    args.eggGlobs = map(make_stitcher(args.eggDir, args.pyMaj, args.pyMin), args.eggGlobs.split("|"))
    print "The following egg globs will be used:", args.eggGlobs
        
    # -- Filter the dependencies to process according to the type of installer (for runtimes or devtools)
    dependencies = OrderedDict( (pk, [mask, None, None]) for pk, (mask,) in thirdPartyPackages  \
                                if processInstaller(mask, args.runtime) )

    # -- find out the installers to package for this mega installer --
    ok = find_installer_files(args.outDir, args.srcDir, args.pyMaj, args.pyMin, args.arch, 
                              dependencies)                            
                            
    if not ok:
        sys.exit(-1)
    # -- find out package testing python module names for the packages that need to be tested
    out("Gathering paths to testing scripts... \n")
    for pk, info in dependencies.iteritems():
        test    = pj(__path__, pk+"_test.py") if bt(info[0],TEST_ME) else None
        info[2] = test
        out("\tWill install %s for %s\n"%(test,pk))
                           
    # if args.private_packages:
        # rc_user, rc_pass = find_login_passwd()
        # gforge_login = args.login or rc_user
        # gforge_passwd = args.passwd or rc_pass        
        # add_private_gforge_repositories(gforge_login, gforge_passwd)
        
    # pi = PackageIndex()
    # pi.add_find_links(get_repo_list())
                

    proj_egg_pths = get_project_eggs(args.arch, args.eggGlobs, args.outDir, args.srcDir)
    configure_inno_setup(appname, appversion, dependencies, args, funcs, proj_egg_pths)
    print "Done, please check the generated file."

    
    
if __name__ == "__main__":
    main()