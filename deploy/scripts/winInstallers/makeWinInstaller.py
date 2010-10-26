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

import sys, os
from os.path import exists, join as pj, basename, abspath
import shutil, glob, string



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
APPNAME=None
APPVERSION=None
thirdPartyPackages = None


CWD = str(os.getcwd())

class StrictTemplate(string.Template):
    idpattern = r"[_A-Z0-9]*"

###########################################
# OPTION HANDLING                         #
# (too lazy to use getopts)               #
###########################################
goodOptions = { "conf":str,
                "pyMaj":int,
                "pyMin":int,
                "srcDir":str,
                "eggGlobs":str,
                "eggDir":str,
                "runtime":bool,
                "arch":str,
                "setup":dict}
                    
optionsThatCanBeInConf = set(["eggGlobs", "setup"])
                            
optionDefaults = {"runtime":True,
                  "pyMaj":sys.version_info[0],
                  "pyMin":sys.version_info[1],
                  "setup":{}
                  }

def evalOption(val, type):
    if type==str:
        return val
    elif type==bool:
        return val=="True" or bool(val)
    elif type==int:
        return int(val)
    elif type==dict:
        return eval(val) if not isinstance(val, dict) else val
###########################################
                     




def print_usage():
    msg="""
python makeWinInstaller conf=vplants.conf pyMaj=2 pyMin=6 srcDir=%HOMEPATH%\\Downloads\\ eggGlobs="VPlants*.egg|Openalea*.egg" runtime=True arch=i386


python makeWinInstaller conf=openalea.conf pyMaj=2 pyMin=7 srcDir=%HOMEPATH%\\Downloads\\ eggGlobs="Openalea*.egg" runtime=False arch=x86_64

python makeWinInstaller.py conf=alinea_conf.py srcDir=%DISTBASE%\\..\\thirdPartyPackages eggDir=%DISTBASE%\\al26 arch=i386 
    setup="{'LicenseFile':r'%DISTBASE%\\..\\..\\vplants\\src\\release_0_9\\vplants_meta\\license.txt'}"

You can have multiple globs, just use: eggGlobs="Openalea*.egg|Vplants*.egg".
The glob will be mangled with to incorporate python version information so you
should NOT write "Openalea*py2.6.egg" because it will be done automatically.
"""
    print msg

# function to test bitmasks
def bt(val, bit):
    return bit==(val&bit)

# -- The following globals are configured in the "if __name__ == '__main__'" section. --
#Subset of package names that will be incorporated wether we're building runtime or "sdk".
dependenciesToProcess=None    
# create easy names for the packages. This might aswell disappear one day
easyThirdPartyNames = {}
# create package testing python module names for the packages that want to be tested
thirdPartyTests = None

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
python_package_ti_template_exe=python_package_test_template+python_package_install_template_exe
python_package_ti_template_egg=python_package_test_template+python_package_install_template_egg
python_package_ti_template_zipdist=python_package_test_template+python_package_install_template_zipdist
python_package_ti_template_msi=python_package_test_template+python_package_install_template_msi



def get_wd(options):
    pyMaj, pyMin = options["pyMajStr"], options["pyMinStr"]
    instDir = pj(CWD, APPNAME+"-"+pyMaj+"."+pyMin)
    return instDir

def prepare_working_dir(options):
    instDir = get_wd(options)
    if exists(instDir):
        shutil.rmtree(instDir, ignore_errors=True)
    os.mkdir(instDir)

import traceback
def copy_installer_files(options):
    srcDir  = options["srcDir"]
    pyMaj  = options["pyMajStr"]
    pyMin  = options["pyMinStr"]

    def globInstaller(pk, mask):
        arch = "win32" if options["arch"] == "i386" else "64"
        
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
            traceback.print_exc()
            print srcDir, identifier
            return "No installer found for "+pk+" with for "+srcDir+" "+identifier

            
    print "Copying binaries..."    
    for pk in dependenciesToProcess:
        mask = thirdPartyPackages[pk][0]
        if bt(mask, NOT_INSTALLABLE):
            continue
        ef = globInstaller(pk, mask)
        filename = basename(ef)
        easyThirdPartyNames[pk] = filename

        src, dst = ef, pj(get_wd(options), basename(ef)) #easyThirdPartyNames[pk])
        print "\t"+src+" => "+dst+"...",
        shutil.copyfile(src, dst)
        print "ok"
    
    print "Copying environment testing scripts..."
    for f in thirdPartyTests.itervalues():
        src, dst = f, pj(get_wd(options), f)
        print "\t"+src+" => "+dst+"...",
        shutil.copyfile(src, dst)
        print "ok"

        
