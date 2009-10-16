#!/usr/env/python
# -*- python -*-
#
#       Multisetup
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

"""
Multi Setup allows to build and install all the packages of OpenAlea
found in this directory.

It is a shortcut to the script make_develop.

Examples: 

    # Developer mode : Installation of the pks from svn
    python multisetup.py develop

    # User mode: Installation of the packages on the system as root
    python multisetup.py install

    # Administrator mode: Create distribution of the packages
    python multisetup.py nosetests -w test install bdist_egg -d ../dist sdist -d ../dist

TODO:
    - multisetup -h 
        * list of the options
"""
import os, sys

try:
    from openalea.misc.path import path
    from openalea.misc.make_develop import Multisetup
except ImportError:
    # Load misc from its source directory
    sys.path.append(os.path.join('misc', 'src', 'openalea', 'misc'))
    from path import path
    from make_develop import MultiSetup

#curdir = path(os.curdir).abspath()

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



def main():

    args = sys.argv[1:]
    if  len(args) == 1 and args[0] in ['-h', '--help']:
        Multisetup.help()
    else:
        mysetup = Multisetup(curdir='.', commands=args, packages=dirs)
        mysetup.run()


if __name__ == '__main__':
    main()

