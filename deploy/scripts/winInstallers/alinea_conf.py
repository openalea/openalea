# -- Installer and dependency packages description : EDIT THIS --
APPNAME="Alinea"
APPVERSION="1.0"
setup = {"LicenseFile":pj(__path__,"LICENSE.TXT")}  

eggGlobs = "*\\dist\\Alinea*.egg"

# package -> (installerFlags, installationOrder)
thirdPartyPackages = [   ("python"  ,    (NOT_INSTALLABLE|RUNTIME|DEVELOP,          )), #always tested
                         ("openalea",    (NOT_INSTALLABLE|RUNTIME|DEVELOP|TEST_ME,  )),
                         ("vplants" ,    (NOT_INSTALLABLE|RUNTIME|DEVELOP|TEST_ME,  )),
                         ("r"       ,    (EXE|ARCH|RUNTIME|TEST_ME,                 )),
                         ("rpy2"    ,    (EGG|PY_DEP|ARCH|RUNTIME|TEST_ME,          )),                           
                         ]
                         
                         
                       
                         
