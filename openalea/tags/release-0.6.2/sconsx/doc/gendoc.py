"""script to automatically generate epydoc documentation


"""
import os
import sys
sys.path.append(os.path.abspath("../../core/src/core"))
from openalea.core.path import path
import version

module='sconsx'
filepattern = "../src/sconsx"
outdir = module + "-%s"%(version.version)
exclude_pattern=[]

# in test mode
test=False

# do not change anythin below in principle !
epydoc_options= """
--html
--name "OpenAlea API"
--docformat restructuredtext
--graph all
--url http://openalea.gforge.inria.fr
--include-log
--show-sourcecode
"""


def run(cmd, verbose=True, test=True):
    """ simple run command alias"""
    if verbose:
        print cmd
    if not test:
        os.system(cmd)


def getfiles():
    """read recursively all python files in a directory and returns a string"""
    d = path(filepattern)
    files = d.walkfiles('*.py')
    list = []
    list = ""
    for file in files:
        if "__wralea__.py" not in file and "__init__.py" not in file:
            list += ' ' + file
    return list


def add_exclude(opt):
    if len(exclude_pattern):
        opt += "  --exclude " 
        for elt in exclude_pattern:
            opt += elt + " "    
    return opt


if __name__ == '__main__':
    # get all python files
    files = getfiles()

    # this is the epydoc command line arguments
    opt = ' '.join(epydoc_options.split())
    opt = add_exclude(opt)
    run('epydoc %s -o %s %s  ' % (opt, outdir, files),
        verbose=True, test=test)
    run('epydoc %s -o %s %s --pdf ' % (opt, outdir, files),
        verbose=True, test=test)

    # once done, we can scp the documentation
    run('scp -r %s scm.gforge.inria.fr:/home/groups/openalea/htdocs/doc/'
        % (outdir), verbose=True, test=test)
