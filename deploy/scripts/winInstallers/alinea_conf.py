# -- Installer and dependency packages description : EDIT THIS --
APPNAME="Alinea"
APPVERSION="0.9"
setup = {"LicenseFile":"LICENSE.TXT"}  

eggGlobs = "Alinea*.egg"

# package -> (installerFlags, installationOrder)
thirdPartyPackages = {   "python"  :    (NOT_INSTALLABLE|RUNTIME|DEVELOP,          0), #always tested
                         "openalea":    (NOT_INSTALLABLE|RUNTIME|DEVELOP|TEST_ME,  1),
                         "vplants" :    (NOT_INSTALLABLE|RUNTIME|DEVELOP|TEST_ME,  2),
                         "r"       :    (EXE|ARCH|RUNTIME|TEST_ME,       3),
                         "rpy2"    :    (MSI|PY_DEP|ARCH|RUNTIME|TEST_ME,4),
                         }
                         
                         
                       
                         
# -- The default generate_pascal_post_install_code(opt) function returns "". --
# -- For alinea, let's make sure RPy2 has everything to work correctly. --                         
postInstallPascal = """
        RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                'PATH', str1);
        if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'Software\R-core\R', 'InstallPath', str2) then
                RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                'R_HOME', str2);
        
                
        if (Pos('%R_HOME%', str1) = 0) then
            RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                'PATH', str1+';%R_HOME%');  
    """
          
def generate_pascal_post_install_code(options):
    return postInstallPascal