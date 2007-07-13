# Test installation of fake package
import os, sys


def run_setup(command):
    """ run the setup.py with a particular command """
    os.system("cd fakepackage;" + sys.executable + " setup.py " + command)


def test_build():
    """ Test the build command on fakepakage """
    command = "build"
    run_setup(command)

    fname = "fakepackage/OpenAlea.FakePackage.egg-info/lib_dirs.txt"
    assert os.path.exists(fname)

    f = open(fname, 'r')
    assert f.read() == "test\nlib\n"

    fname = "fakepackage/OpenAlea.FakePackage.egg-info/include_dirs.txt"
    assert os.path.exists(fname)
    f.close()

    f = open(fname, 'r')
    assert f.read() == "include\n"
    f.close()


def test_get_eggs():

    from openalea.deploy import get_eggs
    assert len(set(get_eggs('openalea'))) == 2


def test_get_shared_lib():

    from openalea.deploy import get_lib_dirs
    assert set(get_lib_dirs("openalea.fakepackage")) == set(["lib", "test"])




    


