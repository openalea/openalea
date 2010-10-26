# -- Installer and dependency packages description : EDIT THIS --
APPNAME="VPlants"
APPVERSION="0.9"
setup = {"LicenseFile":"LICENSE.TXT", "WizardSmallImageFile":"vplogo.bmp"}  

eggGlobs = "VPlants*.egg|OpenAlea*.egg"

# package -> (installerFlags, installationOrder)
thirdPartyPackages = {   "python":      (NOT_INSTALLABLE|RUNTIME|DEVELOP, 0), #always tested
                         "openalea":    (NOT_INSTALLABLE|RUNTIME|DEVELOP|TEST_ME, 1),
                         "scons":       (EGG|DEVELOP|TEST_ME, 2),
                         "bisonflex":   (EGG|DEVELOP|TEST_ME, 3),
                         "boost":       (EGG|PY_DEP|ARCH|RUNTIME|DEVELOP|TEST_ME, 4),
                         "qhull":       (EGG|ARCH|DEVELOP|TEST_ME, 5),
                         "gnuplot":     (EGG|ARCH|RUNTIME|DEVELOP|TEST_ME, 6),
                         "pyopengl":    (ZIPDIST|ARCH|RUNTIME|DEVELOP|TEST_ME, 7),
                         "pyqglviewer": (EGG|ARCH|PY_DEP|RUNTIME|DEVELOP|TEST_ME, 8),
                         "qt4_dev":     (EGG|ARCH|DEVELOP|TEST_ME, 9),
                         "mingw":       (EGG|ARCH|DEVELOP, 10)
                         }                         
                         
manuallyInstalled = ["VPlants"]

manInstTemplate = StrictTemplate("""
    WizardForm.StatusLabel.Caption:='Installing $PACKAGE';
    WizardForm.Update();
    Result := InstallEgg('$PACKAGE', '-H None -i ' + MyTempDir() + ' -f ' + MyTempDir()); 
""")    
                         
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
    
    for pk in manuallyInstalled:
        s += manInstTemplate.substitute(PACKAGE=pk)
        
    s += """               
     WizardForm.ProgressGauge.Position := 100;
    end;
    """ 

    return s