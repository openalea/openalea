import sys, _winreg, os.path

try:
    r=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\R-core\R")
    rpath=_winreg.QueryValueEx(r, "InstallPath")[0]
    rpath = os.path.join(rpath,"bin","R.exe")
    if os.path.exists(rpath):
        print "exists", rpath
        sys.exit(0)
    else:
        print "doesn't exists", rpath
        sys.exit(1)
except WindowsError, e:
    print "can't find key"
    sys.exit(1)
