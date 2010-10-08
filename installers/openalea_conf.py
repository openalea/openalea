# -- Installer and dependency packages description : EDIT THIS --
APPNAME="OpenAlea"
APPVERSION="0.9"

# package -> (installerFlags, installationOrder)
thirdPartyPackages = {   "python":      (MSI|RUNTIME|DEVELOP, 0),
                         "pywin32":     (EXE|PY_DEP|RUNTIME|DEVELOP|TEST_ME, 1),
                         "setuptools":  (EXE|PY_DEP|RUNTIME|DEVELOP|TEST_ME, 2),
                         "PyQt":       (EXE|PY_DEP|RUNTIME|DEVELOP|TEST_ME, 3),
                         }
                         


# -- The default _generate_post_install_code(opt) function returns "". --
# -- Let's do something smarter for openalea, to add it to start menu. --
                         
postInstallPascalTemplate = StrictTemplate("""
    Exec(GetPythonDirectory()+'python.exe', '-c "import sys;sys.path.append(\"'+ GetPythonDirectory()+'Lib\site-packages\'+Eggs[$VISUALEAEGGID]+'\");import visualea_postinstall as vp;vp.install()', '',
          SW_HIDE, ewWaitUntilTerminated, ResultCode)""")
          
def _generate_post_install_code(options):
    eggs = options["eggs"]
    visualeaId = -1
    for i, e in enumerate(eggs):
        if "Visualea" in e:
            visualeaId = str(i)
            
    return postInstallPascalTemplate.substitute(VISUALEAEGGID=visualeaId)        