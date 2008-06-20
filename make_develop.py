#!/usr/python

import sys, os

try:
    from path import path
except:
    pj = os.path.join
    sys.path.insert( 0, pj('core', 'src', 'core'))
    from path import path

develop_cmd = "python setup.py develop"
dist_cmd = "python setup.py bdist_egg -d ../dist sdist -d ../dist --format=gztar"

cmd = develop_cmd

cwd = path(os.getcwd())
if cmd == dist_cmd:
    dist = cwd/'dist'
    if dist.exists():
        dist.removedirs()

    dist.mkdir()
dirs = """core visualea catalog deploy deploygui spatial stand stat plotools image"""
dirs = dirs.split()

for dir in dirs:
    print "Install %s"%dir
    dir = cwd/dir
    os.chdir(dir)
    build = dir / 'build'
    if cmd == dist_cmd:
        dist = dir /'dist'
        if dist.exists():
            dist.removedirs()

    try:
        if build.exists():
            build.removedirs()
    except:
        pass

    os.system(cmd)

    try:
        if build.exists():
            build.removedirs()
    except:
        pass

    os.chdir(cwd)