def copy_eggs(options):
    # real egg names have the project prefix eg, "OpenAlea", "VPlants".
    # then comes the python version "py2.6"
    # and optionnaly the OS "linux-i686", "win32".
    # However, we don't explicitly know which egg has the os in the name
    # so simply encoding the os in the glob is a bad idea. What we do is:
    # [glob for project_prefix*python_version.egg] + [glob for project_prefix*python_version*os.egg]
    # The egg globs at this stage have the project_prefix*python_version*.egg form.   
    arch = "win32" if options["arch"] == "i386" else "64"    
    globs = options["eggGlobs"]        
    
    files = []
    for g in globs:
        files += glob.glob(g)

    # -- then we filter these files.
    files = [f for f in files if (arch in f) or (not "win" in f)]
        
    print "Copying eggs..."
    localFiles = map(basename, files)
    for f, filename in zip(files, localFiles):
        src, dst = f, pj(get_wd(options), filename)
        print "\t"+src+" => "+dst+"...",
        shutil.copyfile(src, dst)
        print "ok"
    options["eggs"] = localFiles


# -- ATTENTION PLEASE -- must be run after "copy eggs" and "copy_installer_files"<
# -- Override me to generate innosetup [setup] section.       
def generate_inno_installer_setup_group(options):    
    final = ""
    setupStuff = options.get("setup", {})
    setupStuff.update(globals().get("setup", {}))
    print "-------------------------------->", setupStuff
    for k, v in setupStuff.iteritems():
        basev = basename(v)
        if "file" in k.lower():
            src, dst = abspath(v), pj(get_wd(options), basev)
            print "\t"+src+" => "+dst+"...",
            shutil.copyfile(src,dst)
            print "ok"
        final += k + "=" + basev + "\n"
    return final
    

# -- ATTENTION PLEASE -- must be run after "copy eggs" and "copy_installer_files"<
def generate_inno_installer_files_group(options):
    final = ""
    #installers
    for pk, f in easyThirdPartyNames.iteritems():
        if bt(thirdPartyPackages[pk][0], NOT_INSTALLABLE):
            continue
        final += "Source: \""+f+"\"; DestDir: {tmp}; Flags: dontcopy\n"
        
    #eggs 
    for f in options["eggs"]:
        final += "Source: \""+f+"\"; DestDir: {tmp}; Flags: dontcopy\n"
        
    #test scripts
    for f in thirdPartyTests.itervalues():
        final += "Source: \""+f+"\"; DestDir: {tmp}; Flags: dontcopy\n"

    return final
    
# -- ATTENTION PLEASE -- must be run after "copy eggs" and "copy_installer_files"    
def generate_pascal_test_install_code(options):
    final = ""
    testVariables = {"python":"PyInstalled"} #there's always this variable

    for pk in dependenciesToProcess:
        mask = thirdPartyPackages[pk][0]
        if bt(mask,TEST_ME):
            testVariables[pk] = pk+"Installed"
            if bt(mask, NOT_INSTALLABLE):
                template = StrictTemplate(python_package_test_template)
                final += template.substitute(PACKAGE=pk,
                                             PACKAGE_TEST=thirdPartyTests[pk])
            else:            
                #"ti" stands for "test and install"
                if bt(mask, MSI): template = python_package_ti_template_msi
                elif bt(mask, ZIPDIST): template = python_package_ti_template_zipdist
                elif bt(mask, EGG): template = python_package_ti_template_egg
                elif bt(mask, EXE): template = python_package_ti_template_exe
                else: raise Exception("Unknown installer type: " + pk +":"+str(mask))
                template = StrictTemplate(template)
                final+=template.substitute(PACKAGE=pk,
                                           PACKAGE_TEST=thirdPartyTests[pk],
                                           PACKAGE_INSTALLER=easyThirdPartyNames[pk])
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
                                           PACKAGE_INSTALLER=easyThirdPartyNames[pk])
                                       
    return final, testVariables


    
def generate_pascal_detect_env_body(testVars):
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
    
    for pk in dependenciesToProcess:
        mask = thirdPartyPackages[pk][0]  
        if bt(mask, TEST_ME) or pk == "python":                 
            var = testVars[pk]
            testing += "  "+ var + " := PyInstalled and Detect"+pk+"();\n"
                    
            if bt(mask, NOT_INSTALLABLE): #if tested and not installable, then fatal!
                reporting += testFatalReportingPascalTemplate.substitute(PACKAGE=pk,
                                                                         VAR=var,
                                                                         APPNAME=APPNAME)
            else:       
                reporting += testReportingPascalTemplate.substitute(PACKAGE=pk,
                                                                    VAR=var,
                                                                    APPNAME=APPNAME)
    return testing, reporting
            
 
def generate_pascal_deploy_body(testVars, step):
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
    
    for pk in dependenciesToProcess:
        mask = thirdPartyPackages[pk][0]
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
    
