# Test installation of fake package
import os, sys


def run_setup(command):
    """ run the setup.py with a particular command """
    os.system("cd fakepackage;" + sys.executable + " setup.py " + command)


def test_build():
    """ Test the build command on fakepakage """
    command = "build"
    run_setup(command)
    
def test_intall():
    """ Test the intall command on fakepakage """
    run_setup("install")


def test_get_eggs():

    from openalea.deploy import get_eggs

    assert len(set(get_eggs('openalea'))) == 2

def test_get_shared_lib():

    from openalea.deploy import get_shared_lib

    assert list(get_shared_lib("openalea.fakepackage")) == ["lib", "test"]
    


