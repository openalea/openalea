import subprocess, sys

try:
    subprocess.Popen("R")
    sys.exit(0)
except Exception, e:
    sys.exit(1)
