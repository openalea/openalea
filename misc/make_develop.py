#!/usr/python
"""A script to install all modules (listed in this script) within a package.

Should work like setup.py script

:Example:

>>> python make_develop install -p vplants -d ./vplants/trunk  
>>> python make_develop install -p alinea -d ./openaleapkg

type --help to get more help and usage  

"""

__license__ = "Cecill-C"
__revision__ = " $Id$"

import sys, os
from optparse import OptionParser

try:
    from path import path
except:
    pj = os.path.join
    sys.path.insert( 0, pj('..', 'openalea', 'core', 'src', 'core'))
    try:
        from path import path
    except:
        from openalea.core.path import path

def setup( project, command, directory, options=None):
    
    develop_cmd = "python setup.py develop"
    undevelop_cmd = "python setup.py develop -u"
    #install_cmd = "python setup.py install bdist_egg -d ../../dist sdist -d ../../dist --format=gztar"
    install_cmd = "python setup.py install"
    release_cmd = "python setup.py install bdist_egg -d ../../dist sdist -d ../../dist "
    """
    if project == 'vplants':
        release_cmd += '--package=VPlants'
    elif project == 'alinea':
        release_cmd += '--package=Alinea'
    """
    if command == 'develop':
        cmd = develop_cmd
    elif command == 'undevelop':
        cmd = undevelop_cmd
    elif command == 'install':
        cmd = install_cmd
    elif command == 'release':
        cmd = release_cmd
    if options and options.install_dir: 
        cmd += ' --install-dir ' + options.install_dir

    cwd = path(os.getcwd())
    if command == 'release':
        dist = cwd/'..'/'dist'
        try:
            if dist.exists():
                dist.removedirs()
        except:
            pass
    
    oa_dirs = """deploy deploygui core visualea sconsx stdlib openalea_meta"""
    vp_dirs = """PlantGL tool stat_tool sequence_analysis amlobj mtg tree_matching aml fractalysis newmtg WeberPenn vplants_meta"""
    alinea_dirs = """caribu graphtal adel topvine"""
    
    
    if project == 'openalea':
        dirs = oa_dirs
    elif project == 'vplants':
        dirs = vp_dirs
    elif project == 'alinea':
        dirs = alinea_dirs
   
    dirs = dirs.split()
    if command == 'undevelop':
        # if undevelop, we uninstall in the reversed order
        # of the installation. For instance, in OpenAlea case, we want
        # deploy package to be installed first be removed last. This
        # prevents warnings and potential errors due to original 
        # distutils being used.
        dirs.reverse() 
    
    root_dir = path(directory)
    dirs_under_root = root_dir.dirs()
    # check if the dirs are under the given directory.
    for dir in dirs:
        if root_dir/dir not in dirs_under_root:
            print "%s is not a directory of %s"%(dir,str(root_dir.realpath()))
            print "---- EXIT ----"
            return

    for dir in dirs:
        print "--------------"
        print "cd %s"%dir
        print "Executing %s"%cmd
        print '\n'

        dir = root_dir/dir
        os.chdir(dir)
    
        status = os.system(cmd)
        if status != 0:
            print "Error during the execution of %s"%cmd
            print "---- EXIT ----"
            return
    
        os.chdir(cwd)

def main():
    """ Define command line and parse options. """

    usage = """
    %prog [options] develop
    or %prog [options] install
    or %prog [options] release
    or %prog [options] undevelop
"""

    parser = OptionParser(usage=usage)

    parser.add_option( "-p", "--project", dest="project",
                       help="project: openalea, vplants or alinea [default: %default]",
                       default='openalea')
    parser.add_option( "-d", "--dir", dest="directory",
                       help="Directory which contains the various modules [default: %default]",
                       default='.')
    parser.add_option( "-i", "--install-dir", dest="install_dir",
                       help="Directory where to install librairies",
                       default=None)


    available_mode = ['develop', 'undevelop', 'install', 'release']

    try:
        (options, args)= parser.parse_args()
    except Exception,e:
        parser.print_usage()
        print "Error while parsing args:", e
        return

    if(len(args) < 1 or args[0] not in available_mode):
        parser.error("Incomplete command : specify develop, undevelop, install or release")

    mode = args[0]

    status = setup(options.project, mode, options.directory, options)




if(__name__ == "__main__"):
    main()