def configure_inno_setup(options):
    print "Configuring inno script...",
    f = open("template_win_inst.iss.in")
    s = f.read()
    f.close()

    template = StrictTemplate(s)
    eggs = options["eggs"]
    eggnum = len(eggs)

    eggArrayInit = ""
    visualeaId = -1
    for i, e in enumerate(eggs):
        eggArrayInit+="Eggs[%i] := '%s';\n"%(i, e)
        if "Visualea" in e:
            visualeaId = str(i)            
            
    step = int(100./(eggnum+len(dependenciesToProcess)))    
    detect, testVars = generate_pascal_test_install_code(options)
    testingBody, reportingBody =generate_pascal_detect_env_body(testVars)
    installationBody = generate_pascal_deploy_body(testVars, step)
    
    modeStr = "" if options["runtime"] else "dev"
    s = template.substitute(APPNAME=APPNAME,
                            APPVERSION=APPVERSION,
                            INSTTYPE=modeStr.upper(),
                            SETUP_CONF=generate_inno_installer_setup_group(options),
                            #configure Python Major and Minor
                            PYTHONMAJOR=options["pyMajStr"],
                            PYTHONMINOR=options["pyMinStr"],
                            #the pascal booleans that store if this or that package is installed or not.
                            TEST_VARIABLES=reduce(lambda x,y: x+", "+y, testVars.itervalues(), "dummy"),
                            #the files that will be packed by the installer.
                            INSTALLER_FILES=generate_inno_installer_files_group(options),
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
                            INSTALL_APP_BODY=generate_pascal_install_code(options),
                            #configure the body of Deploy that installs the soft
                            DEPLOY_BODY=installationBody,
                            #Code to run on post install
                            POSTINSTALLCODE=generate_pascal_post_install_code(options),                            
                            )

    
    f = open( pj(get_wd(options), APPNAME+"_installer_"+modeStr+".iss"), "w" )
    f.write(s)
    f.close()
    print "ok"

def make_stitcher(options):
    """Creates a function that inserts the pyX.X string
    in the egg glob string if it's not there already."""
    pyfix = "py"+options["pyMajStr"]+"."+options["pyMinStr"]+"*"
    def __stitch_egg_names(eggName):
        if pyfix in eggName:
            return pj(options["eggDir"], eggName)
        part = eggName.partition(".egg")
        return pj(options["eggDir"], part[0] + pyfix + part[1])
    return __stitch_egg_names


def read_conf_file(options):
        confFile = options["conf"]
        print "Reading conf file:", confFile, "...",
        execfile(confFile, globals())
        print "Done"

def processInstaller(mask, runtimeMode):
    if (runtimeMode==True and bt(mask, RUNTIME)) or (runtimeMode==False and bt(mask, DEVELOP)):
        return True
    return False                                   
        
def printMissingArgs(input):
    goodSet = set(goodOptions.iterkeys())
    missing = goodSet-set(options.iterkeys())
    for i in missing:
        print "\t", i         
    return missing













    
        
if __name__ == "__main__":
    options = dict(map(lambda x: x.split('='), sys.argv[1:]))

    # -- Read the configuration file given on command line
    read_conf_file(options)
    goodSet = set(goodOptions.iterkeys())
    
    # -- Quick options parsing, first check if all required options are given.
    if not set(options.iterkeys()) == goodSet:
    
        # -- some options can be given in the conf file, and if they are, we find them in the global dict
        for opt in optionsThatCanBeInConf:
            print "Looking for value for the following arguments in conf file:"
            printMissingArgs(set(options.iterkeys()))               
            if opt not in options and opt in globals():
                options[opt] = globals()[opt]
            
        # -- some options can have default values
        curOpts = set(options.iterkeys())
        if not curOpts == goodSet:
            print "Looking for defaults for the following arguments:"
            printMissingArgs(curOpts)        
            for opt, val in optionDefaults.iteritems():
                if opt not in options:
                    options[opt] = val
        
        # -- are we dead -- ?
        curOpts = set(options.iterkeys())
        if not set(options.iterkeys()) == goodSet:
            print_usage()
            print "You didn't supply the following arguments:"
            printMissingArgs(curOpts)
            sys.exit(-1)

            
    options = dict((k, evalOption(v, goodOptions[k])) for k, v in options.iteritems())
    # pyMaj and pyMin are also handy as string:
    options["pyMajStr"] = str(options["pyMaj"])
    options["pyMinStr"] = str(options["pyMin"])
    
    # -- Fix the egg globs to include python version and architecture dependency.
    options["eggGlobs"] = map(make_stitcher(options), options["eggGlobs"].split("|"))
    print "The following egg globs will be used:", options["eggGlobs"]
    

    
    # -- Filter the dependencies to process according to the type of installer (for runtimes or devtools)
    installerMode = options["runtime"]
    dependenciesToProcess = [pk for pk, (mask, order) in sorted(thirdPartyPackages.iteritems(), key=lambda x:x[1][1]) 
                            if processInstaller(mask, installerMode)]

    # -- create easy names for the packages. The generated inno script will use the short names. This might aswell disappear one day
    # -- NO! This is now done in copy_installer_files

    # -- find out package testing python module names for the packages that need to be tested
    thirdPartyTests = dict((k, k+"_test.py") for k in dependenciesToProcess if bt(thirdPartyPackages[k][0],TEST_ME))    
        
    prepare_working_dir(options)
    copy_installer_files(options)
    copy_eggs(options)
    configure_inno_setup(options)
    print "Done, please check the generated file."
