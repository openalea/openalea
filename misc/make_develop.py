#!/usr/python

import sys, os

try:
    from path import path
except:
    pj = os.path.join
    sys.path.insert( 0, pj('..', 'openalea', 'core', 'src', 'core'))
    from path import path

develop_cmd = "python setup.py develop"
uninstall_cmd = "python setup.py develop -u"
dist_cmd = "python setup.py install bdist_egg -d ../../dist sdist -d ../../dist --format=gztar"

cmd = develop_cmd
cmd = uninstall_cmd
cmd = dist_cmd

cwd = path(os.getcwd())
if cmd == dist_cmd:
    dist = cwd/'..'/'dist'
    try:
        if dist.exists():
            dist.removedirs()
    except:
        pass

    #dist.mkdir()
oa_dirs = """core visualea catalog deploy deploygui spatial stand stat plotools image"""
vp_dirs = """PlantGL tool stat_tool sequence_analysis amlobj mtg tree_matching aml PyLsystems"""

dirs = vp_dirs
dirs = oa_dirs

dirs = dirs.split()

for dir in dirs:
    print "Install %s"%dir
    dir = cwd/dir
    os.chdir(dir)
#    build = dir / 'build'
#    if cmd == dist_cmd:
#        dist = dir /'dist'
#        try:
#            if dist.exists():
#                dist.removedirs()
#        except:
#            pass

#    try:
#        if build.exists():
#            build.removedirs()
#    except:
#        pass

    os.system(cmd)

    try:
        if build.exists():
            build.removedirs()
    except:
        pass

    os.chdir(cwd)


