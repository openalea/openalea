"""Using of make_develop script
"""
import os, sys
from openalea.core.path import path

from openalea.misc.make_develop import Multisetup

curdir = path(os.curdir).abspath()

dirs = ['core', 
        'deploy', 
        'deploygui', 
        'misc', 
        'scheduler', 
        'sconsx', 
        'stdlib', 
        'visualea',
        'openalea_meta']


def main():

    mysetup = Multisetup(curdir, sys.argv[1:], dirs)
    mysetup.run()


if __name__ == '__main__':
    main()
