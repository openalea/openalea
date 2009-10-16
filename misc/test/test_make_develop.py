"""Test make_develop for Multisetup object"""

from openalea.misc.make_develop import Multisetup

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

 

mysetup = Multisetup(curdir='../..', commands=args, packages=dirs)

def test_init():
    """ Test of initialization of Multisetup object """
    assert mysetup.commands == ['install']
    assert mysetup.packages == """
                      deploy 
                      deploygui 
                      core 
                      scheduler 
                      visualea 
                      stdlib 
                      sconsx
                      misc
                      """.split()


def test_parse_packages():
    """ Test of parse_packages() method with option --package"""
    mysetup.commands = ['install', '--package', 'core']
    mysetup.parse_packages()

    assert mysetup.packages == ['core']


def test_parse_no_packages():
    """ Test of parse_packages() method with option --no-package"""
    mysetup.packages = dirs
    mysetup.commands = ['install', '--no-package', 'core', '--no-package', 'misc']
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
    mysetup.commands = ['install', 'sdist', '-d', './dist', 'bdist_egg', '--dist-dir', './dist', '--stop-on-errors', '--verbose']
    mysetup.parse_commands()
    
    assert len(mysetup.commands) == 3
    assert mysetup.commands[0] == 'install'
    assert mysetup.commands[1] == 'sdist -d ./dist'
    assert mysetup.commands[2] == 'bdist_egg --dist-dir ./dist'
    assert mysetup.verbose == True
    assert mysetup.force == True 


def test_run():
    """ Test of parse_commands() method"""
    mysetup.commands = ['--package', 'core', 'sdist', '-h' ]
    mysetup.parse_packages()
    mysetup.parse_commands()
    mysetup.run()

    









