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
from os.path import exists, join as pj, basename
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

    
# What options do we accept (too lazy to use getopts)
goodOptions = set([ "conf",
                    "pyMaj",
                    "pyMin",
                    "srcDir",
                    "eggGlobs",
                    "runtime",
                    "arch" ])

def print_usage():
    msg="""
makeWinInstaller conf=vplants.conf pyMaj=2 pyMin=6 srcDir=%HOMEPATH%\Downloads\ eggGlobs="VPlants*.egg|Openalea*.egg" runtime=True arch=i386
makeWinInstaller conf=openalea.conf pyMaj=2 pyMin=7 srcDir=%HOMEPATH%\Downloads\ eggGlobs="Openalea*.egg" runtime=False arch=x86_64

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
easyThirdPartyNames = None
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
       Result := InstallEgg( MyTempDir()+'$PACKAGE_INSTALLER');
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
    pyMaj, pyMin = options["pyMaj"], options["pyMin"]
    instDir = pj(CWD, APPNAME+"-"+pyMaj+"."+pyMin)
    return instDir

def prepare_working_dir(options):
    instDir = get_wd(options)
    if exists(instDir):
        shutil.rmtree(instDir, ignore_errors=True)
    os.mkdir(instDir)

def copy_installer_files(options):
    srcDir  = options["srcDir"]
    pyMaj  = options["pyMaj"]
    pyMin  = options["pyMin"]

    def globInstaller(srcDir, pk, mask):
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
                return files[0]
            else:
                return glob.glob(pj(srcDir, identifier))[0]
        except:
            return "No installer found for "+pk+" with glob "+pj(srcDir, identifier)

            
    print "Copying binaries..."    
    for pk in dependenciesToProcess:
        mask = thirdPartyPackages[pk][0]
        if bt(mask, NOT_INSTALLABLE):
            continue
        ef = globInstaller(options, pk, mask)
        src, dst = ef, pj(get_wd(options), easyThirdPartyNames[pk])
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


# -- ATTENTION PLEASE -- must be run after "copy eggs"    
def __generate_inno_installer_files_group(options):
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

    
def __generate_pascal_test_install_code(options):
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


    
def __generate_pascal_detect_env_body(testVars):
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
            
 
def __generate_pascal_deploy_body(testVars, step):
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
    detect, testVars = __generate_pascal_test_install_code(options)
    testingBody, reportingBody =__generate_pascal_detect_env_body(testVars)
    installationBody = __generate_pascal_deploy_body(testVars, step)
    
    modeStr = "" if eval(options["runtime"]) else "dev"
    s = template.substitute(APPNAME=APPNAME,
                            APPVERSION=APPVERSION,
                            INSTTYPE=modeStr.upper(),
                            #configure Python Major and Minor
                            PYTHONMAJOR=options["pyMaj"],
                            PYTHONMINOR=options["pyMin"],
                            #the pascal booleans that store if this or that package is installed or not.
                            TEST_VARIABLES=reduce(lambda x,y: x+", "+y, testVars.itervalues(), "dummy"),
                            #the files that will be packed by the installer.
                            INSTALLER_FILES=__generate_inno_installer_files_group(options),
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
    pyfix = "py"+options["pyMaj"]+"."+options["pyMin"]+"*"
    def __stitch_egg_names(eggName):
        if pyfix in eggName:
            return eggName
        part = eggName.partition(".egg")
        return part[0] + pyfix + part[1]
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
        
        
if __name__ == "__main__":
    options = dict(map(lambda x: x.split('='), sys.argv[1:]))

    # -- Quick options parsing, either all options are satisfied or the process halts.
    if not set(options.iterkeys()) == goodOptions:
        print_usage()
        sys.exit(-1)

    # -- Fix the egg globs to include python version and architecture dependency.
    options["eggGlobs"] = map(make_stitcher(options), options["eggGlobs"].split("|"))
    print "The following egg globs will be used:", options["eggGlobs"]
    
    # -- Read the configuration file given on command line
    read_conf_file(options)
    
    # -- Filter the dependencies to process according to the type of installer (for runtimes or devtools)
    installerMode = eval(options["runtime"])
    dependenciesToProcess = [pk for pk, (mask, order) in sorted(thirdPartyPackages.iteritems(), key=lambda x:x[1][1]) 
                            if processInstaller(mask, installerMode)]

    # -- create easy names for the packages. The generated inno script will use the short names. This might aswell disappear one day
    easyThirdPartyNames = dict((k, k+installerExtensions[thirdPartyPackages[k][0]&0xf]) \
                               for k in dependenciesToProcess)

    # -- find out package testing python module names for the packages that need to be tested
    thirdPartyTests = dict((k, k+"_test.py") for k in dependenciesToProcess if bt(thirdPartyPackages[k][0],TEST_ME))    
        
    prepare_working_dir(options)
    copy_installer_files(options)
    copy_eggs(options)
    configure_inno_setup(options)
    print "Done"
