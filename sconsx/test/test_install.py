"""Test installation of fake package"""

__license__ = "Cecill-C"
__revision__ =" $Id$"

import os, sys

def run_setup(command):
    """ run the setup.py with a particular command """
    oldDir = os.getcwd()
    os.chdir("fakepackage")
    py = sys.executable
    os.spawnl(os.P_WAIT, py, py, "setup.py", command)
    os.chdir(oldDir)


def test_build():
    """ Test the build command on fakepakage """
    command = "build"
    run_setup(command)

    fname = "fakepackage/OpenAlea.FakePackage.egg-info/lib_dirs.txt"
    assert os.path.exists(fname)

    f = open(fname, 'r')
    assert f.read() == "lib\n"

    fname = "fakepackage/OpenAlea.FakePackage.egg-info/inc_dirs.txt"
    assert os.path.exists(fname)
    f.close()

    f = open(fname, 'r')
    assert f.read() == "include\n"
    f.close()


def _test_get_eggs():
    """need to be fixced"""
    from openalea.deploy import get_eggs
    print get_eggs('openalea')
    print set(get_eggs('openalea'))
    print len(set(get_eggs('openalea')))

    assert len(set(get_eggs('openalea'))) == 8


def _test_get_shared_lib():

    from openalea.deploy import get_lib_dirs
    assert set(get_lib_dirs("openalea.fakepackage")) == set(["lib"])


def _test_get_shared_inc():

    from openalea.deploy import get_inc_dirs
    print set(get_inc_dirs("openalea.fakepackage"))
    assert set(get_inc_dirs("openalea.fakepackage")) == set(["include"])


def _test_get_postinstall_scripts():

    from openalea.deploy import get_postinstall_scripts
    print list(get_postinstall_scripts("openalea.fakepackage"))
    assert set(get_postinstall_scripts("openalea.fakepackage")) == \
           set(["openalea.fakepackage.postinstall"])


