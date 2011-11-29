# -- Installer and dependency packages description : EDIT THIS --
APPNAME="VPlants"
APPVERSION="0.9"
setup = {"LicenseFile":"LICENSE.TXT", "WizardSmallImageFile":"vplogo.bmp"}  

eggGlobs = "*\\dist\\VPlants*.egg|*\\dist\\OpenAlea*.egg"

# package -> (installerFlags, installationOrder)
thirdPartyPackages = [   ("python", (NOT_INSTALLABLE|RUNTIME|DEVELOP,)), #always tested
                         ("openalea", (NOT_INSTALLABLE|RUNTIME|DEVELOP|TEST_ME,)),
                         ("scons", (EGG|DEVELOP|TEST_ME,)),
                         ("bisonflex", (EGG|DEVELOP|TEST_ME,)),
                         ("boost", (EGG|PY_DEP|ARCH|RUNTIME|DEVELOP|TEST_ME,)),
                         ("qhull", (EGG|ARCH|DEVELOP|TEST_ME,)),
                         ("gnuplot", (EGG|ARCH|RUNTIME|DEVELOP|TEST_ME,)),
                         ("pyopengl", (ZIPDIST|ARCH|RUNTIME|DEVELOP|TEST_ME,)),
                         ("pyqglviewer", (EGG|ARCH|PY_DEP|RUNTIME|DEVELOP|TEST_ME,)),
                         ("qt4_dev", (EGG|ARCH|DEVELOP|TEST_ME,)),
                         ("mingw", (EGG|ARCH|DEVELOP,)),
                         ("r", (EXE|ARCH|RUNTIME|TEST_ME,)),
                         ("rpy2", (MSI|PY_DEP|ARCH|RUNTIME|TEST_ME,)),                         
                         ]                         
                         
manuallyInstalled = ["VPlants"]

 
                         
def generate_pascal_install_code(options):        
    s = """
var i, incr:Integer;
var s:String;
begin
    Result:=False;
    incr := (100 - WizardForm.ProgressGauge.Position)/high(Eggs)/2;
    for i:=0 to high(Eggs) do begin
        s := Eggs[i];
        WizardForm.StatusLabel.Caption:='Uncompressing '+s;
        WizardForm.Update();
        ExtractTemporaryFile(s);
        WizardForm.ProgressGauge.Position := WizardForm.ProgressGauge.Position + incr;
    end;
    """
    manInstTemplate = StrictTemplate("""
    WizardForm.StatusLabel.Caption:='Installing $PACKAGE';
    WizardForm.Update();
    Result := InstallEgg('$PACKAGE', '-H None -i ' + MyTempDir() + ' -f ' + MyTempDir()); 
    """)       
    
    for pk in manuallyInstalled:
        s += manInstTemplate.substitute(PACKAGE=pk)
        
    s += """               
     WizardForm.ProgressGauge.Position := 100;
    end;
    """ 

    return s
    
    
# -- The default generate_pascal_post_install_code(opt) function returns "". --
# -- For alinea, let's make sure RPy2 has everything to work correctly. --                         
def generate_pascal_post_install_code(egg_pths):
    s=""
    s += """
        RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                'PATH', str1);
        if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'Software\R-core\R', 'InstallPath', str2) then
                RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                'R_HOME', str2);
                        
        if (Pos('%R_HOME%', str1) = 0) then
            RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                'PATH', str1+';%R_HOME%');  
    """
          
    egg_post_inst = StrictTemplate("""
    Exec(GetPythonDirectory()+'python.exe', '-c "import sys;sys.path.append(\\"'+ GetPythonDirectory()+'Lib\\site-packages\\'+Eggs[$EGGID]+'\\");import $EGGNAME' + '_postinstall as pi;pi.install()', '',
     SW_HIDE, ewWaitUntilTerminated, ResultCode);""")
    
    names = ["lpygui"]

    for i, e in enumerate(egg_pths):
        e = basename(e)
        for p in names:
            if p in e.lower():
                s += egg_post_inst.substitute(EGGID=str(i), EGGNAME=p)          
    return postInstallPascal    