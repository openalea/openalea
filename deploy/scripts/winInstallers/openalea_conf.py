# -- Installer and dependency packages description : EDIT THIS --
__path__ = dirname(abspath(__file__))

APPNAME="OpenAlea"
APPVERSION="1.0"
setup = {"LicenseFile": pj(__path__,"LICENSE.TXT"), "WizardSmallImageFile":pj(__path__,"oalogo.bmp") } 

eggGlobs = "*\\dist\\OpenAlea*.egg"

# package -> (installerFlags, installationOrder)
# NOTE: Symbols here are "injected" by master makeWinInstaller.py script.
# TODO : Use ordered dict
thirdPartyPackages = [  ("python", (MSI|RUNTIME|DEVELOP,)),
                        ("pywin32", (EXE|PY_DEP|ARCH|RUNTIME|DEVELOP|TEST_ME,)),
                        ("setuptools", (EXE|PY_DEP|ARCH|RUNTIME|DEVELOP|TEST_ME,)),
                        #("PyQt", (EXE|PY_DEP|ARCH|RUNTIME|DEVELOP|TEST_ME,)), #if using standard installer
                        ("mingw_rt", (EGG|ARCH|RUNTIME|DEVELOP,)),
                        ("qt4", (EGG|PY_DEP|ARCH|RUNTIME|TEST_ME,)),
                        ("numpy", (EXE|PY_DEP|ARCH|RUNTIME|TEST_ME,)),
                        ("scipy", (EXE|PY_DEP|ARCH|RUNTIME|TEST_ME,)),
                        ("matplotlib", (EXE|PY_DEP|ARCH|RUNTIME|TEST_ME,)),                         
                        ("pil", (EXE|PY_DEP|RUNTIME|TEST_ME,)),
                        ("pylsm", (TARDIST|RUNTIME|TEST_ME,)),
                        ("soappy", (TARDIST|RUNTIME,)),
                        ("nose", (TARDIST|DEVELOP,)),
                        #("pylibtiff", (EGG|PY_DEP|ARCH|RUNTIME|TEST_ME,)),
                         ]
                         


                         
def generate_pascal_install_code(options):        
    return  """
var i, incr:Integer;
var s:String;
begin
    Result:=False;
    incr := (100 - WizardForm.ProgressGauge.Position)/high(Eggs)/2;
    for i:=0 to high(Eggs) do begin
        s := ExtractFileName(Eggs[i]);
        WizardForm.StatusLabel.Caption:='Uncompressing '+s;
        WizardForm.Update();
        try
            ExtractTemporaryFile(s);
            InstallEgg( MyTempDir()+s, '-N');
        except
            Exit;
        end;
        WizardForm.ProgressGauge.Position := WizardForm.ProgressGauge.Position + incr;
    end;

    WizardForm.StatusLabel.Caption:='Installing OpenAlea ';
    WizardForm.ProgressGauge.Position := 85;
    WizardForm.Update();    
    InstallEgg( 'OpenAlea.Deploy', '-H None -i ' + MyTempDir() + ' -f ' + MyTempDir());
        
    WizardForm.ProgressGauge.Position := 90;
    WizardForm.Update();        
    InstallEgg( 'OpenAlea', '-H None -i ' + MyTempDir() + ' -f ' + MyTempDir());
    Result := True;

    WizardForm.ProgressGauge.Position := 100;
    WizardForm.Update();                   
end;"""

        
# -- The default generate_pascal_post_install_code(opt) function returns "". --
# -- Let's do something smarter for openalea, to add it to start menu. --                                  
def generate_pascal_post_install_code(egg_pths):
    postInstallPascalTemplate = StrictTemplate("""
    Exec(GetPythonDirectory()+'python.exe', '-c "import sys;sys.path.append(\\"'+ GetPythonDirectory()+'Lib\\site-packages\\'+Eggs[$EGGID]+'\\");import $EGGNAME' + '_postinstall as pi;pi.install()', '',
     SW_HIDE, ewWaitUntilTerminated, ResultCode);""")
    s=""
    names = ["visualea", "deploygui"]

    for i, e in enumerate(egg_pths):
        e = basename(e)
        for p in names:
            if p in e.lower():
                s += postInstallPascalTemplate.substitute(EGGID=str(i), EGGNAME=p)
            
    return s