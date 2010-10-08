# -- Installer and dependency packages description : EDIT THIS --
APPNAME="VPlants"
APPVERSION="0.9"

# package -> (installerFlags, installationOrder)
thirdPartyPackages = {   "python":      (NOT_INSTALLABLE|RUNTIME|DEVELOP, 0), #always tested
                         "openalea":    (NOT_INSTALLABLE|RUNTIME|DEVELOP|TEST_ME, 1),
                         "scons":       (EGG|DEVELOP|TEST_ME, 2),
                         "bisonflex":   (EGG|DEVELOP|TEST_ME, 3),
                         "boost":       (EGG|PY_DEP|RUNTIME|DEVELOP|TEST_ME, 4),
                         "qhull":       (EGG|RUNTIME|DEVELOP|TEST_ME, 5),
                         "gnuplot":     (EGG|RUNTIME|DEVELOP|TEST_ME, 6),
                         "pyopengl":    (ZIPDIST|RUNTIME|DEVELOP|TEST_ME, 7),
                         "pyqglviewer": (EGG|PY_DEP|RUNTIME|DEVELOP|TEST_ME, 8),
                         }