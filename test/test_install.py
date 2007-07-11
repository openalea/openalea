# Test installation of fake package
import os, sys

def test_build():

    command = "build"
    os.system("cd fakepackage;" + sys.executable + " setup.py " + command)

    
