# -- Installer and dependency packages description : EDIT THIS --
APPNAME="Alinea"
APPVERSION="1.0"
setup = {"LicenseFile":"LICENSE.TXT"}  

eggGlobs = "Alinea*.egg"

# package -> (installerFlags, installationOrder)
thirdPartyPackages = {   "python"  :    (NOT_INSTALLABLE|RUNTIME|DEVELOP,          0), #always tested
                         "openalea":    (NOT_INSTALLABLE|RUNTIME|DEVELOP|TEST_ME,  1),
                         "vplants" :    (NOT_INSTALLABLE|RUNTIME|DEVELOP|TEST_ME,  2),
                         ("r", (EXE|ARCH|RUNTIME|TEST_ME,)),
                         ("rpy2", (MSI|PY_DEP|ARCH|RUNTIME|TEST_ME,)),                           
                         }
                         
                         
                       
                         
