# -- Installer and dependency packages description : EDIT THIS --
APPNAME="VPlants"
APPVERSION="0.9"

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