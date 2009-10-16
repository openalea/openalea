"""Test make_develop for Multisetup object"""
import os
from openalea.misc.make_develop import Multisetup

"""!!For the following test, don't use intrusive commands such as install 
together with run method. !!!!"""

dirs = """
deploy 
deploygui 
core 
scheduler 
visualea 
stdlib 
sconsx
misc
""".split()


args = ['install']
curdir = '..' + os.sep + '..'
mysetup = Multisetup(curdir=curdir, commands=args, packages=dirs)


def test_init():
    """ Test initialization of Multisetup object """
    mysetup = Multisetup(curdir=curdir, commands=args, packages=dirs)
    assert mysetup.commands == args
    assert mysetup.packages == dirs
    

def test_wrong_package():
    mysetup = Multisetup(curdir=curdir, 
                         commands=['install', '--package','corezzz'],
                         packages=dirs) # !! overwritten by --package
    assert mysetup.packages == ['corezzz']
    
    try:
        mysetup.run()
        assert False
    except:
        assert True
    
def test_parse_packages():
    """ Test of parse_packages() method with option --package"""
    mysetup = Multisetup(curdir=curdir, commands=args, packages=dirs)
    mysetup.commands = ['install', '--package', 'core']
    mysetup.parse_packages()
    assert mysetup.packages == ['core']


def test_parse_no_packages():
    """ Test of parse_packages() method with option --no-package"""
    mysetup = Multisetup(curdir=curdir, commands=args, packages=dirs)
    mysetup.commands = ['install', '--exclude-package', 'core', 
                        '--exclude-package', 'misc']
    mysetup.parse_packages()
 
    assert mysetup.packages == """
                      deploy 
                      deploygui  
                      scheduler 
                      visualea 
                      stdlib 
                      sconsx
                      """.split()


def test_parse_commands():
    """ Test of parse_commands() method"""
    mysetup.commands = ['install', 
                        'sdist', '-d', './dist', 
                        'bdist_egg', '--dist-dir', './dist',  
                        '--verbose', '--keep-going']
    mysetup.parse_commands()
    
    assert len(mysetup.commands) == 3
    assert mysetup.commands[0] == 'install'
    assert mysetup.commands[1] == 'sdist -d ./dist'
    assert mysetup.commands[2] == 'bdist_egg --dist-dir ./dist'
    assert mysetup.verbose == True
    assert mysetup.force == True 


def test_run_verbose():
    """ Test of run() method with verbose option on"""
    mysetup.commands = ['--package', 'core', 'sdist' , '--verbose']
    mysetup.parse_packages()
    mysetup.parse_commands()
    mysetup.run()
    
def test_run_no_verbose():
    """ Test of run() method with verbose option on"""
    mysetup.commands = ['--package', 'core', 'sdist']
    mysetup.parse_packages()
    mysetup.parse_commands()
    mysetup.run()

def test_setup_failure():
    """ Test of run() method with verbose option on"""
    mysetup.commands = ['--package', 'core', 'sdist', '--bad-option']
    mysetup.parse_packages()
    mysetup.parse_commands()
    mysetup.run()








