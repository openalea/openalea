# -- Installer and dependency packages description : EDIT THIS --
APPNAME="OpenAlea"
APPVERSION="0.9"
setup = {"LicenseFile":"LICENSE.TXT", "WizardSmallImageFile":"oalogo.bmp"}

eggGlobs = "OpenAlea*.egg"

# package -> (installerFlags, installationOrder)
# NOTE: Symbols here are "injected" by master makeWinInstaller.py script.
# TODO : Use ordered dict
thirdPartyPackages = {   "python":      (MSI|RUNTIME|DEVELOP, 0),
                         "pywin32":     (EXE|PY_DEP|ARCH|RUNTIME|DEVELOP|TEST_ME, 1),
                         "setuptools":  (EXE|PY_DEP|ARCH|RUNTIME|DEVELOP|TEST_ME, 2),
#                         "PyQt":       (EXE|PY_DEP|ARCH|RUNTIME|DEVELOP|TEST_ME, 3), #if using standard installer
                         "mingw_rt":    (EGG|ARCH|RUNTIME, 3),
                         "qt4":         (EGG|PY_DEP|ARCH|RUNTIME|TEST_ME, 4),
                         "numpy":       (EGG|PY_DEP|ARCH|RUNTIME|TEST_ME, 5),
                         "scipy":       (EGG|PY_DEP|ARCH|RUNTIME|TEST_ME, 6),
                         "matplotlib":  (EGG|PY_DEP|ARCH|RUNTIME|TEST_ME, 7),                         
                         "pil":         (EGG|PY_DEP|RUNTIME|TEST_ME, 8),
                         "pylsm":       (EGG|PY_DEP|RUNTIME, 8),
                         #"pylibtiff":   (EGG|PY_DEP|ARCH|RUNTIME|TEST_ME, 8),
                         }
                         


                         
def generate_pascal_install_code(options):        
    return  """
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
                         
postInstallPascalTemplate = StrictTemplate("""
    Exec(GetPythonDirectory()+'python.exe', '-c "import sys;sys.path.append(\\"'+ GetPythonDirectory()+'Lib\\site-packages\\'+Eggs[$EGGID]+'\\");import $EGGNAME' + '_postinstall as pi;pi.install()', '',
          SW_HIDE, ewWaitUntilTerminated, ResultCode);""")
          
def generate_pascal_post_install_code(options):
    eggs = options["eggs"]
    s=""
    names = ["visualea", "deploygui"]

    for i, e in enumerate(eggs):
        for p in names:
            if p in e.lower():
                s += postInstallPascalTemplate.substitute(EGGID=str(i), EGGNAME=p)
            
    return s