import sys

try:
    from win32com.shell import shell, shellcon
    sys.exit(0)
except Exception, e:
    sys.exit(1)
